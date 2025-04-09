import streamlit as st

# Set page config
st.set_page_config(page_title="Ion Mobility Data Processing", page_icon="🧪", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Navigate to", ["Home", "Plot", "Upload Data", "Gaussian Fit"])

# Home page content
if page == "Home":
    st.title("Welcome to the Ion Mobility Processing Tool")
    st.markdown("""
    Use the sidebar to navigate between:
    - 📊 Plot
    - 📁 Upload Data
    - 🌋 Gaussian Fitting
    """)
  
elif page == "Gaussian Fit":
    st.title("Gaussian Fitting Tool")
    # Your Gaussian fitting code (from before)
