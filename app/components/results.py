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
    if health_status is None or confidence is None:
        st.error("Could not analyze the image. Please try uploading a different photo.")
        return

    st.markdown("""
        <style>
            .status-header {
                display: flex;
                align-items: center;
                gap: 1.25rem;
                margin-bottom: 1.5rem;
                padding: 1.5rem;
                background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
                border: 2px solid #e1effe;
                border-radius: 12px;
                transition: all 0.3s ease;
            }
            
            .status-header:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 118, 255, 0.15);
            }
            
            .status-icon {
                width: 3rem;
                height: 3rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                border-radius: 50%;
                flex-shrink: 0;
                transition: all 0.3s ease;
            }
            
            .status-icon.healthy {
                background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
                color: #059669;
                border: 2px solid #86efac;
            }
            
            .status-icon.unhealthy {
                background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
                color: #dc2626;
                border: 2px solid #fca5a5;
            }
            
            .status-content h2 {
                font-size: 1.5rem;
                font-weight: 700;
                color: #1e40af;
                margin: 0 0 0.5rem 0;
            }
            
            .status-content p {
                font-size: 1rem;
                color: #3b82f6;
                margin: 0;
                line-height: 1.5;
            }
            
            .confidence-meter {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 2rem;
                padding: 1.25rem;
                background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
                border: 2px solid #e1effe;
                border-radius: 12px;
                transition: all 0.3s ease;
            }
            
            .confidence-meter:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 118, 255, 0.15);
            }
            
            .confidence-bar {
                flex-grow: 1;
                height: 0.5rem;
                background: #e1effe;
                border-radius: 9999px;
                overflow: hidden;
                border: 2px solid #bfdbfe;
            }
            
            .confidence-bar-fill {
                height: 100%;
                border-radius: 9999px;
                transition: width 1s ease;
            }
            
            .confidence-bar-fill.healthy {
                background: linear-gradient(90deg, #059669 0%, #34d399 100%);
            }
            
            .confidence-bar-fill.unhealthy {
                background: linear-gradient(90deg, #dc2626 0%, #f87171 100%);
            }
            
            .confidence-value {
                font-size: 1.125rem;
                font-weight: 600;
                color: #1e40af;
                min-width: 4rem;
                text-align: right;
            }
            
            .recommendations-title {
                font-size: 1.25rem;
                font-weight: 700;
                color: #1e40af;
                margin: 0 0 1.25rem 0;
                display: flex;
                align-items: center;
                gap: 0.75rem;
            }
            
            .recommendations-list {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            
            .recommendation-item {
                display: flex;
                align-items: flex-start;
                gap: 1rem;
                padding: 1.25rem;
                background: linear-gradient(135deg, #f0f9ff 0%, #ffffff 100%);
                border: 2px solid #e1effe;
                border-radius: 12px;
                transition: all 0.3s ease;
            }
            
            .recommendation-item:hover {
                transform: translateX(4px);
                box-shadow: 0 6px 20px rgba(0, 118, 255, 0.15);
            }
            
            .recommendation-icon {
                width: 2.5rem;
                height: 2.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.25rem;
                background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
                border: 2px solid #86efac;
                border-radius: 50%;
                flex-shrink: 0;
            }
            
            .recommendation-text {
                font-size: 1rem;
                color: #3b82f6;
                line-height: 1.6;
                margin: 0;
                padding: 0.25rem 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    try:
        # Status header
        icon = "🌿" if health_status else "⚠️"
        status_text = "Healthy" if health_status else "Needs Attention"
        status_desc = (
            "Your plant appears to be in good health. Keep up the great care!" 
            if health_status 
            else "Your plant might need some attention. Here are some recommendations to help."
        )
        
        st.markdown(f"""
            <div class="status-header">
                <div class="status-icon {'healthy' if health_status else 'unhealthy'}">{icon}</div>
                <div class="status-content">
                    <h2>Plant Status: {status_text}</h2>
                    <p>{status_desc}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Confidence meter
        st.markdown(f"""
            <div class="confidence-meter">
                <div class="confidence-bar">
                    <div 
                        class="confidence-bar-fill {'healthy' if health_status else 'unhealthy'}" 
                        style="width: {confidence * 100}%">
                    </div>
                </div>
                <span class="confidence-value">{confidence:.1%}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Care recommendations
        st.markdown("""
            <h3 class="recommendations-title">
                <span>💡</span>
                <span>Care Recommendations</span>
            </h3>
            <div class="recommendations-list">
        """, unsafe_allow_html=True)
        
        suggestions = get_care_suggestions(health_status)
        for suggestion in suggestions:
            st.markdown(f"""
                <div class="recommendation-item">
                    <div class="recommendation-icon">{suggestion['icon']}</div>
                    <p class="recommendation-text">{suggestion['text']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}") 