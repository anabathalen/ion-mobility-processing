import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import find_peaks

# Define the Gaussian function
def gaussian(x, amp, mean, stddev):
    return amp * np.exp(-(x - mean)**2 / (2 * stddev**2))

def upload_and_plot():
    # Allow the user to upload a CSV file
    uploaded_file = st.file_uploader("Upload your x, y CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Show the uploaded data as a DataFrame for reference
        st.write("Here is the data you uploaded:")
        st.dataframe(df)
        
        # Check if the DataFrame contains 'x' and 'y' columns
        if 'x' in df.columns and 'y' in df.columns:
            # Plot the raw data
            st.subheader("Raw Data Plot")
            fig, ax = plt.subplots()
            ax.plot(df['x'], df['y'], label='Data', marker='o', linestyle='-', color='blue')
            ax.set_title("Data")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            st.pyplot(fig)

            # Identify local maxima using scipy.signal.find_peaks
            peaks, _ = find_peaks(df['y'], height=0)  # Identify all local maxima
            
            # If peaks are found, display them
            if len(peaks) > 0:
                st.write(f"Local maxima found at indices: {peaks}")
                st.write(f"X-values at maxima: {df['x'].iloc[peaks]}")
                st.write(f"Y-values at maxima: {df['y'].iloc[peaks]}")
            else:
                st.write("No local maxima found.")

            # Ask the user how many Gaussians they want to fit
            num_gaussians = st.number_input("How many Gaussians would you like to fit to the data?", min_value=1, max_value=5, value=1)

            # Ask for initial guesses for the Gaussian means (maxima)
            peaks = []
            for i in range(num_gaussians):
                peak_guess = st.number_input(f"Enter the initial guess for the {i+1}th peak (mean of Gaussian {i+1}):", value=float(df['x'].median()))
                peaks.append(peak_guess)

            # Fit the Gaussians
            if st.button("Fit Gaussians"):
                # Create the x values for fitting
                x_data = df['x']
                y_data = df['y']

                # Prepare the initial parameters for curve fitting
                initial_guess = []
                for peak in peaks:
                    # Initial guess: amplitude (max y), mean (user input), and standard deviation (arbitrary, set to 1)
                    initial_guess += [max(y_data), peak, 1]

                # Create an array of weights based on the local maxima
                weights = np.ones_like(y_data)  # Default weight is 1 for all points
                weights[peaks] = 10  # Increase the weight for points at local maxima

                # Fit the Gaussians
                def multi_gaussian(x, *params):
                    result = np.zeros_like(x)
                    for i in range(num_gaussians):
                        amp, mean, stddev = params[3*i:3*(i+1)]
                        result += gaussian(x, amp, mean, stddev)
                    return result

                # Use curve fitting to find the best parameters with weighted least squares
                popt, _ = curve_fit(multi_gaussian, x_data, y_data, p0=initial_guess, sigma=weights, absolute_sigma=True)

                # Plot the data with the fitted Gaussians
                st.subheader("Fitted Gaussians with Weighted Fitting")
                fig, ax = plt.subplots()
                ax.plot(df['x'], df['y'], label='Data', marker='o', linestyle='-', color='blue')

                # Plot each Gaussian
                for i in range(num_gaussians):
                    amp, mean, stddev = popt[3*i:3*(i+1)]
                    gaussian_fit = gaussian(x_data, amp, mean, stddev)
                    ax.plot(x_data, gaussian_fit, label=f'Gaussian {i+1}', linestyle='--')

                ax.set_title("Gaussian Fit to Data")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.legend()
                st.pyplot(fig)

                # Display fitted parameters (Amplitude, Mean, Standard Deviation for each Gaussian)
                st.write("Fitted Gaussian Parameters:")
                for i in range(num_gaussians):
                    amp, mean, stddev = popt[3*i:3*(i+1)]
                    st.write(f"Gaussian {i+1}: Amplitude = {amp:.2f}, Mean = {mean:.2f}, Stddev = {stddev:.2f}")
                
        else:
            st.error("CSV must contain 'x' and 'y' columns.")



