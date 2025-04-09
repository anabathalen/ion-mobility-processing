import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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
            
            # Label each point with its row number
            for i, txt in enumerate(df['y']):
                ax.annotate(f"Row {i+1}", (df['x'][i], df['y'][i]), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)
                
            ax.set_title("Data")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            st.pyplot(fig)

            # Ask the user how many Gaussians they want to fit
            num_gaussians = st.number_input("How many Gaussians would you like to fit to the data?", min_value=1, max_value=5, value=1)

            # Ask for initial guesses for the Gaussian means (peak x-values)
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

                # Fitting function to include only a local region (x-10 to x+10)
                def multi_gaussian(x, *params):
                    result = np.zeros_like(x)
                    for i in range(num_gaussians):
                        amp, mean, stddev = params[3*i:3*(i+1)]
                        result += gaussian(x, amp, mean, stddev)
                    return result

                # Prepare to store the fitted results
                fig, ax = plt.subplots()
                ax.plot(df['x'], df['y'], label='Data', marker='o', linestyle='-', color='blue')

                # Loop through each peak guess to perform the fitting and plot the results
                for peak in peaks:
                    # Define the local region from peak - 10 to peak + 10
                    x_range_min = peak - 10
                    x_range_max = peak + 10

                    # Get the subset of data within the x-range [peak-10, peak+10]
                    mask = (x_data >= x_range_min) & (x_data <= x_range_max)
                    x_local = x_data[mask]
                    y_local = y_data[mask]

                    # Ensure we have enough points for fitting
                    if len(x_local) < 3:
                        st.warning(f"Not enough data points around peak {peak:.2f} for fitting. Skipping this peak.")
                        continue  # Skip this peak if there's not enough data

                    # Initial guess for this local region
                    local_guess = [max(y_local), peak, 1]  # Amplitude, Mean (the peak), Stddev

                    # Fit the Gaussians for this region only
                    try:
                        popt, _ = curve_fit(multi_gaussian, x_local, y_local, p0=local_guess)
                    except Exception as e:
                        st.error(f"Fitting failed for peak {peak:.2f}: {e}")
                        continue  # Skip this peak if fitting fails

                    # Plot the fitted Gaussian if fitting was successful
                    for i in range(num_gaussians):
                        amp, mean, stddev = popt[3*i:3*(i+1)]
                        gaussian_fit = gaussian(x_local, amp, mean, stddev)
                        ax.plot(x_local, gaussian_fit, label=f'Gaussian {i+1} around x={peak:.2f}', linestyle='--')

                ax.set_title("Gaussian Fit to Data (with Local Regions)")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.legend()
                st.pyplot(fig)

                # Display fitted parameters (Amplitude, Mean, Standard Deviation for each Gaussian)
                st.write("Fitted Gaussian Parameters:")
                for i, peak in enumerate(peaks):
                    st.write(f"Peak {i+1} (initial guess: {peak}):")
                    # Only access popt if the fitting was successful
                    if 'popt' in locals():
                        for j in range(num_gaussians):
                            amp, mean, stddev = popt[3*j:3*(j+1)]
                            st.write(f"  Gaussian {j+1}: Amplitude = {amp:.2f}, Mean = {mean:.2f}, Stddev = {stddev:.2f}")
                    else:
                        st.write(f"  Gaussian fitting failed for peak {peak:.2f}")
                
        else:
            st.error("CSV must contain 'x' and 'y' columns.")







