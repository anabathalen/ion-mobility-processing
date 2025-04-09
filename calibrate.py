import streamlit as st

# Function to handle file upload and display content
def handle_file_upload():
    # Allow user to upload a text file
    uploaded_file = st.file_uploader("Upload a text file", type="txt")
    
    if uploaded_file is not None:
        # Read the contents of the uploaded file
        file_content = uploaded_file.read().decode("utf-8")
        
        # Display the content of the file
        st.write("File content:")
        st.text(file_content)

# Main app code
st.title("Text File Upload Example")

# Call the function to handle the file upload
handle_file_upload()





