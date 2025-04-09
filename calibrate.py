import streamlit as st
import zipfile
import os
import tempfile

# Define the function to handle the ZIP file upload and extract folder names
def process_zip_and_list_folders(uploaded_zip):
    # Create a temporary directory to extract the ZIP contents
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Extract the ZIP file to the temporary directory
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        # List the folder names inside the extracted ZIP file
        folder_names = [folder for folder in os.listdir(tmpdirname) if os.path.isdir(os.path.join(tmpdirname, folder))]

        return folder_names

# Streamlit interface
st.write("### Upload a ZIP File and List Folder Names")
st.write("""
This tool allows you to upload a ZIP file. After uploading, the names of the folders inside the ZIP file will be displayed.
""")

# File uploader widget
uploaded_zip = st.file_uploader("Upload ZIP File", type=["zip"])

if uploaded_zip:
    # Show the uploaded ZIP file name immediately
    st.write(f"Uploaded file: {uploaded_zip.name}")

    # Execute the function to process the ZIP and list folder names
    folder_names = process_zip_and_list_folders(uploaded_zip)

    # Display the folder names
    if folder_names:
        st.write("### Found the following folders inside the ZIP file:")
        for folder in folder_names:
            st.write(folder)
    else:
        st.write("No folders were found in the ZIP file.")


