"""Results component for the Smart Plant Care application."""
import streamlit as st

def get_care_suggestions(health_status):
    """Get care suggestions based on plant health status."""
    if health_status:
        return [
            {"icon": "💧", "text": "Maintain the current watering schedule - your plant's hydration is optimal", "color": "#059669"},
            {"icon": "☀️", "text": "Continue providing the same amount of light exposure", "color": "#f59e0b"},
            {"icon": "✂️", "text": "Regular pruning will help maintain the plant's healthy growth pattern", "color": "#059669"},
            {"icon": "🌡️", "text": "Current temperature conditions are suitable for your plant", "color": "#3b82f6"},
            {"icon": "🌱", "text": "Consider a balanced fertilizer every 2-3 months to sustain growth", "color": "#059669"}
        ]
    else:
        return [
            {"icon": "💧", "text": "Adjust watering frequency - check soil moisture before each watering", "color": "#dc2626"},
            {"icon": "🌡️", "text": "Monitor temperature and humidity levels in the plant's environment", "color": "#dc2626"},
            {"icon": "🦠", "text": "Inspect leaves and stems carefully for signs of pests or disease", "color": "#dc2626"},
            {"icon": "🌿", "text": "Remove affected leaves and consider treating with appropriate plant care products", "color": "#dc2626"},
            {"icon": "📝", "text": "Test soil pH and nutrient levels to ensure optimal growing conditions", "color": "#dc2626"}
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
                gap: 1.5rem;
                margin-bottom: 2rem;
                padding: 2rem;
                background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
                border: 2px solid #e1effe;
                border-radius: 16px;
                transition: all 0.4s ease;
                position: relative;
                overflow: hidden;
            }
            
            .status-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.05), transparent);
                transition: left 0.8s ease;
            }
            
            .status-header:hover::before {
                left: 100%;
            }
            
            .status-header:hover {
                transform: translateY(-4px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            }
            
            .status-icon {
                width: 4rem;
                height: 4rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                border-radius: 50%;
                flex-shrink: 0;
                transition: all 0.4s ease;
                position: relative;
                overflow: hidden;
            }
            
            .status-icon::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                transform: translateX(-100%);
                transition: transform 0.6s ease;
            }
            
            .status-icon:hover::before {
                transform: translateX(100%);
            }
            
            .status-icon.healthy {
                background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
                color: #059669;
                border: 3px solid #86efac;
                box-shadow: 0 8px 25px rgba(5, 150, 105, 0.2);
            }
            
            .status-icon.unhealthy {
                background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
                color: #dc2626;
                border: 3px solid #fca5a5;
                box-shadow: 0 8px 25px rgba(220, 38, 38, 0.2);
            }
            
            .status-content h2 {
                font-size: 1.75rem;
                font-weight: 700;
                color: #1e40af;
                margin: 0 0 0.75rem 0;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .status-content p {
                font-size: 1.1rem;
                color: #64748b;
                margin: 0;
                line-height: 1.6;
            }
            
            .confidence-meter {
                display: flex;
                align-items: center;
                gap: 1.5rem;
                margin-bottom: 2.5rem;
                padding: 1.5rem;
                background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
                border: 2px solid #e1effe;
                border-radius: 16px;
                transition: all 0.4s ease;
                position: relative;
                overflow: hidden;
            }
            
            .confidence-meter::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.03), transparent);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .confidence-meter:hover::before {
                opacity: 1;
            }
            
            .confidence-meter:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }
            
            .confidence-label {
                font-size: 1rem;
                font-weight: 600;
                color: #374151;
                min-width: 8rem;
            }
            
            .confidence-bar {
                flex-grow: 1;
                height: 0.75rem;
                background: #e1effe;
                border-radius: 9999px;
                overflow: hidden;
                border: 2px solid #bfdbfe;
                position: relative;
            }
            
            .confidence-bar-fill {
                height: 100%;
                border-radius: 9999px;
                transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            
            .confidence-bar-fill::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                animation: shimmer 2s infinite;
            }
            
            @keyframes shimmer {
                0% { left: -100%; }
                100% { left: 100%; }
            }
            
            .confidence-bar-fill.healthy {
                background: linear-gradient(90deg, #059669 0%, #34d399 50%, #6ee7b7 100%);
            }
            
            .confidence-bar-fill.unhealthy {
                background: linear-gradient(90deg, #dc2626 0%, #f87171 50%, #fca5a5 100%);
            }
            
            .confidence-value {
                font-size: 1.25rem;
                font-weight: 700;
                color: #1e40af;
                min-width: 5rem;
                text-align: right;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            }
            
            .recommendations-title {
                font-size: 1.5rem;
                font-weight: 700;
                color: #1e40af;
                margin: 0 0 1.5rem 0;
                display: flex;
                align-items: center;
                gap: 1rem;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .recommendations-list {
                display: flex;
                flex-direction: column;
                gap: 1.25rem;
            }
            
            .recommendation-item {
                display: flex;
                align-items: flex-start;
                gap: 1.25rem;
                padding: 1.5rem;
                background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
                border: 2px solid #e1effe;
                border-radius: 16px;
                transition: all 0.4s ease;
                position: relative;
                overflow: hidden;
            }
            
            .recommendation-item::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.05), transparent);
                transition: left 0.6s ease;
            }
            
            .recommendation-item:hover::before {
                left: 100%;
            }
            
            .recommendation-item:hover {
                transform: translateX(8px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            }
            
            .recommendation-icon {
                width: 3rem;
                height: 3rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                border-radius: 50%;
                flex-shrink: 0;
                transition: all 0.4s ease;
                position: relative;
                overflow: hidden;
            }
            
            .recommendation-icon::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.4), transparent);
                transform: translateX(-100%);
                transition: transform 0.6s ease;
            }
            
            .recommendation-item:hover .recommendation-icon::before {
                transform: translateX(100%);
            }
            
            .recommendation-item:hover .recommendation-icon {
                transform: scale(1.1);
            }
            
            .recommendation-text {
                font-size: 1.05rem;
                color: #374151;
                line-height: 1.6;
                margin: 0;
                padding: 0.5rem 0;
                font-weight: 500;
            }
            
            /* Animation classes */
            .fade-in-up {
                animation: fadeInUp 0.8s ease-out;
            }
            
            .slide-in-right {
                animation: slideInRight 0.8s ease-out;
            }
            
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
            
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(30px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        </style>
    """, unsafe_allow_html=True)
    
    try:
        # Status header
        icon = "🌿" if health_status else "⚠️"
        status_text = "Healthy" if health_status else "Needs Attention"
        status_desc = (
            "Your plant appears to be in excellent health! Keep up the great care routine." 
            if health_status 
            else "Your plant might need some attention. Here are some recommendations to help it thrive."
        )
        
        st.markdown(f"""
            <div class="status-header fade-in-up">
                <div class="status-icon {'healthy' if health_status else 'unhealthy'}">{icon}</div>
                <div class="status-content">
                    <h2>Plant Status: {status_text}</h2>
                    <p>{status_desc}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Confidence meter
        st.markdown(f"""
            <div class="confidence-meter slide-in-right">
                <span class="confidence-label">AI Confidence:</span>
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
            <h3 class="recommendations-title fade-in-up">
                <span>💡</span>
                <span>Care Recommendations</span>
            </h3>
            <div class="recommendations-list">
        """, unsafe_allow_html=True)
        
        suggestions = get_care_suggestions(health_status)
        for i, suggestion in enumerate(suggestions):
            delay = i * 0.1
            st.markdown(f"""
                <div class="recommendation-item slide-in-right" style="animation-delay: {delay}s;">
                    <div class="recommendation-icon" style="background: linear-gradient(135deg, {suggestion['color']}20 0%, {suggestion['color']}10 100%); border: 2px solid {suggestion['color']}40; color: {suggestion['color']};">
                        {suggestion['icon']}
                    </div>
                    <p class="recommendation-text">{suggestion['text']}</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Additional tips section
        st.markdown("""
            <div style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-radius: 16px; border: 2px solid #bfdbfe;">
                <h4 style="color: #1e40af; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                    <span>💡</span>
                    <span>Pro Tip</span>
                </h4>
                <p style="color: #374151; margin: 0; line-height: 1.6;">
                    For the most accurate analysis, take photos in natural lighting and include both healthy and concerning areas of your plant. 
                    Regular monitoring helps catch issues early!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}") 