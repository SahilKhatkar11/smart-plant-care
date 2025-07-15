"""Sidebar component for the Smart Plant Care application."""
import streamlit as st

def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        # App title section
        st.markdown('<div class="sidebar-title">', unsafe_allow_html=True)
        st.markdown("""
            <div class="title-content">
                <span style="font-size: 2.5rem;">🌿</span>
                <h1>Smart Plant Care</h1>
                <p>Upload a photo of your plant to check its health status and get personalized care recommendations.</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # How it works section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("""
            <div class="section-header">
                <span>🔍</span>
                <h3>How It Works</h3>
            </div>
            <div class="steps-list">
                <div class="step">
                    <span class="step-number">1</span>
                    <p>Upload a clear photo of your plant showing any concerning areas</p>
                </div>
                <div class="step">
                    <span class="step-number">2</span>
                    <p>Our advanced AI model analyzes the image for health indicators</p>
                </div>
                <div class="step">
                    <span class="step-number">3</span>
                    <p>Get detailed health assessment and personalized care recommendations</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Developer section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown("""
            <div class="section-header">
                <span>👨‍💻</span>
                <h3>Developer</h3>
            </div>
            <div class="section-content">
                <div class="dev-info">
                    <p class="dev-name">Created by Sahil Khatkar</p>
                    <p class="dev-role">Microsoft AI & Azure Intern</p>
                </div>
                <div style="margin-top: 1rem;">
                    <a href="https://github.com/yourusername" target="_blank" style="text-decoration: none; color: inherit;">
                        <div class="step" style="margin-top: 0.5rem;">
                            <span style="font-size: 1.2rem;">📦</span>
                            <p>View on GitHub</p>
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Version info
        st.markdown("""
            <div style="position: fixed; bottom: 0; left: 0; width: 100%; padding: 1rem; text-align: center; font-size: 0.8rem; color: #6c757d; background: linear-gradient(0deg, white 0%, rgba(255,255,255,0.9) 100%);">
                <p style="margin: 0;">v1.0.0 • Made with ❤️</p>
            </div>
        """, unsafe_allow_html=True)  