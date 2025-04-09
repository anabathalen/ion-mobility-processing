import streamlit as st

# Sidebar with navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload CSV"])

# Home Page
if page == "Home":
    st.title("Welcome to the Home Page!")
    st.write("This is your main page. You can navigate to the 'Plot' or 'Upload CSV' page from the sidebar.")

# Upload CSV Page
elif page == "Upload CSV":
    st.title("Upload CSV and Plot")
    st.write("Upload your x, y CSV file to generate a plot.")
    # This will be handled by the upload_plot.py file
    import upload_plot  # Import the page to handle CSV upload
