import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Step 1: Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file with 'x' and 'y' columns", type="csv")

# Helper: sum of N gaussians
def multi_gaussian(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        amp = params[i]
        cen = params[i+1]
        wid = params[i+2]
        y += amp * np.exp(-(x - cen)**2 / (2 * wid**2))
    return y

if uploaded_file is not None:
    try:
        # Step 2: Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Show the first few rows of the uploaded data to the user
        st.write("Data Preview:")
        st.write(df.head())  # Ensure the dataframe is valid
        
        # Step 3: Ensure correct data format (x and y columns)
        if 'x' in df.columns and 'y' in df.columns:
            x = df['x'].values
            y = df['y'].values

            st.write(f"Data successfully loaded: {len(x)} data points.")
            
            # Step 4: Plot y vs x
            st.write("Here is the plot of y vs x:")
            fig, ax = plt.subplots()
            ax.plot(x, y, 'b.', label="Data")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title("y vs x")
            st.pyplot(fig)

            # Step 5: Ask the user for number of Gaussians
            n_gaussians = st.slider("Number of Gaussians to fit", 1, 5, 3)

            # Step 6: Ask the user for initial parameters for each Gaussian
            initial_guesses = []
            for i in range(n_gaussians):
                st.subheader(f"Gaussian {i+1} parameters")
                amplitude = st.number_input(f"Amplitude of Gaussian {i+1}", value=max(y)/n_gaussians, step=0.1)
                centroid = st.number_input(f"Centroid (mean) of Gaussian {i+1}", value=np.mean(x), step=0.1)
                width = st.number_input(f"Width (sigma) of Gaussian {i+1}", value=1.0, step=0.1)

                initial_guesses.extend([amplitude, centroid, width])

            # Step 7: Fit the Gaussians
            if st.button("Fit Gaussians"):
                try:
                    # Perform the curve fitting
                    popt, _ = curve_fit(multi_gaussian, x, y, p0=initial_guesses)
                    st.write("Fitting successful!")

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

                    # Step 8: Display fitted parameters
                    st.subheader("Fitted Parameters")
                    for i in range(n_gaussians):
                        st.write(f"Gaussian {i+1}:")
                        st.write(f"  Amplitude = {popt[i*3]:.3f}")
                        st.write(f"  Center = {popt[i*3+1]:.3f}")
                        st.write(f"  Width = {popt[i*3+2]:.3f}")
                except Exception as e:
                    st.error(f"An error occurred during the fitting process: {e}")
        else:
            st.error("The uploaded CSV must contain 'x' and 'y' columns.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
else:
    st.info("Please upload a CSV file to begin.")






