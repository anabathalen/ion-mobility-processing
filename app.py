import streamlit as st

# Function to clear session state
def clear_state_on_page_change():
    if "page" in st.session_state:
        # Check if the page has changed
        if st.session_state["page"] != st.session_state.get("current_page"):
            st.session_state.clear()  # Clear session state on page change
            st.session_state["current_page"] = st.session_state.get("page")  # Track the current page

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Fit Gaussians to Data", "Calibrate"])

# Store the page in session state
st.session_state["page"] = page

# Clear session state if the page changes
clear_state_on_page_change()

# Home Page
if page == "Home":
    st.title("👩🏻‍🔬 Barran Group IM-MS Processing Tools")
    st.subheader("←←← Navigate to the tool you need from the sidebar.")

# Fit Gaussians to Data Page
elif page == "Fit Gaussians to Data":
    st.title("Fit Gaussians to Data")
    import upload_plot  # Your specific tool import

# Calibrate Page
elif page == "Calibrate":
    st.title("Calibrate")
    import calibrate  # Your specific tool import


