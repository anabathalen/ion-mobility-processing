import streamlit as st

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Calibrate (IMSCal)", "Fit Gaussians to Data"])

# Home Page
if page == "Home":
    st.title("👩🏻‍🔬 Barran Group IM-MS Processing Tools")
    st.subheader("←←← Navigate to the tool you need from the sidebar.")

# Upload CSV Page (handles the file upload)
elif page == "Fit Gaussians to Data":
    st.title("Fit Gaussians to Data")
    
    import upload_plot  # This will bring in the CSV upload functionality from upload_plot.py
    
# Upload CSV Page (handles the file upload)
elif page == "Calibrate (IMSCal)":
    st.title("Calibrate (IMSCal)")
    
    import calibrate
