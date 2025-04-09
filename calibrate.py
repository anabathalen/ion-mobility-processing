import streamlit as st

# Define the function to show the checkbox
def show_checkbox():
    # Create a checkbox and store its state
    if st.checkbox("Try me"):
        st.write("Working")
    else:
        st.write("Please try me!")

# Main code execution
st.title("Simple Streamlit App")

# Call the function to show the checkbox
show_checkbox()








