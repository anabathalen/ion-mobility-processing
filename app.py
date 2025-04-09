import streamlit as st

# Function to reset the page when switching
def reset_page():
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = None
    if st.session_state["current_page"] != st.session_state.get("page"):
        st.session_state.clear()
        st.session_state["current_page"] = st.session_state.get("page")
        st.rerun()  # Using st.rerun() instead of st.experimental_rerun()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Fit Gaussians to Data", "Calibrate"])

# Call reset_page when page changes
st.session_state["page"] = page
reset_page()

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

