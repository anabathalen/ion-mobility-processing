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
        st.write("Here is the data you uploaded:")
        st.dataframe(df)
        
        # Check for required columns
        if 'x' in df.columns and 'y' in df.columns:
            # First plot: raw data plot (with x-value annotations) for reference
            st.subheader("Raw Data Plot")
            fig_raw, ax_raw = plt.subplots()
            ax_raw.plot(df['x'], df['y'], 'o', color='black', alpha=1.0)
            # Label each point with its x value (or row number if desired)
            for i, x_val in enumerate(df['x']):
                ax_raw.annotate(f"{x_val}", (df['x'][i], df['y'][i]),
                                textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)
            ax_raw.set_xlabel("X")
            ax_raw.set_ylabel("Y")
            st.pyplot(fig_raw)
            
            # Ask for number of gaussians and their initial guesses for peak (mean) values
            num_gaussians = st.number_input("How many Gaussians would you like to fit to the data?", 
                                            min_value=1, max_value=5, value=1)
            peaks = []
            for i in range(num_gaussians):
                peak_guess = st.number_input(f"Enter the initial guess for the {i+1}th peak (mean of Gaussian {i+1}):", 
                                             value=float(df['x'].median()))
                peaks.append(peak_guess)
            
            # When the user clicks the button to perform the fit:
            if st.button("Fit Gaussians"):
                x_data = df['x']
                y_data = df['y']
                
                # List to store fitted parameter tuples (amp, mean, stddev) for each peak that fits
                fitted_params = []
                
                # Use a color palette (used if you want to visualize individual fits, here we only use for debugging)
                colors = sns.color_palette("Set1", n_colors=num_gaussians)
                
                # Loop over each user-defined peak and perform local Gaussian fit
                for i, peak in enumerate(peaks):
                    # Define local region: using a range from (peak - 0.05*peak) to (peak + 0.05*peak)
                    # (You can modify to fixed 10, or another value)
                    x_range_min = peak - 10
                    x_range_max = peak + 10
                    mask = (x_data >= x_range_min) & (x_data <= x_range_max)
                    x_local = x_data[mask]
                    y_local = y_data[mask]
                    
                    if len(x_local) < 3:
                        continue  # skip if not enough points
                    # Use an initial guess based on the local maximum and provided peak value:
                    local_guess = [max(y_local), peak, 1]  
                    try:
                        popt, _ = curve_fit(gaussian, x_local, y_local, p0=local_guess)
                        fitted_params.append(popt)  # popt is [amp, mean, stddev]
                    except Exception as e:
                        continue
                        
                # Generate summed gaussian across the full data range
                x_full = np.linspace(min(x_data), max(x_data), 1000)
                y_sum = np.zeros_like(x_full)
                # Also for visualization, draw each individual gaussian (optional)
                fig_fit, ax_fit = plt.subplots()
                # Plot the raw data as dots
                ax_fit.plot(x_data, y_data, 'o', color='black', markersize=4)
                for i, params in enumerate(fitted_params):
                    y_fit = gaussian(x_full, *params)
                    y_sum += y_fit
                    # If you want to see the individual fits:
                    # ax_fit.fill_between(x_full, y_fit, color=colors[i], alpha=0.3, label=f'Gaussian {i+1}')
                
                # Plot the summed gaussian as a smooth black line
                ax_fit.plot(x_full, y_sum, '-', color='black', linewidth=2, label='Summed Gaussian')
                
                # Set axis properties as requested:
                # Remove title and y-axis ticks/labels.
                ax_fit.set_title("")
                ax_fit.set_yticks([])
                ax_fit.set_ylabel("")
                ax_fit.set_xlabel("drift time (bins)")
                
                st.pyplot(fig_fit)
                
                # Ask the user if they want to save the figure
                save_fig = st.checkbox("Save figure?")
                if save_fig:
                    st.subheader("Figure Save Options")
                    font_size = st.number_input("Enter desired font size:", value=12)
                    fig_width = st.number_input("Enter desired figure width (inches):", value=8.0)
                    fig_height = st.number_input("Enter desired figure height (inches):", value=6.0)
                    dpi_val = st.number_input("Enter desired resolution (dpi):", value=300)
                    x_label_custom = st.text_input("Enter desired x-axis label:", value="drift time (bins)")
                    
                    # Update font size and x label
                    plt.rcParams.update({'font.size': font_size})
                    ax_fit.set_xlabel(x_label_custom)
                    
                    # Create new figure with requested size and dpi, then replot
                    fig_save, ax_save = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi_val)
                    ax_save.plot(x_data, y_data, 'o', color='black', markersize=4)
                    ax_save.plot(x_full, y_sum, '-', color='black', linewidth=2)
                    
                    ax_save.set_yticks([])
                    ax_save.set_ylabel("")
                    ax_save.set_xlabel(x_label_custom)
                    
                    # Remove title as requested
                    ax_save.set_title("")
                    
                    # Save to a buffer and provide a download link
                    buf = io.BytesIO()
                    fig_save.savefig(buf, format="png", bbox_inches="tight")
                    buf.seek(0)
                    
                    st.download_button(
                        label="Download Figure",
                        data=buf,
                        file_name="figure.png",
                        mime="image/png"
                    )
                    
        else:
            st.error("CSV must contain 'x' and 'y' columns.")

# The function should be called from the main app file.
if __name__ == "__main__":
    upload_and_plot()
