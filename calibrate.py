import streamlit as st

# Step 1: Ask for the first calibrant name
st.title("Calibrant Charge State File Upload")
calibrant_name = st.text_input("Enter the name of the first calibrant:")

# If a calibrant name is provided, ask to upload the charge state files
if calibrant_name:
    st.write(f"Processing files for calibrant: {calibrant_name}")
    
    # Step 2: File uploader for multiple files (drag-and-drop)
    charge_state_files = st.file_uploader(
        "Upload Charge State Files for this calibrant",
        type=["txt", "csv", "dat"],  # Assuming charge state files are of these types
        accept_multiple_files=True
    )

    if charge_state_files:
        # Step 3: Process the uploaded charge state files
        st.write(f"Processing {len(charge_state_files)} files...")

        # (Optional) Here you would include your fitting logic:
        # For now, we are just displaying the names of the uploaded files
        for uploaded_file in charge_state_files:
            st.write(f"- {uploaded_file.name}")
        
        # After fitting (if applicable), we could show a success message
        st.success(f"Successfully processed the charge state files for {calibrant_name}!")

        # Step 4: Ask if you want to upload for another calibrant
        next_calibrant = st.radio("Do you want to upload files for another calibrant?", ["Yes", "No"])

        if next_calibrant == "Yes":
            st.text_input("Enter the name of the next calibrant:")
        else:
            st.write("All files have been processed.")
    else:
        st.write("Please upload the charge state files for this calibrant.")
else:
    st.write("Please enter a calibrant name to start.")



