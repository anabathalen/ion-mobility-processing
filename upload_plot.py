import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
import io

st.write("This page is for fitting gaussians to x, y data. If you have already calibrated/summed/done whatever else you planned to do to your data, and you just want to fit gaussians to the major peaks, this tool is for you.")

# Define the Gaussian function
def gaussian(x, amp, mean, stddev):
    return amp * np.exp(-(x - mean)**2 / (2 * stddev**2))

# Find major local maxima (points where the y values go down on both sides 5 times) and intensity >= 0.1 * max intensity
def find_major_local_maxima(x, y, window_size=5, intensity_threshold=0.1):
    maxima_indices = []
    max_intensity = max(y)
    for i in range(window_size, len(y) - window_size):
        if y[i] == max(y[i - window_size:i + window_size + 1]) and y[i] >= intensity_threshold * max_intensity:
            maxima_indices.append(i)
    return maxima_indices

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
                ax.annotate(f'{x_val:.2f}', (x_val, y_val), textcoords="offset points", xytext=(0, 5), ha='center')

            ax.legend()
            st.pyplot(fig)

            # Now ask the user to enter the initial guesses for the Gaussian peaks
            num_gaussians = st.number_input("How many Gaussians would you like to fit to the data?", min_value=1, max_value=10, value=1)

            peaks = []
            for i in range(num_gaussians):
                peak_guess = st.number_input(f"Enter the initial guess for the {i+1}th peak (mean of Gaussian {i+1}):", value=float(df['x'].median()))
                peaks.append(peak_guess)

            # Create the x values for fitting
            x_data = df['x']
            y_data = df['y']

            # Prepare the initial parameters for curve fitting
            initial_guess = []
            for peak in peaks:
                # Initial guess: amplitude (max y), mean (user input), and standard deviation (arbitrary, set to 1)
                initial_guess += [max(y_data), peak, 100]

            # Fitting function to include only a local region (x-10 to x+10)
            def multi_gaussian(x, *params):
                result = np.zeros_like(x)
                for i in range(num_gaussians):
                    amp, mean, stddev = params[3*i:3*(i+1)]
                    result += gaussian(x, amp, mean, stddev)
                return result

            # Fix for standard deviation constraints
            def fit_with_fixed_stddev(x_data, y_data, peaks):
                # Start by fitting the first peak
                initial_guess = [max(y_data), peaks[0], 100]
                popt, _ = curve_fit(gaussian, x_data, y_data, p0=initial_guess)

                # Extract the fitted standard deviation for the first peak
                stddev_first_peak = popt[2]

                # For subsequent peaks, limit the stddev to be no more than 10% larger than the previous one
                all_params = []
                for i, peak in enumerate(peaks):
                    if i == 0:
                        # Use the fitted stddev for the first peak
                        stddev = stddev_first_peak
                    else:
                        # For subsequent peaks, limit the stddev to 10% larger than the previous one
                        stddev = min(stddev_first_peak * (1 + 0.1 * i), stddev_first_peak * 1.5)  # Arbitrary upper limit of 1.5 times
                    initial_guess = [max(y_data), peak, stddev]
                    popt, _ = curve_fit(gaussian, x_data, y_data, p0=initial_guess)
                    all_params += popt[1:]  # Append the mean and stddev of each peak (amp is not needed here)

                return all_params

            # Fit the Gaussians
            fitted_params = fit_with_fixed_stddev(x_data, y_data, peaks)

            # Now plot the fit
            fig, ax = plt.subplots()
            ax.plot(df['x'], df['y'], label='Data', color='black', alpha=1.0, linewidth=1)  # Data as line

            # Create a high-resolution x-axis (full range) for the fit
            x_full = np.linspace(min(x_data), max(x_data), 1000)

            colors = sns.color_palette("Set1", n_colors=num_gaussians)

            # Loop through each peak guess to perform the fitting and plot the results
            for i, peak in enumerate(peaks):
                amp, mean, stddev = fitted_params[3*i:3*(i+1)]
                y_fit = gaussian(x_full, amp, mean, stddev)

                # Plot the fitted Gaussian across the full range with a transparent fill
                ax.fill_between(x_full, y_fit, color=colors[i], alpha=0.3, label=f'Gaussian {i+1} - mean: {mean:.2f}, stddev: {stddev:.2f}')

            ax.legend()
            st.pyplot(fig)

            # Allow user to download the customized plot
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
    
            st.download_button(
                label="Download Customized Plot as PNG",
                data=buf,
                file_name="customized_gaussian_plot.png",
                mime="image/png"
            )

