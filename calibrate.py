import streamlit as st

# Streamlit UI
st.title("Simple Streamlit App")

# Create a checkbox and store its state
if st.checkbox("Try me"):
    st.write("Working")
else:
    st.write("Please try me!")






