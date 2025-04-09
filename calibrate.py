import streamlit as st
import pandas as pd

# Function to handle file upload and display data
def handle_file_upload():
    # Allow the user to upload a CSV file
    uploaded_file = st.file_uploader("Upload your CSV file here:", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Show the uploaded data as a DataFrame for reference
        st.write("Your data:")
        st.dataframe(df)

# Main app code
st.title("CSV File Upload Example")

# Call the function to handle the file upload
handle_file_upload()
