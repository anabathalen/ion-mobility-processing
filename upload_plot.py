import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import seaborn as sns
import io

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
            # Ask the user how many Gaussians they want to fit
            num_gaussians = st.number_input("How many Gaussians would you like to fit to the data?", min_value=1, max_value=5, value=1)

            # Ask for initial guesses for the Gaussian means (peak x-values)
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

            # Customization options for the plot
            dpi = st.slider("Select DPI", min_value=50, max_value=300, value=150)
            font_size = st.slider("Font Size", min_value=8, max_value=20, value=12)
            fig_size = st.slider("Figure Size (inches)", min_value=5, max_value=10, value=8)
            x_label = st.text_input("Enter X-axis Label", "Drift Time (Bins)")
            color_palette = st.selectbox("Choose a Color Palette", options=["Set1", "Set2", "Paired", "Pastel1", "Dark2"])

            # Line width for the data plot
            line_width = st.slider("Line Width for Data Plot", min_value=1, max_value=5, value=2)

            # Fit the Gaussians and plot the result
            fig, ax = plt.subplots()
            ax.plot(df['x'], df['y'], label='Data', color='black', alpha=1.0, linewidth=line_width)  # Data as line

            # Get the selected color palette
            colors = sns.color_palette(color_palette, n_colors=num_gaussians)

            # Create a high-resolution x-axis (full range) for the fit
            x_full = np.linspace(min(x_data), max(x_data), 1000)

            # Loop through each peak guess to perform the fitting and plot the results
            for i, peak in enumerate(peaks):
                # Define the local region from peak - 10 to peak + 10
                x_range_min = peak - peak*0.05
                x_range_max = peak + peak*0.05

                # Get the subset of data within the x-range [peak-10, peak+10]
                mask = (x_data >= x_range_min) & (x_data <= x_range_max)
                x_local = x_data[mask]
                y_local = y_data[mask]

                # Ensure we have enough points for fitting
                if len(x_local) < 3:
                    continue  # Skip this peak if there's not enough data

                # Initial guess for this local region
                local_guess = [max(y_local), peak, 1]  # Amplitude, Mean (the peak), Stddev

                # Fit the Gaussians for this region only
                try:
                    # Fit the Gaussian to the local data
                    popt, _ = curve_fit(gaussian, x_local, y_local, p0=local_guess)
                    
                    # Extract parameters from the fitting result
                    amp, mean, stddev = popt

                    # Generate y values across the full x_full range to plot the Gaussian
                    y_fit = gaussian(x_full, amp, mean, stddev)

                    # Plot the fitted Gaussian across the full range with a transparent fill
                    ax.fill_between(x_full, y_fit, color=colors[i], alpha=0.3, label=f'Gaussian {i+1} (mean = {mean:.2f})')
                    
                except Exception as e:
                    continue  # Skip this peak if fitting fails

            # Update plot aesthetics based on user settings
            ax.set_xlabel(x_label, fontsize=font_size)
            ax.tick_params(axis='y', labelleft=False, left=False, right=False)
            ax.set_ylabel("", fontsize=font_size)

            # Update X-axis tick label font size
            ax.tick_params(axis='x', labelsize=font_size)

            # Remove grey line around the legend
            ax.legend(fontsize=font_size, frameon=False)

            # Adjust figure size
            fig.set_size_inches(fig_size, fig_size)
            plt.rcParams.update({'font.size': font_size})  # Update font size globally

            # Show the plot to the user
            st.pyplot(fig)

            # Allow user to download the customized plot
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=dpi)
            buf.seek(0)

            st.download_button(
                label="Download Customized Plot as PNG",
                data=buf,
                file_name="customized_gaussian_plot.png",
                mime="image/png"
            )



