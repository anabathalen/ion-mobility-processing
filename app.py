import streamlit as st

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload CSV"])

# Home Page
if page == "Home":
    st.title("Welcome to the Home Page!")
    st.write("This is your main page. You can navigate to the 'Plot' or 'Upload CSV' page from the sidebar.")

# Upload CSV Page (handles the file upload)
elif page == "Upload CSV":
    st.title("Upload CSV and Plot")
    st.write("Upload your x, y CSV file to generate a plot.")
    
    import upload_plot  # This will bring in the CSV upload functionality from upload_plot.py
    upload_plot.upload_and_plot()
