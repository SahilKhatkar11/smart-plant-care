"""Main application file for the Smart Plant Care app."""
import os
import streamlit as st
from PIL import Image
import io
import numpy as np
import sys
# Add utils directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.utils.image_diagnostics import run_image_diagnostic_test, diagnose_image, repair_image
from components.header import render_header
from components.sidebar import render_sidebar, render_sidebar_toggle
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
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 50%, #ffffff 100%);
            min-height: 100vh;
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
            padding: 0;
            max-width: 1200px;
            margin: 0 auto;
            background: transparent;
            transition: all 0.4s ease;
        }

        /* Adjust main content when sidebar is hidden */
        .sidebar-hidden .main .block-container {
            margin-left: 0;
            max-width: 1400px;
        }

        /* Hero Section */
        .hero-section {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
            border-radius: 0 0 30px 30px;
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            margin-bottom: 3rem;
            box-shadow: 0 20px 40px rgba(30, 64, 175, 0.2);
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            pointer-events: none;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 800px;
            margin: 0 auto;
        }

        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: white;
            margin-bottom: 1.5rem;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            animation: fadeInUp 1s ease-out;
        }

        .hero-subtitle {
            font-size: 1.25rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 2rem;
            line-height: 1.6;
            animation: fadeInUp 1s ease-out 0.2s both;
        }

        .hero-features {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease-out 0.4s both;
        }

        .hero-feature {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.95rem;
            font-weight: 500;
        }

        .hero-feature-icon {
            font-size: 1.25rem;
        }

        /* Upload container */
        .upload-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            margin: 0 2rem 3rem 2rem;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .upload-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.6s ease;
            opacity: 0;
        }

        .upload-container:hover::before {
            opacity: 1;
            transform: rotate(45deg) translate(50%, 50%);
        }

        .upload-container:hover {
            transform: translateY(-8px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
        }

        .upload-title {
            font-size: 2rem;
            font-weight: 700;
            color: #1e40af;
            margin-bottom: 1rem;
            position: relative;
            z-index: 2;
        }

        .upload-description {
            font-size: 1.1rem;
            color: #64748b;
            max-width: 600px;
            margin: 0 auto 2rem;
            line-height: 1.6;
            position: relative;
            z-index: 2;
        }

        /* File uploader container */
        .file-uploader-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 3rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-align: center;
            margin: 0 2rem 3rem 2rem;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .file-uploader-container::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.6s ease;
            opacity: 0;
        }

        .file-uploader-container:hover::before {
            opacity: 1;
            transform: rotate(45deg) translate(50%, 50%);
        }

        .file-uploader-container:hover {
            transform: translateY(-8px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.15);
        }

        /* File uploader */
        .stFileUploader {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }

        .stFileUploader > div {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%) !important;
            border: 3px dashed #60a5fa !important;
            border-radius: 16px !important;
            padding: 3rem 2rem !important;
            color: #2563eb !important;
            transition: all 0.4s ease !important;
            position: relative;
            overflow: hidden;
        }

        /* Hide the default Streamlit label */
        .stFileUploader > div > div:first-child {
            display: none !important;
        }

        /* Style the upload area content */
        .stFileUploader > div > div:last-child {
            background: transparent !important;
            border: none !important;
            color: #2563eb !important;
            font-weight: 500 !important;
        }

        /* Override any dark styling */
        .stFileUploader > div,
        .stFileUploader > div > div,
        .stFileUploader > div > div > div {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%) !important;
            color: #2563eb !important;
            border-color: #60a5fa !important;
        }

        /* Force white background and blue text for all uploader elements */
        [data-testid="stFileUploader"] > div,
        [data-testid="stFileUploader"] > div > div,
        [data-testid="stFileUploader"] > div > div > div,
        [data-testid="stFileUploader"] > div > div > div > div {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%) !important;
            color: #2563eb !important;
            border-color: #60a5fa !important;
        }

        /* Style the drag and drop text */
        [data-testid="stFileUploader"] div[data-testid="stMarkdown"] {
            color: #2563eb !important;
            font-weight: 500 !important;
        }

        /* Style the browse button */
        [data-testid="stFileUploader"] button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        [data-testid="stFileUploader"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
        }

        .stFileUploader > div::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.1), transparent);
            transition: left 0.6s ease;
        }

        .stFileUploader > div:hover::before {
            left: 100%;
        }

        .stFileUploader > div:hover {
            border-color: #2563eb !important;
            background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%) !important;
            transform: scale(1.02);
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.15);
        }

        .stFileUploader > div > div {
            color: #2563eb !important;
            font-weight: 500;
        }

        /* Results container */
        .results-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            margin: 0 2rem;
            animation: slideInUp 0.6s ease-out;
        }

        /* Two-column layout */
        .results-grid {
            display: grid;
            grid-template-columns: 350px 1fr;
            gap: 3rem;
            align-items: start;
        }

        /* Image preview */
        .image-preview {
            width: 100%;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            background: white;
            padding: 1rem;
            border: 2px solid #e1effe;
            transition: all 0.4s ease;
            position: relative;
        }

        .image-preview::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.05), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .image-preview:hover::before {
            opacity: 1;
        }

        .image-preview:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }

        .image-preview img {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 12px;
            transition: transform 0.3s ease;
        }

        .image-preview:hover img {
            transform: scale(1.02);
        }

        /* Analysis results */
        .analysis-results {
            background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
            border-radius: 16px;
            padding: 2rem;
            border: 2px solid #e1effe;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }

        .analysis-results:hover {
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }

        /* Error message */
        .stAlert {
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
            color: #991b1b !important;
            border-radius: 16px !important;
            border: 2px solid #fecaca !important;
            padding: 1.5rem !important;
            margin: 1rem 0 !important;
            box-shadow: 0 10px 25px rgba(220, 38, 38, 0.1);
        }

        /* Custom error message styling */
        .error-container {
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border: 2px solid #fecaca;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            color: #991b1b;
            font-weight: 500;
            box-shadow: 0 10px 25px rgba(220, 38, 38, 0.1);
        }

        .error-title {
            margin: 0 0 0.5rem 0;
            color: #dc2626;
            font-size: 1.1rem;
            font-weight: 600;
        }

        .error-message {
            margin: 0 0 0.5rem 0;
            color: #991b1b;
            font-size: 1rem;
        }

                 .error-help {
             margin: 0;
             font-size: 0.9rem;
             color: #7f1d1d;
         }
         
         /* Diagnostic section styling */
         .diagnostic-section {
             background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
             border: 2px solid #7dd3fc;
             border-radius: 16px;
             padding: 2rem;
             margin: 2rem 0;
             box-shadow: 0 10px 25px rgba(30, 64, 175, 0.1);
         }
         
         .diagnostic-title {
             color: #1e40af;
             margin-bottom: 1rem;
             display: flex;
             align-items: center;
             gap: 0.5rem;
             font-size: 1.25rem;
             font-weight: 600;
         }
         
         .diagnostic-description {
             color: #374151;
             margin-bottom: 1.5rem;
             line-height: 1.6;
         }
         
         /* Warning message styling */
         .warning-message {
             background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
             border: 2px solid #fdcb6e;
             border-radius: 12px;
             padding: 1rem;
             margin: 0.75rem 0;
             color: #856404;
             font-weight: 500;
             box-shadow: 0 4px 12px rgba(253, 203, 110, 0.2);
         }
         
         .warning-title {
             color: #d63031;
             font-weight: 600;
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
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3) !important;
        }

        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .pulse-animation {
            animation: pulse 2s ease-in-out infinite;
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }

            .hero-features {
                flex-direction: column;
                gap: 1rem;
            }

            .results-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
            }

            .image-preview {
                max-width: 400px;
                margin: 0 auto;
            }

            .upload-container {
                margin: 0 1rem 2rem 1rem;
                padding: 2rem;
            }

            .file-uploader-container {
                margin: 0 1rem 2rem 1rem;
                padding: 2rem;
            }

            .results-container {
                margin: 0 1rem;
            }

            /* Adjust sidebar toggle for mobile */
            .sidebar-toggle {
                top: 10px;
                left: 10px;
                width: 40px;
                height: 40px;
                font-size: 1rem;
            }
        }

        @media (max-width: 480px) {
            .hero-section {
                padding: 3rem 1rem;
            }

            .hero-title {
                font-size: 2rem;
            }

            .upload-title {
                font-size: 1.5rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    # Initialize sidebar state
    if 'sidebar_visible' not in st.session_state:
        st.session_state.sidebar_visible = True

    # Render sidebar toggle button
    render_sidebar_toggle()

    # Render sidebar only if visible
    if st.session_state.sidebar_visible:
        render_sidebar()

    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">🌿 Smart Plant Care</h1>
                <p class="hero-subtitle">
                    Transform your plant care with AI-powered health analysis.
                    Get instant insights and personalized recommendations to help your plants thrive.
                </p>
                <div class="hero-features">
                    <div class="hero-feature">
                        <span class="hero-feature-icon">🤖</span>
                        <span>AI-Powered Analysis</span>
                    </div>
                    <div class="hero-feature">
                        <span class="hero-feature-icon">⚡</span>
                        <span>Instant Results</span>
                    </div>
                    <div class="hero-feature">
                        <span class="hero-feature-icon">💡</span>
                        <span>Smart Recommendations</span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Main content
    st.markdown("""
        <div class="upload-container">
            <h2 class="upload-title">📸 Upload Your Plant Photo</h2>
            <p class="upload-description">
                Take a clear photo of your plant, focusing on any areas of concern.
                Our advanced AI will analyze the image and provide detailed health insights.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # File uploader in its own container
    st.markdown("""
        <div class="file-uploader-container">
            <h3 style="color: #1e40af; margin-bottom: 1.5rem; font-size: 1.25rem; font-weight: 600;">
                📸 Choose a photo of your plant
            </h3>
            <p style="color: #64748b; margin-bottom: 1rem; font-size: 0.9rem;">
                Supported formats: JPG, JPEG, PNG<br>
                For best results, use a well-lit, clear image under 5MB
            </p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",  # Empty label since we have custom HTML above
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear, well-lit photo of your plant for the best analysis results."
    )

    # Handle uploaded file
    if uploaded_file is not None:
        try:
            # Get file info for debugging
            file_info = f"File: {uploaded_file.name}, Type: {uploaded_file.type}, Size: {uploaded_file.size} bytes"

            # Reset file pointer and read bytes
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()

            # Try multiple approaches to load the image
            image = None

            # Method 1: Direct BytesIO with proper error handling
            try:
                # Create a fresh BytesIO object to ensure clean data
                image_buffer = io.BytesIO(image_bytes)
                image = Image.open(image_buffer)

                # Verify image is valid by forcing load
                image.load()

                # Convert to RGB immediately to avoid mode issues
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                # Test if image can be processed
                test_array = np.array(image)
                if test_array.size == 0:
                    raise Exception("Image array is empty")
            except Exception as e1:
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border: 2px solid #fdcb6e; border-radius: 12px; padding: 1rem; margin: 0.75rem 0; color: #856404; font-weight: 500; box-shadow: 0 4px 12px rgba(253, 203, 110, 0.2);">
                        <strong style="color: #d63031;">⚠️ Method 1 failed:</strong> {str(e1)}
                    </div>
                """, unsafe_allow_html=True)

                # Method 2: Using temporary file with proper extension
                try:
                    import tempfile
                    import os
                    import imghdr

                    # Try to detect actual image type regardless of extension
                    actual_type = imghdr.what(None, h=image_bytes)

                    # Use detected type if available, fallback to content-type
                    if actual_type:
                        file_extension = f'.{actual_type}'
                    else:
                        file_extension = '.png' if uploaded_file.type == 'image/png' else '.jpg'

                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                        tmp_file.write(image_bytes)
                        tmp_file.flush()
                        os.fsync(tmp_file.fileno())  # Ensure data is written to disk

                        # Force sync and wait
                        import time
                        time.sleep(0.1)

                        image = Image.open(tmp_file.name)
                        image.load()  # Force load to verify image is valid

                        if image.mode != 'RGB':
                            image = image.convert('RGB')

                        # Clean up
                        os.unlink(tmp_file.name)
                except Exception as e2:
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border: 2px solid #fdcb6e; border-radius: 12px; padding: 1rem; margin: 0.75rem 0; color: #856404; font-weight: 500; box-shadow: 0 4px 12px rgba(253, 203, 110, 0.2);">
                            <strong style="color: #d63031;">⚠️ Method 2 failed:</strong> {str(e2)}
                        </div>
                    """, unsafe_allow_html=True)

                    # Method 3: Try with different approach and image libraries
                    try:
                        import tempfile
                        import cv2

                        # Try OpenCV as an alternative to PIL
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                            tmp_file.write(image_bytes)
                            tmp_file.flush()
                            os.fsync(tmp_file.fileno())

                            # Try OpenCV first
                            try:
                                cv_img = cv2.imread(tmp_file.name)
                                if cv_img is not None and cv_img.size > 0:
                                    # Convert from BGR to RGB
                                    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
                                    # Convert OpenCV image to PIL
                                    image = Image.fromarray(cv_img)
                                else:
                                    raise Exception("OpenCV could not load the image")
                            except Exception as cv_error:
                                # Fallback to PIL with different modes
                                for mode in ['RGB', 'RGBA', 'L', 'P', '1']:
                                    try:
                                        image = Image.open(tmp_file.name)
                                        image.load()  # Force load
                                        image = image.convert(mode)
                                        if mode != 'RGB':
                                            image = image.convert('RGB')
                                        break
                                    except:
                                        continue

                            # Clean up
                            os.unlink(tmp_file.name)

                            if image is None:
                                raise Exception("Could not load image with any method or mode")
                    except Exception as e3:
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); border: 2px solid #fdcb6e; border-radius: 12px; padding: 1rem; margin: 0.75rem 0; color: #856404; font-weight: 500; box-shadow: 0 4px 12px rgba(253, 203, 110, 0.2);">
                                <strong style="color: #d63031;">⚠️ Method 3 failed:</strong> {str(e3)}
                            </div>
                        """, unsafe_allow_html=True)
                        raise Exception(f"All methods failed. The image file appears to be corrupted or in an unsupported format.")

            # Verify image was loaded
            if image is None:
                raise Exception("Failed to load image from file")

            # Display image and results in a two-column layout
            st.markdown('<div class="results-grid">', unsafe_allow_html=True)

            # Column 1: Image Preview
            st.markdown('<div class="image-preview">', unsafe_allow_html=True)
            st.image(image, use_column_width=True, caption="Your Plant Photo")
            st.markdown('</div>', unsafe_allow_html=True)

            # Column 2: Analysis Results
            with st.spinner('🔍 Analyzing your plant with AI...'):
                # Analyze the image
                health_status, confidence = analyze_image(image)

                # Render results
                st.markdown('<div class="analysis-results">', unsafe_allow_html=True)
                render_results(health_status, confidence)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.markdown("""
                <div class="error-container">
                    <h4 class="error-title">⚠️ Image Processing Error</h4>
                    <p class="error-message">Error processing image: {}</p>
                    <p class="error-message">File info: {}</p>
                                         <p class="error-message">Try using the diagnostics tool below to troubleshoot the issue.</p>
                     <p class="error-help">Please try the following:</p>
                     <ul class="error-help-list" style="margin-left: 1.5rem; color: #7f1d1d; font-size: 0.9rem;">
                         <li>Make sure you're uploading a valid image file (JPG, JPEG, or PNG)</li>
                         <li>Try converting your image to JPG using an image editor</li>
                         <li>Check if the image can be opened on your device</li>
                         <li>Try a different image with smaller file size</li>
                     </ul>
                     <div style="margin-top: 1rem;">
                         <button id="diagnose-btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; border: none; padding: 10px 20px; border-radius: 8px; margin-top: 10px; cursor: pointer; font-weight: 600; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); transition: all 0.3s ease;">🔍 Run Image Diagnostics</button>
                     </div>
                </div>
            """.format(str(e), file_info), unsafe_allow_html=True)

            # Add diagnostics button functionality
            if st.button("🔍 Run Image Diagnostics", key="run_diagnostics"):
                st.markdown("### Image Diagnostics")
                st.markdown("Running comprehensive diagnostics on your image to identify the problem...")

                # Run diagnostics
                if uploaded_file:
                    uploaded_file.seek(0)
                    diagnostic_results = diagnose_image(uploaded_file)

                    # Display diagnostic info
                    st.markdown(f"**Format detected:** {diagnostic_results.get('format', 'Unknown')}")
                    st.markdown(f"**File size:** {diagnostic_results.get('size_bytes', 0) / 1024:.1f} KB")

                    if diagnostic_results.get('dimensions'):
                        st.markdown(f"**Dimensions:** {diagnostic_results.get('dimensions')[0]} x {diagnostic_results.get('dimensions')[1]} pixels")

                    # Show issues
                    if diagnostic_results.get('issues'):
                        st.markdown("#### Issues Found:")
                        for issue in diagnostic_results.get('issues'):
                            st.markdown(f"- {issue}")

                    # Show suggestions
                    if diagnostic_results.get('suggestions'):
                        st.markdown("#### Suggestions:")
                        for suggestion in diagnostic_results.get('suggestions'):
                            st.markdown(f"- {suggestion}")

                    # Try repair if needed
                    if not diagnostic_results.get('valid'):
                        st.markdown("#### Attempting to repair image...")
                        uploaded_file.seek(0)
                        repaired_image = repair_image(uploaded_file)

                        if repaired_image:
                            st.markdown("✅ Image successfully repaired! You can now proceed with analysis.")
                            st.image(repaired_image, caption="Repaired Image", width=300)

                            # Analyze repaired image
                            with st.spinner('🔍 Analyzing your plant with AI...'):
                                health_status, confidence = analyze_image(repaired_image)

                                # Render results
                                st.markdown('<div class="analysis-results">', unsafe_allow_html=True)
                                render_results(health_status, confidence)
                                st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.error("Could not repair the image. Please try a different image file.")

    # Add a call-to-action when no file is uploaded
    else:
        st.markdown("""
            <div style="text-align: center; padding: 3rem; color: #64748b;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📱</div>
                <h3 style="color: #1e40af; margin-bottom: 1rem;">Ready to analyze your plant?</h3>
                <p style="font-size: 1.1rem; max-width: 500px; margin: 0 auto;">
                    Upload a photo above to get started with your plant health analysis.
                </p>
                <div style="margin-top: 2rem;">
                    <button onclick="javascript:void(0)" style="background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); color: #1e40af; border: 2px solid #7dd3fc; border-radius: 12px; padding: 1rem 2rem; cursor: pointer; font-weight: 600; box-shadow: 0 4px 12px rgba(30, 64, 175, 0.15); transition: all 0.3s ease;">🛠️ Having trouble with images?</button>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Add advanced diagnostics option
        st.markdown("""
            <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px solid #7dd3fc; border-radius: 16px; padding: 2rem; margin: 2rem 0; box-shadow: 0 10px 25px rgba(30, 64, 175, 0.1);">
                <h3 style="color: #1e40af; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🛠️</span>
                    <span>Advanced Image Diagnostics</span>
                </h3>
                <p style="color: #374151; margin-bottom: 1.5rem; line-height: 1.6;">
                    If you're experiencing issues with image uploads, this tool can help identify problems with your image files.
                    Upload an image below to run a comprehensive diagnostic test.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 Image Diagnostic Tool", expanded=True):
            diagnostic_image = run_image_diagnostic_test()

            if diagnostic_image is not None:
                # User selected a sample image, analyze it
                with st.spinner('🔍 Analyzing sample plant with AI...'):
                    health_status, confidence = analyze_image(diagnostic_image)

                    # Render results
                    st.markdown('<div class="analysis-results">', unsafe_allow_html=True)
                    render_results(health_status, confidence)
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
