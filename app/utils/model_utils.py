"""Model utility functions for the Smart Plant Care application."""
import os
import streamlit as st
import tensorflow as tf
from .preprocess import load_and_preprocess_image

@st.cache_resource
def load_model():
    """Load the trained model from disk."""
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                             'model', 'plant_health_model.h5')
    if not os.path.exists(model_path):
        st.error("❌ Model file not found! Please train the model first.")
        return None
    return tf.keras.models.load_model(model_path)

def analyze_image(image_file):
    """Analyze an image using the trained model.
    
    Args:
        image_file: The uploaded image file.
        
    Returns:
        tuple: (health_status: bool, confidence: float)
    """
    try:
        # Load and preprocess the image
        img = load_and_preprocess_image(image_file)
        
        # Load the model
        model = load_model()
        if model is None:
            return None, None
            
        # Make prediction
        prediction = model.predict(img)
        health_status = bool(prediction[0][0] > 0.5)
        confidence = float(prediction[0][0] if health_status else 1 - prediction[0][0])
        
        return health_status, confidence
        
    except Exception as e:
        st.error(f"❌ Error analyzing image: {str(e)}")
        return None, None 