import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
import io

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Fit Gaussians to Data", "Calibrate"])

# Check if the page has changed, to ensure no redundant loading
if "page" not in st.session_state or st.session_state["page"] != page:
    st.session_state.clear()  # Clear session state for fresh start

# Store the current page in session state
st.session_state["page"] = page

# Home Page
if page == "Home":
    st.title("👩🏻‍🔬 Barran Group IM-MS Processing Tools")
    st.subheader("←←← Navigate to the tool you need from the sidebar.")

# Fit Gaussians to Data Page
elif page == "Fit Gaussians to Data":
    st.title("Fit Gaussians to Data")
    
    # Gaussian function definition
    def gaussian(x, amp, mean, stddev):
        return amp * np.exp(-(x - mean)**2 / (2 * stddev**2))

    # Function to find local maxima
    def find_major_local_maxima(x, y, window_size=5, intensity_threshold=0.1):
        maxima_indices = []
        max_intensity = max(y)
        for i in range(window_size, len(y) - window_size):
            if y[i] == max(y[i - window_size:i + window_size + 1]) and y[i] >= intensity_threshold * max_intensity:
                maxima_indices.append(i)
        return maxima_indices

    # Function to upload and plot
    def upload_and_plot():
        # Allow the user to upload a CSV file
        uploaded_file = st.file_uploader("Upload your csv file here:", type="csv")
        
        if uploaded_file is not None:
            
            # Read the CSV into a pandas DataFrame
            df = pd.read_csv(uploaded_file)
            
            # Show the uploaded data as a DataFrame for reference
            st.write("Your data:")
            st.dataframe(df)
            
            # Check if the DataFrame contains 'x' and 'y' columns
            if 'x' in df.columns and 'y' in df.columns:
                # Find and label major local maxima
                maxima_indices = find_major_local_maxima(df['x'], df['y'])
                maxima_x = df['x'].iloc[maxima_indices]
                maxima_y = df['y'].iloc[maxima_indices]

                # Plot the raw data with labeled major maxima
                fig, ax = plt.subplots()
                ax.plot(df['x'], df['y'], label='Data', color='black', alpha=1.0, linewidth=1)  # Data as line
                ax.scatter(maxima_x, maxima_y, color='red', label='Major Local Maxima', zorder=5)

                # Annotate the major local maxima with x values
                for i, x_val in enumerate(maxima_x):
                    y_val = maxima_y.iloc[i]
                    offset = 10
                    if x_val < min(df['x']) + 0.1 * (max(df['x']) - min(df['x'])):
                        offset = -10
                    elif x_val > max(df['x']) - 0.1 * (max(df['x']) - min(df['x'])):
                        offset = -10
                    ax.annotate(f'{x_val:.2f}', (x_val, y_val), textcoords="offset points", xytext=(0, offset), ha='center')

                ax.set_xlabel("Drift Time (Bins)")
                ax.set_ylabel("Intensity")
                ax.legend()
                st.pyplot(fig)

                # Ask for initial guesses for the Gaussian means (peak x-values)
                st.write("Now that the major maxima have been identified, please input the number of Gaussian peaks and their positions.")
                num_gaussians = st.number_input("How many Gaussians would you like to fit to the data?", min_value=1, max_value=10, value=1)

                peaks = []
                for i in range(num_gaussians):
                    peak_guess = st.number_input(f"Enter the initial guess for the {i+1}th peak (mean of Gaussian {i+1}):", value=float(df['x'].median()))
                    peaks.append(peak_guess)

                if st.button("Generate Plot and Fit Gaussians"):
                    x_data = df['x']
                    y_data = df['y']

                    initial_guess = []
                    for peak in peaks:
                        initial_guess += [max(y_data), peak, 100]

                    def multi_gaussian(x, *params):
                        result = np.zeros_like(x)
                        for i in range(num_gaussians):
                            amp, mean, stddev = params[3*i:3*(i+1)]
                            result += gaussian(x, amp, mean, stddev)
                        return result

                    fig, ax = plt.subplots()
                    ax.plot(df['x'], df['y'], label='Data', color='black', alpha=1.0, linewidth=1)

                    colors = sns.color_palette("Set1", n_colors=num_gaussians)
                    x_full = np.linspace(min(x_data), max(x_data), 1000)

                    for i, peak in enumerate(peaks):
                        x_range_min = peak - peak*0.05
                        x_range_max = peak + peak*0.05

                        mask = (x_data >= x_range_min) & (x_data <= x_range_max)
                        x_local = x_data[mask]
                        y_local = y_data[mask]

                        if len(x_local) < 3:
                            continue

                        local_guess = [max(y_local), peak, 1]
                        try:
                            popt, _ = curve_fit(gaussian, x_local, y_local, p0=local_guess)
                            amp, mean, stddev = popt
                            y_fit = gaussian(x_full, amp, mean, stddev)
                            ax.fill_between(x_full, y_fit, color=colors[i], alpha=0.3, label=f'mean = {mean:.2f}')
                        except Exception as e:
                            continue

                    ax.set_xlabel("Drift Time (Bins)")
                    ax.set_ylabel("Intensity")
                    ax.legend()
                    st.pyplot(fig)

            else:
                st.error("CSV file must contain 'x' and 'y' columns.")
        
    upload_and_plot()

# Calibrate Page
elif page == "Calibrate":
    st.title("Calibrate")
    
    # Simple file upload test for calibration
    def handle_file_upload():
        uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
        
        if uploaded_file:
            st.session_state["uploaded_file"] = uploaded_file
            st.write("File uploaded successfully!")

        if st.session_state.get("uploaded_file"):
            try:
                # Read CSV and display it
                df = pd.read_csv(st.session_state["uploaded_file"])
                st.write("Your data:")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error reading the file: {e}")
        else:
            st.write("No file uploaded yet.")
    
    handle_file_upload()

