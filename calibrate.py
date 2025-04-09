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
def main():
    st.title("Simple Streamlit App")

    # Call the checkbox handler function
    handle_checkbox()

# Run the app
if __name__ == "__main__":
    main()









