import streamlit as st

# Streamlit UI
st.title("Simple Streamlit App")

# Create a checkbox and store its state
user_input = st.checkbox("Try me")

# Check if the checkbox is ticked
if user_input:
    st.write("Working")
else:
    st.write("Please try me!")







