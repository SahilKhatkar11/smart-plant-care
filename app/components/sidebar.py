"""Sidebar component for the Smart Plant Care application."""
import streamlit as st

# Sidebar CSS as a single multi-line string
SIDEBAR_CSS = """
<style>
/* Sidebar container */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #3b82f6 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.1);
    transition: all 0.4s ease;
}

[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 50%, #3b82f6 100%) !important;
    padding: 2rem 1.5rem !important;
}

[data-testid="stSidebarNav"] { display: none; }



/* Reusable classes */
.sidebar-section {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.75rem;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.sidebar-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.6s ease;
}

.sidebar-section:hover::before {
    left: 100%;
}

.sidebar-section:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.sidebar-title {
    color: white;
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.sidebar-description {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    font-weight: 400;
}

.step-item {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.step-item::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.6s ease;
}

.step-item:hover::before {
    left: 100%;
}

.step-item:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateX(6px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.step-number {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.8) 100%);
    color: #2563eb;
    width: 28px;
    height: 28px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 0.8rem;
    font-weight: 700;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.step-item:hover .step-number {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.step-text {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.93rem;
    margin: 0;
    line-height: 1.5;
    font-weight: 400;
}

.developer-info {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.89rem;
    margin: 0;
    line-height: 1.5;
}

.github-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1.25rem;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    text-decoration: none;
    color: white;
    font-size: 0.875rem;
    font-weight: 500;
    margin-top: 1.5rem;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}

.github-link::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    transition: left 0.6s ease;
}

.github-link:hover::before {
    left: 100%;
}

.github-link:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.github-link svg {
    transition: transform 0.4s ease;
    width: 20px;
    height: 20px;
}

.github-link:hover svg {
    transform: rotate(360deg) scale(1.1);
}

/* Quick stats section */
.quick-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.stat-item {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-item:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}

.stat-number {
    font-size: 1.5rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.25rem;
}

.stat-label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.8);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Animation classes */
.fade-in-up {
    animation: fadeInUp 0.8s ease-out;
}

.slide-in-left {
    animation: slideInLeft 0.8s ease-out;
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

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-30px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .sidebar-section {
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    .step-item {
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    
    .github-link {
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .quick-stats {
        grid-template-columns: 1fr;
    }
}
</style>
"""

def render_sidebar():
    """Render the upgraded application sidebar."""
    st.markdown(SIDEBAR_CSS, unsafe_allow_html=True)
    
    with st.sidebar:
        # Brand section
        st.markdown(
            """
            <div class="sidebar-section fade-in-up">
                <div class="sidebar-title">
                    <span aria-label="Plant" title="Plant" style="font-size: 1.5rem;">🌿</span>
                    <span>Smart Plant Care</span>
                </div>
                <p class="sidebar-description">
                    Upload a photo of your plant to check its health status and get personalized care recommendations powered by advanced AI.
                </p>
            </div>
            """, unsafe_allow_html=True
        )

        # Quick stats section
        st.markdown(
            """
            <div class="sidebar-section slide-in-left">
                <div class="sidebar-title">
                    <span aria-label="Stats" title="Quick Stats" style="font-size: 1.25rem;">📊</span>
                    <span>Quick Stats</span>
                </div>
                <div class="quick-stats">
                    <div class="stat-item">
                        <div class="stat-number">99%</div>
                        <div class="stat-label">Accuracy</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">2s</div>
                        <div class="stat-label">Analysis Time</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )

        # How It Works section
        st.markdown(
            """
            <div class="sidebar-section slide-in-left">
                <div class="sidebar-title">
                    <span aria-label="Magnifier" title="How It Works" style="font-size: 1.25rem;">🔍</span>
                    <span>How It Works</span>
                </div>
            """, unsafe_allow_html=True
        )

        steps = [
            "Upload a clear photo of your plant showing any concerning areas.",
            "Our advanced AI analyzes the image for health indicators and patterns.",
            "Get a detailed health assessment with personalized care recommendations.",
        ]
        # Render steps
        step_html = ""
        for i, step in enumerate(steps, 1):
            step_html += f"""
            <div class="step-item" style="animation-delay: {i * 0.1}s;">
                <span class="step-number">{i}</span>
                <p class="step-text">{step}</p>
            </div>
            """
        st.markdown(step_html + "</div>", unsafe_allow_html=True)

        # Developer / Github section
        st.markdown(
            """
            <div class="sidebar-section fade-in-up">
                <div class="sidebar-title">
                    <span aria-label="Developer" title="Developer" style="font-size: 1.25rem;">👨‍💻</span>
                    <span>Developer</span>
                </div>
                <p class="developer-info">Created by Sahil Khatkar<br>Microsoft AI & Azure Intern</p>
                <a href="https://github.com/yourusername" target="_blank" rel="noopener" class="github-link">
                    <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                        <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z"/>
                    </svg>
                    <span>View on GitHub</span>
                </a>
            </div>
            """, unsafe_allow_html=True
        )

def render_sidebar_toggle():
    """Render the sidebar toggle button using Streamlit components."""
    # Initialize sidebar state in session state
    if 'sidebar_visible' not in st.session_state:
        st.session_state.sidebar_visible = True
    
    # Create a container for the toggle button
    with st.container():
        # Use columns to position the button
        col1, col2, col3 = st.columns([1, 20, 1])
        with col1:
            if st.button("◀" if st.session_state.sidebar_visible else "▶", 
                        help="Toggle Sidebar", 
                        key="sidebar_toggle"):
                st.session_state.sidebar_visible = not st.session_state.sidebar_visible
    
    # Add CSS to style the toggle button
    st.markdown("""
        <style>
        /* Style the toggle button */
        [data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
            border: none !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            color: white !important;
            font-size: 1.25rem !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
            transition: all 0.3s ease !important;
            margin: 10px 0 !important;
        }
        
        [data-testid="baseButton-secondary"]:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
        }
        
        /* Hide sidebar when toggled off */
        .sidebar-hidden [data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Adjust main content when sidebar is hidden */
        .sidebar-hidden .main .block-container {
            margin-left: 0 !important;
            max-width: 1400px !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Example call for Streamlit apps:
# render_sidebar()
# render_sidebar_toggle()
