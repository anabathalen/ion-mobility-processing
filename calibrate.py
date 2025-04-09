import streamlit as st
import zipfile
import os
import tempfile

# Function to handle the ZIP file upload and extract folder names
def extract_zip_and_list_folders(uploaded_zip):
    try:
        # Create a temporary directory to extract the ZIP contents
        with tempfile.TemporaryDirectory() as tmpdirname:
            st.write(f"Temporary directory created: {tmpdirname}")  # Debug log

            # Extract the ZIP file to the temporary directory
            with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                st.write(f"Extracting ZIP file: {uploaded_zip.name}")  # Debug log
                zip_ref.extractall(tmpdirname)
                st.write("Extraction completed!")  # Debug log
            
            # List the folder names inside the extracted ZIP file
            folder_names = [folder for folder in os.listdir(tmpdirname) if os.path.isdir(os.path.join(tmpdirname, folder))]
            st.write(f"Folder names found: {folder_names}")  # Debug log

            if folder_names:
                return folder_names
            else:
                return "No folders were found inside the ZIP file."
    except Exception as e:
        return f"Error during extraction: {e}"

# Streamlit interface
st.title("ZIP File Folder Extractor")
st.write("Upload a ZIP file, and it will show the names of any folders inside it.")

# File uploader widget
uploaded_zip = st.file_uploader("Upload ZIP File", type=["zip"])

if uploaded_zip:
    st.write(f"Uploaded file: {uploaded_zip.name}")  # Debug log
    st.write(f"File size: {uploaded_zip.size / 1024:.2f} KB")  # Debug log

    # Step 1: Extract and process the ZIP file
    folder_names = extract_zip_and_list_folders(uploaded_zip)

    # Step 2: Check if folders were found or if there was an error
    if isinstance(folder_names, list):  # If folder names were successfully retrieved
        if folder_names:
            st.write("### Found the following folders inside the ZIP file:")
            for folder in folder_names:
                st.write(f"- {folder}")
        else:
            st.write("No folders were found inside the ZIP file.")
    else:  # If there was an error during extraction
        st.write(folder_names)  # Display the error message
else:
    st.write("Please upload a ZIP file to get started.")





