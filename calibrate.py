import streamlit as st
import zipfile
import os
from io import BytesIO

def extract_zip(zip_file):
    """Extract the contents of the uploaded zip file."""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall("/tmp")  # Extract to temporary folder
        return zip_ref.namelist()  # Return list of file/folder names

def list_folders(zip_file):
    """List only the folder names from the zip file."""
    extracted_files = extract_zip(zip_file)
    folders = set()
    
    for file in extracted_files:
        folder_name = os.path.dirname(file)
        if folder_name:  # Ignore empty string (root files)
            folders.add(folder_name)
    
    return sorted(folders)

# Streamlit UI
st.title("Zip File Folder Extractor")

uploaded_zip = st.file_uploader("Upload a Zip file", type=["zip"])

if uploaded_zip is not None:
    # Use in-memory file
    zip_file = BytesIO(uploaded_zip.read())
    
    st.write("Extracting folders...")
    
    # Get the list of folders inside the zip
    folders = list_folders(zip_file)
    
    if folders:
        st.write("Folders inside the zip file:")
        for folder in folders:
            st.write(f"- {folder}")
    else:
        st.write("No folders found in the zip file.")




