import streamlit as st

# Function to clear session state
def reset_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Fit Gaussians to Data", "Calibrate"])

# Reset session state when a new page is selected
reset_session_state()

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
