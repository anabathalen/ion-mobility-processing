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
            
            # Variable to store the clicked peaks
            peaks = []

            # Function to capture mouse clicks on the plot
            def onpick(event):
                # Get the x and y data from the click event
                mouse_x = event.artist.get_xdata()[event.ind][0]
                mouse_y = event.artist.get_ydata()[event.ind][0]
                
                # Add the clicked peak to the peaks list (avoiding duplicates)
                if (mouse_x, mouse_y) not in peaks:
                    peaks.append((mouse_x, mouse_y))
                    st.write(f"Peak selected at x={mouse_x:.2f}, y={mouse_y:.2f}")
                    
                    # Highlight the selected peak
                    ax.plot(mouse_x, mouse_y, 'ro')  # Red dot for peak
                    ax.set_title("Data with Selected Peaks")
                    ax.figure.canvas.draw()
            
            # Connect the pick event to the plot
            fig.canvas.mpl_connect('pick_event', onpick)

            # Enable picking on the data points
            ax.plot(df['x'], df['y'], label='Data', marker='o', linestyle='-', color='blue', picker=True)
            st.pyplot(fig)

            # If the user has selected peaks, let them fit Gaussians
            if len(peaks) > 0:
                st.write(f"Number of peaks selected: {len(peaks)}")
                # Ask the user how many Gaussians they want to fit
                num_gaussians = st.number_input("How many Gaussians would you like to fit to the data?", min_value=1, max_value=5, value=1)

                # Fit the Gaussians
                if st.button("Fit Gaussians"):
                    # Create the x values for fitting
                    x_data = df['x']
                    y_data = df['y']

                    # Prepare the initial parameters for curve fitting
                    initial_guess = []
                    for peak in peaks:
                        # Initial guess: amplitude (max y), mean (user input), and standard deviation (arbitrary, set to 1)
                        initial_guess += [max(y_data), peak[0], 1]

                    # Create an array of weights based on the user-selected peaks
                    weights = np.ones_like(y_data)  # Default weight is 1 for all points
                    for peak in peaks:
                        # Get the index of the peak closest to the selected x value
                        peak_idx = np.abs(x_data - peak[0]).argmin()
                        weights[peak_idx] = 10  # Increase the weight for selected peaks

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
                    st.subheader("Fitted Gaussians with User-Selected Peaks")
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




