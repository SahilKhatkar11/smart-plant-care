"""Model utility functions for the Smart Plant Care application."""
import os
import streamlit as st
import tensorflow as tf
from PIL import Image, ImageFile
import io
import numpy as np
import cv2
import imghdr
import tempfile
from typing import Union, BinaryIO, Optional, Tuple

# Allow loading truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

@st.cache_resource
def load_model():
    """Load the trained model from disk."""
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                             'model', 'plant_health_model.h5')
    if not os.path.exists(model_path):
        st.error("Model file not found! Please ensure the model is properly trained.")
        return None
    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def load_image_multiple_methods(image_data: Union[str, Image.Image, BinaryIO]) -> Optional[Image.Image]:
    """Try multiple methods to load an image.

    Args:
        image_data: PIL Image object, file-like object, or path to image file

    Returns:
        Optional[Image.Image]: A loaded PIL Image or None if all methods fail
    """
    image = None
    errors = []

    # Method 1: Direct PIL approach
    try:
        if isinstance(image_data, str):
            # Load from file path
            image = Image.open(image_data)
            image.load()  # Force load to verify image is valid
        elif isinstance(image_data, Image.Image):
            # Already a PIL Image, make a copy
            image = image_data.copy()
            image.load()  # Force load to verify image is valid
        else:
            # Assume file-like object
            if hasattr(image_data, 'seek'):
                image_data.seek(0)

            # Try to get file extension or type
            file_type = None
            if hasattr(image_data, 'name') and '.' in image_data.name:
                file_type = image_data.name.split('.')[-1].lower()

            # Read bytes
            if hasattr(image_data, 'read'):
                image_bytes = image_data.read()
                if hasattr(image_data, 'seek'):
                    image_data.seek(0)
            else:
                # If we can't read, return None
                return None

            # Try to identify image format
            img_format = imghdr.what(None, h=image_bytes)

            # Create BytesIO object
            image_buffer = io.BytesIO(image_bytes)
            image = Image.open(image_buffer)
            image.load()  # Force load to verify image is valid

        # Test if image is valid
        if image.width == 0 or image.height == 0:
            raise ValueError("Image has invalid dimensions")

        return image
    except Exception as e:
        errors.append(f"PIL direct method failed: {str(e)}")

    # Method 2: Via temporary file with PIL
    try:
        if isinstance(image_data, str):
            # Already a file path, just open it
            image = Image.open(image_data)
            image.load()
            return image

        # Get image bytes
        if isinstance(image_data, Image.Image):
            # Convert PIL image to bytes
            byte_arr = io.BytesIO()
            image_data.save(byte_arr, format='PNG')
            image_bytes = byte_arr.getvalue()
        elif hasattr(image_data, 'read'):
            if hasattr(image_data, 'seek'):
                image_data.seek(0)
            image_bytes = image_data.read()
            if hasattr(image_data, 'seek'):
                image_data.seek(0)
        else:
            return None

        # Try to detect image type
        img_format = imghdr.what(None, h=image_bytes)
        file_ext = f'.{img_format}' if img_format else '.png'

        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            tmp_file.write(image_bytes)
            tmp_file.flush()

            # Try to open with PIL
            for mode in ['RGB', 'RGBA', 'L', 'P', '1']:
                try:
                    img = Image.open(tmp_file.name)
                    img.load()  # Force load

                    # Convert to requested mode
                    if img.mode != mode:
                        img = img.convert(mode)

                    # Clean up
                    os.unlink(tmp_file.name)
                    return img
                except Exception:
                    continue

            # Clean up if all modes failed
            os.unlink(tmp_file.name)
    except Exception as e:
        errors.append(f"Temporary file with PIL method failed: {str(e)}")

    # Method 3: Try OpenCV
    try:
        # Get image bytes
        if isinstance(image_data, str):
            # Read image with OpenCV directly
            img_cv = cv2.imread(image_data)
            if img_cv is not None and img_cv.size > 0:
                # Convert from BGR to RGB
                img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                # Convert to PIL
                return Image.fromarray(img_cv)
        elif isinstance(image_data, Image.Image):
            # Already have a PIL image
            return image_data
        else:
            # Get bytes from file-like object
            if hasattr(image_data, 'seek'):
                image_data.seek(0)

            if hasattr(image_data, 'read'):
                image_bytes = image_data.read()
                if hasattr(image_data, 'seek'):
                    image_data.seek(0)
            else:
                return None

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                tmp_file.write(image_bytes)
                tmp_file.flush()

                # Read with OpenCV
                img_cv = cv2.imread(tmp_file.name)
                os.unlink(tmp_file.name)

                if img_cv is not None and img_cv.size > 0:
                    # Convert from BGR to RGB
                    img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                    # Convert to PIL
                    return Image.fromarray(img_cv)
    except Exception as e:
        errors.append(f"OpenCV method failed: {str(e)}")

    # If we got here, all methods failed
    if errors:
        st.error(f"All image loading methods failed:\n" + "\n".join(errors))
    return None

def analyze_image(image_data: Union[str, Image.Image, BinaryIO]) -> Tuple[Optional[bool], Optional[float]]:
    """Analyze an image using the trained model.

    Args:
        image_data: PIL Image object, file-like object, or path to image file

    Returns:
        tuple: (health_status: bool, confidence: float)
    """
    try:
        # Load the model
        model = load_model()
        if model is None:
            return None, None

        # Try multiple methods to load the image
        image = load_image_multiple_methods(image_data)

        # Verify image was loaded successfully
        if image is None:
            st.error("Failed to load image with any method")
            return None, None

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize image to match model's expected input size
        image = image.resize((224, 224))

        # Convert to numpy array and normalize
        img_array = np.array(image)
        img_array = img_array.astype('float32') / 255.0

        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_array, verbose=0)

        # Get health status and confidence
        prediction_value = float(prediction[0][0])
        health_status = prediction_value > 0.5
        confidence = prediction_value if health_status else 1 - prediction_value

        return health_status, confidence

    except Exception as e:
        st.error(f"Error analyzing image: {str(e)}")
        # Reset file pointer if there's an error and it's a file-like object
        if not isinstance(image_data, (str, Image.Image)) and hasattr(image_data, 'seek'):
            image_data.seek(0)
        return None, None
