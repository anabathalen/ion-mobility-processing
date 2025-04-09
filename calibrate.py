import streamlit as st
import pandas as pd

# Store file in session state to persist it across interactions
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None

# Simple file upload test
def handle_file_upload():
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    
    if uploaded_file:
        st.session_state["uploaded_file"] = uploaded_file
        st.write("File uploaded successfully!")

    if st.session_state["uploaded_file"]:
        try:
            # Read CSV and display it
            df = pd.read_csv(st.session_state["uploaded_file"])
            st.write("Your data:")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    else:
        st.write("No file uploaded yet.")

# Main app code
st.title("CSV File Upload Example")
handle_file_upload()
