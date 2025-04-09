import streamlit as st

# Function to handle checkbox logic
def handle_checkbox():
    # Create a checkbox and store its state
    checkbox_state = st.checkbox("Try me")
    
    # Based on checkbox state, show the appropriate message
    if checkbox_state:
        st.write("Working")
    else:
        st.write("Please try me!")

# Main app code
st.title("Simple Streamlit App")

# Call the checkbox handler function directly
handle_checkbox()








