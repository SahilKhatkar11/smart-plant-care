"""Results component for the Smart Plant Care application."""
import streamlit as st

def get_care_suggestions(health_status):
    """Get care suggestions based on plant health status."""
    if health_status:
        return [
            {"icon": "💧", "text": "Maintain the current watering schedule - your plant's hydration is optimal"},
            {"icon": "☀️", "text": "Continue providing the same amount of light exposure"},
            {"icon": "✂️", "text": "Regular pruning will help maintain the plant's healthy growth pattern"},
            {"icon": "🌡️", "text": "Current temperature conditions are suitable for your plant"},
            {"icon": "🌱", "text": "Consider a balanced fertilizer every 2-3 months to sustain growth"}
        ]
    else:
        return [
            {"icon": "💧", "text": "Adjust watering frequency - check soil moisture before each watering"},
            {"icon": "🌡️", "text": "Monitor temperature and humidity levels in the plant's environment"},
            {"icon": "🦠", "text": "Inspect leaves and stems carefully for signs of pests or disease"},
            {"icon": "🌿", "text": "Remove affected leaves and consider treating with appropriate plant care products"},
            {"icon": "📝", "text": "Test soil pH and nutrient levels to ensure optimal growing conditions"}
        ]

def render_results(health_status, confidence):
    """Render the analysis results."""
    status_color = "healthy" if health_status else "unhealthy"
    st.markdown(f'<div class="results-box {status_color}">', unsafe_allow_html=True)
    
    # Results header
    st.markdown('<div class="results-header">', unsafe_allow_html=True)
    icon = "🌿" if health_status else "⚠️"
    status_text = "Healthy" if health_status else "Needs Attention"
    st.markdown(f'<span class="results-icon">{icon}</span>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="results-title">Plant Status: {status_text}</h2>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results content
    st.markdown('<div class="results-content">', unsafe_allow_html=True)
    
    # Confidence meter
    st.markdown(
        f'<div class="confidence-meter">'
        f'<span class="confidence-label">Analysis Confidence:</span>'
        f'<span class="confidence-value">{confidence:.1%}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Care suggestions
    st.markdown('<h3 style="color: #1a1a1a; margin-bottom: 1.5rem;">💡 Personalized Care Recommendations</h3>', unsafe_allow_html=True)
    suggestions = get_care_suggestions(health_status)
    for suggestion in suggestions:
        st.markdown(
            f'<div class="suggestion-item">'
            f'<span class="suggestion-icon">{suggestion["icon"]}</span>'
            f'<span class="suggestion-text">{suggestion["text"]}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) 