import cv2
import numpy as np
from PIL import Image
import tensorflow as tf

def load_and_preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess an image for model prediction
    
    Args:
        image_path: Path to the image file or uploaded file object
        target_size: Tuple of (height, width) to resize the image to
        
    Returns:
        Preprocessed image array ready for model prediction
    """
    # Handle both file paths and uploaded file objects
    if isinstance(image_path, str):
        img = Image.open(image_path)
    else:
        img = Image.open(image_path)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize image
    img = img.resize(target_size)
    
    # Convert to numpy array and normalize
    img_array = np.array(img)
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def get_care_suggestions(prediction):
    """
    Generate care suggestions based on model prediction
    
    Args:
        prediction: Model prediction probability (0-1)
        
    Returns:
        Dictionary containing care suggestions
    """
    if prediction >= 0.5:  # Healthy
        suggestions = {
            'status': 'Healthy',
            'confidence': f'{prediction * 100:.1f}%',
            'care_tips': [
                'Continue with regular watering schedule',
                'Maintain current light conditions',
                'Regular pruning to maintain health',
                'Monitor for any changes in leaf color'
            ]
        }
    else:  # Unhealthy
        suggestions = {
            'status': 'Unhealthy',
            'confidence': f'{(1 - prediction) * 100:.1f}%',
            'care_tips': [
                'Check for signs of pests or disease',
                'Ensure proper watering (not too much/little)',
                'Verify light conditions are appropriate',
                'Consider checking soil nutrients',
                'Remove any dead or yellowing leaves'
            ]
        }
    
    return suggestions 