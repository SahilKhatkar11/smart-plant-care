"""Main application file for the Smart Plant Care app."""
import os
import streamlit as st
from PIL import Image
import io
from components.header import render_header
from components.sidebar import render_sidebar
from components.results import render_results
from utils.model_utils import analyze_image

# Set page config
st.set_page_config(
    page_title="Smart Plant Care",
    page_icon="🌿",
    layout="wide"
)

# Configure page styling
st.markdown("""
    <style>
        /* Reset Streamlit styles */
        .stApp {
            background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
        }
        
        .stMarkdown {
            color: #1a365d !important;
        }
        
        /* Hide Streamlit components */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        header {visibility: hidden;}
        div[data-testid="stToolbar"] {display: none;}
        div[data-testid="stDecoration"] {display: none;}
        div[data-testid="stStatusWidget"] {display: none;}
        
        /* Main content styling */
        .main .block-container {
            padding: 2rem;
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        }
        
        /* Upload container */
        .upload-container {
            background: linear-gradient(135deg, #e6f4ff 0%, #ffffff 100%);
            border-radius: 16px;
            padding: 2.5rem;
            box-shadow: 0 4px 15px rgba(0, 118, 255, 0.1);
            border: 2px solid #e1effe;
            text-align: center;
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }
        
        .upload-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 118, 255, 0.15);
        }
        
        /* File uploader */
        .stFileUploader {
            width: 100%;
            max-width: 500px;
            margin: 0 auto;
        }
        
        .stFileUploader > div {
            background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%) !important;
            border: 2px dashed #60a5fa !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            color: #2563eb !important;
            transition: all 0.3s ease !important;
        }
        
        .stFileUploader > div:hover {
            border-color: #2563eb !important;
            background: linear-gradient(135deg, #e6f4ff 0%, #ffffff 100%) !important;
            transform: scale(1.02);
        }
        
        .stFileUploader > div > div {
            color: #2563eb !important;
        }
        
        /* Results container */
        .results-container {
            background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0, 118, 255, 0.1);
            border: 2px solid #e1effe;
        }
        
        /* Two-column layout */
        .results-grid {
            display: grid;
            grid-template-columns: 300px 1fr;
            gap: 2rem;
            align-items: start;
        }
        
        /* Image preview */
        .image-preview {
            width: 100%;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 118, 255, 0.1);
            background: white;
            padding: 0.75rem;
            border: 2px solid #e1effe;
            transition: all 0.3s ease;
        }
        
        .image-preview:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 118, 255, 0.15);
        }
        
        .image-preview img {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 8px;
        }
        
        /* Analysis results */
        .analysis-results {
            background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
            border-radius: 12px;
            padding: 2rem;
            border: 2px solid #e1effe;
            box-shadow: 0 4px 15px rgba(0, 118, 255, 0.1);
        }
        
        /* Error message */
        .stAlert {
            background: #fee2e2 !important;
            color: #991b1b !important;
            border-radius: 12px !important;
            border: 2px solid #fecaca !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-color: #2563eb !important;
            border-right-color: transparent !important;
        }
        
        /* Button styles */
        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .results-grid {
                grid-template-columns: 1fr;
            }
            
            .image-preview {
                max-width: 300px;
                margin: 0 auto;
            }
            
            .main .block-container {
                padding: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    # Render sidebar
    render_sidebar()
    
    # Main content
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown("""
        <h1 style="font-size: 2rem; font-weight: 700; color: #1e40af; margin-bottom: 1rem;">
            🌿 Plant Health Analysis
        </h1>
        <p style="font-size: 1.1rem; color: #3b82f6; max-width: 600px; margin: 0 auto 1.5rem; line-height: 1.6;">
            Upload a photo of your plant and let our AI analyze its health status.
        </p>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a photo of your plant",
        type=['jpg', 'jpeg', 'png']
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Handle uploaded file
    if uploaded_file is not None:
        try:
            # Create a copy of the file in memory
            image_bytes = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(image_bytes))
            
            # Display image and results in a two-column layout
            st.markdown('<div class="results-grid">', unsafe_allow_html=True)
            
            # Column 1: Image Preview
            st.markdown('<div class="image-preview">', unsafe_allow_html=True)
            st.image(image, use_column_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Column 2: Analysis Results
            with st.spinner('🔍 Analyzing your plant...'):
                # Analyze the image
                health_status, confidence = analyze_image(image)
                
                # Render results
                st.markdown('<div class="analysis-results">', unsafe_allow_html=True)
                render_results(health_status, confidence)
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main() 