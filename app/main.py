"""Main application file for the Smart Plant Care app."""
import os
import streamlit as st
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

# Hide Streamlit elements and remove spacing
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        header {visibility: hidden;}
        .appview-container {margin: 0; padding: 0;}
        .css-1544g2n {padding: 0 !important;}
        .css-1y4p8pa {padding: 0 !important;}
        .css-18e3th9 {padding: 0 !important;}
        .block-container {padding: 0; max-width: 100%;}
        section[data-testid="stSidebarContent"] {padding-top: 1rem;}
        div[data-testid="stToolbar"] {display: none;}
        div[data-testid="stDecoration"] {display: none;}
        div[data-testid="stStatusWidget"] {display: none;}
        #root > div:nth-child(1) > div > div > div {gap: 0;}
    </style>
""", unsafe_allow_html=True)

# Load CSS
with open(os.path.join(os.path.dirname(__file__), 'styles', 'main.css'), 'r') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set max upload size to 20MB
st.session_state.max_upload_size = 20 * 1024 * 1024  # 20MB in bytes

def main():
    """Main function to run the Streamlit app."""
    # Render sidebar
    render_sidebar()

    # Main content container
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Render header
    render_header()

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload plant image",
        type=['jpg', 'jpeg', 'png'],
        key="plant_upload",
        label_visibility="collapsed"
    )

    # Custom upload UI
    st.markdown("""
        <div class="upload-container" id="upload-container">
            <h2 class="upload-title">Drop your plant photo here or click to browse</h2>
            <div class="upload-area" onclick="document.querySelector('.stFileUploader input[type=\'file\']').click()">
                <div class="upload-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M4 16L8 12M12 8L8 12M8 12L12 16M8 12H20M20 12V18C20 19.1046 19.1046 20 18 20H6C4.89543 20 4 19.1046 4 18V6C4 4.89543 4.89543 4 6 4H18C19.1046 4 20 4.89543 20 6V12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <p class="upload-instructions">Drag and drop file here</p>
                <p class="upload-limits">Limit 20MB per file • JPG, JPEG, PNG</p>
            </div>
            <div class="upload-requirements">
                <div class="upload-requirement">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Clear, well-lit photo
                </div>
                <div class="upload-requirement">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Max size: 20MB
                </div>
                <div class="upload-requirement">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    JPG, JPEG, PNG
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Handle uploaded file
    if uploaded_file is not None:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        # Check file size
        if len(uploaded_file.getvalue()) > st.session_state.max_upload_size:
            st.error("❌ File size exceeds 20MB limit. Please upload a smaller image.")
            return

        # Display image preview
        st.markdown('<div class="image-preview">', unsafe_allow_html=True)
        st.image(uploaded_file, caption="Uploaded Plant Image", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Show loading animation and analyze image
        with st.spinner('🔍 Analyzing your plant...'):
            health_status, confidence = analyze_image(uploaded_file)
            
            if health_status is not None and confidence is not None:
                # Render results
                render_results(health_status, confidence)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <footer class="footer">
            <div class="footer-content">
                v1.0.0 • Made with 
                <span class="footer-heart">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                    </svg>
                </span>
            </div>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 