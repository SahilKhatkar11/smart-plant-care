"""Model utility functions for the Smart Plant Care application."""
import os
import streamlit as st
import tensorflow as tf
from PIL import Image
import io
import numpy as np
from typing import Union, BinaryIO

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

def analyze_image(image_data: Union[str, Image.Image, BinaryIO]):
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

        # Convert input to PIL Image
        if isinstance(image_data, str):
            # Load from file path
            image = Image.open(image_data)
        elif isinstance(image_data, Image.Image):
            # Already a PIL Image
            image = image_data
        else:
            # Assume file-like object
            try:
                image = Image.open(image_data)
                # Reset file pointer for file-like objects
                if hasattr(image_data, 'seek'):
                    image_data.seek(0)
            except Exception as e:
                st.error(f"Error opening image: {str(e)}")
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