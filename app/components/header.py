"""Header component for the Smart Plant Care application."""
import streamlit as st

def render_header():
    """Render the application header."""
    st.markdown("""
        <div class="header">
            <div class="header-content">
                <div class="header-icon">
                    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 3C9.23858 3 7 5.23858 7 8C7 9.5 7.5 10.5 9 12C8.5 12.5 7 14.5 7 16C7 18.7614 9.23858 21 12 21C14.7614 21 17 18.7614 17 16C17 14.5 15.5 12.5 15 12C16.5 10.5 17 9.5 17 8C17 5.23858 14.7614 3 12 3Z" stroke="#2ecc71" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <h1 class="header-title">Plant Health Analysis</h1>
                <p class="header-description">Upload a photo of your plant and let our AI analyze its health status. Get instant insights and personalized care recommendations to help your plants thrive.</p>
            </div>
        </div>
    """, unsafe_allow_html=True) 