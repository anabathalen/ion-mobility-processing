import streamlit as st

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload CSV"])

# Home Page
if page == "Home":
    st.title("IM-MS Processing Tools")
    st.write("<-- Use the sidebar to navigate to the tool you need.")

# Upload CSV Page (handles the file upload)
elif page == "Fit Gaussians to Data":
    st.title("Fit Gaussians to Data")
    
    import upload_plot  # This will bring in the CSV upload functionality from upload_plot.py
    upload_plot.upload_and_plot()
