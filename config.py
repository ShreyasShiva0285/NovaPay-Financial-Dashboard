import streamlit as st

def setup_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="NovaPay Financial Dashboard",
        page_icon="💰",
        layout="wide"
    )

def add_custom_css():
    """Add custom CSS to the Streamlit app."""
    st.markdown("""
    <style>
        .main {
            padding-top: 0rem;
        }
        .title-container {
            background-color: #f5f7f9;
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 1rem;
        }
        .metric-card {
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .positive {
            color: green;
        }
        .negative {
            color: red;
        }
        .sidebar .sidebar-content {
            background-color: #f8fafc;
        }
        .form-container {
            background-color: white;
            padding: 1.5rem;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        .stExpander {
            border: none !important;
            box-shadow: 0 0 5px rgba(0,0,0,0.05);
        }
    </style>
    """, unsafe_allow_html=True)
