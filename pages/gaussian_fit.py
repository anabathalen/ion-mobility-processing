import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

st.title("🌋 Gaussian Fitting Tool")

# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file with x and y columns", type="csv")

# Helper: sum of N gaussians
def multi_gaussian(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        amp = params[i]
        cen = params[i+1]
        wid = params[i+2]
        y += amp * np.exp(-(x - cen)**2 / (2 * wid**2))
    return y

if uploaded_file:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        st.write("Preview of the uploaded data:")
        st.dataframe(df.head())  # Show the first few rows of the uploaded data

        # Ensure we have 'x' and 'y' columns
        if 'x' in df.columns and 'y' in df.columns:
            x = df['x'].values
            y = df['y'].values

            # Show some debug information
            st.write(f"Total data points: {len(x)}")

            # Create a progress bar to show live updates during fitting
            progress_bar = st.progress(0)
            
            # Gaussian fitting options
            n_gaussians = st.slider("Number of Gaussians to fit", 1, 5, 3)

            # Initial guess: equally spaced means, fixed width, guess amps
            amps = [max(y) / n_gaussians] * n_gaussians
            cens = np.linspace(min(x), max(x), n_gaussians)
            wids = [1.0] * n_gaussians

            initial_guess = []
            for a, c, w in zip(amps, cens, wids):
                initial_guess += [a, c, w]

            # Perform the curve fitting
            popt, _ = curve_fit(multi_gaussian, x, y, p0=initial_guess)

            # Plot the result
            fig, ax = plt.subplots()
            ax.plot(x, y, 'b.', label="Data")
            ax.plot(x, multi_gaussian(x, *popt), 'r-', label="Total Fit")

            # Plot individual Gaussians
            for i in range(n_gaussians):
                amp = popt[i*3]
                cen = popt[i*3 + 1]
                wid = popt[i*3 + 2]
                g = amp * np.exp(-(x - cen)**2 / (2 * wid**2))
                ax.plot(x, g, '--', label=f'Gaussian {i+1}')

            ax.legend()
            st.pyplot(fig)

            # Display the fitted parameters
            st.subheader("Fitted Parameters")
            for i in range(n_gaussians):
                st.write(f"Gaussian {i+1}:")
                st.write(f"  Amplitude = {popt[i*3]:.3f}")
                st.write(f"  Center = {popt[i*3+1]:.3f}")
                st.write(f"  Width = {popt[i*3+2]:.3f}")

            # Update the progress bar to indicate fitting is complete
            progress_bar.progress(100)

        else:
            st.error("The uploaded CSV must contain 'x' and 'y' columns.")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")


