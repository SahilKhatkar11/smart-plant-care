"""Sidebar component for the Smart Plant Care application."""
import streamlit as st

# Sidebar CSS as a single multi-line string
SIDEBAR_CSS = """
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%) !important;
    padding: 2rem 1.5rem !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* Reusable classes */
.sidebar-section {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: all 0.3s ease;
}

.sidebar-section:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
}

.sidebar-title {
    color: white;
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.sidebar-description {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

.step-item {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    transition: all 0.3s ease;
}

.step-item:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateX(4px);
}

.step-number {
    background: rgba(255, 255, 255, 0.9);
    color: #2563eb;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-size: 0.75rem;
    font-weight: 600;
    flex-shrink: 0;
}

.step-text {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.93rem;
    margin: 0;
    line-height: 1.5;
}

.developer-info {
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.89rem;
    margin: 0;
}

.github-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    text-decoration: none;
    color: white;
    font-size: 0.875rem;
    margin-top: 1rem;
    transition: all 0.3s ease;
}

.github-link:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

.github-link svg {
    transition: transform 0.3s ease;
}

.github-link:hover svg {
    transform: rotate(360deg);
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
            <div class="sidebar-section">
                <div class="sidebar-title">
                    <span aria-label="Plant" title="Plant">🌿</span>
                    <span>Smart Plant Care</span>
                </div>
                <p class="sidebar-description">
                    Upload a photo of your plant to check its health status and get personalized care recommendations.
                </p>
            </div>
            """, unsafe_allow_html=True
        )

        # How It Works section
        st.markdown(
            """
            <div class="sidebar-section">
                <div class="sidebar-title">
                    <span aria-label="Magnifier" title="How It Works">🔍</span>
                    <span>How It Works</span>
                </div>
            """, unsafe_allow_html=True
        )

        steps = [
            "Upload a clear photo of your plant showing any concerning areas.",
            "Our advanced AI analyzes the image for health indicators.",
            "Get a detailed health assessment with personalized recommendations.",
        ]
        # Render steps
        step_html = ""
        for i, step in enumerate(steps, 1):
            step_html += f"""
            <div class="step-item">
                <span class="step-number">{i}</span>
                <p class="step-text">{step}</p>
            </div>
            """
        st.markdown(step_html + "</div>", unsafe_allow_html=True)

        # Developer / Github section
        st.markdown(
            """
            <div class="sidebar-section">
                <div class="sidebar-title">
                    <span aria-label="Developer" title="Developer">👨‍💻</span>
                    <span>Developer</span>
                </div>
                <p class="developer-info">Created by Sahil Khatkar<br>Microsoft AI & Azure Intern</p>
                <a href="https://github.com/yourusername" target="_blank" rel="noopener" class="github-link">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                        <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z"/>
                    </svg>
                    <span>View on GitHub</span>
                </a>
            </div>
            """, unsafe_allow_html=True
        )

# Example call for Streamlit apps:
# render_sidebar()
