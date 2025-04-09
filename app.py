import streamlit as st

# Set page config
st.set_page_config(page_title="Ion Mobility Data Processing", page_icon="🧪", layout="wide")

# Sidebar navigation
page = st.sidebar.selectbox("Navigate to", ["Home", "Gaussian Fit"])

# Home page content
if page == "Home":
    st.title("Welcome to the Ion Mobility Processing Tool")
    st.markdown("""
    Use the sidebar to navigate between:
    - 🌋 Gaussian Fitting
    """)
  
elif page == "Gaussian Fit":
    st.title("Gaussian Fitting Tool")
    # Your Gaussian fitting code (from before)
    import pages/1_Gaussian_Fit.py  # You can just import the page's code
