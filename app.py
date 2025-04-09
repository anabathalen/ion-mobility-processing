import streamlit as st

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload CSV"])

# Home Page
if page == "Home":
    st.title("👩🏻‍🔬 Barran Group IM-MS Processing Tools")
    st.subheader("←←← Navigate to the tool you need from the sidebar.")

# Upload CSV Page (handles the file upload)
elif page == "Upload CSV":
    st.title("Upload CSV and Plot")
    st.write("Upload your x, y CSV file to generate a plot.")
    
    import upload_plot  # This will bring in the CSV upload functionality from upload_plot.py
    upload_plot.upload_and_plot()
