import streamlit as st

# Use Streamlit's session state to store file content
if "file_content" not in st.session_state:
    st.session_state["file_content"] = None

# Function to handle file upload and display content
def handle_file_upload():
    uploaded_file = st.file_uploader("Upload a text file", type="txt")
    
    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.session_state["file_content"] = file_content  # Store in session state
            st.write("File content:")
            st.text(file_content)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    else:
        if st.session_state["file_content"]:
            st.write("Previous file content:")
            st.text(st.session_state["file_content"])

# Main app code
st.title("Text File Upload Example")

# Call the function to handle the file upload
handle_file_upload()
