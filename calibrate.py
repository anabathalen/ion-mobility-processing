import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import zipfile
import os
from io import BytesIO
import tempfile

# Gaussian function definition
def gaussian(x, amp, mean, stddev):
    return amp * np.exp(-((x - mean) ** 2) / (2 * stddev ** 2))

# R-squared calculation
def r_squared(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

# Gaussian fit function with retries
def fit_gaussian_with_retries(drift_time, intensity, n_attempts=10):
    best_r2 = -np.inf
    best_params = None
    best_fitted_values = None

    for _ in range(n_attempts):
        initial_guess = [
            np.random.uniform(0.8 * max(intensity), 1.2 * max(intensity)),
            np.random.uniform(np.min(drift_time), np.max(drift_time)),
            np.random.uniform(0.1 * np.std(drift_time), 2 * np.std(drift_time))
        ]

        try:
            params, _ = curve_fit(gaussian, drift_time, intensity, p0=initial_guess)
            fitted_values = gaussian(drift_time, *params)
            r2 = r_squared(intensity, fitted_values)

            if r2 > best_r2:
                best_r2 = r2
                best_params = params
                best_fitted_values = fitted_values
        except RuntimeError:
            continue

    return best_params, best_r2, best_fitted_values

# Function to handle file processing and fitting
def process_uploaded_files(uploaded_zip):
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Extract the ZIP file to a temporary directory
        with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        protein_results = []
        protein_plots = []
        folder_names = [folder for folder in os.listdir(tmpdirname) if os.path.isdir(os.path.join(tmpdirname, folder))]

        return folder_names, tmpdirname

# Streamlit interface
st.write("### IMS Calibration Reference File Generator")
st.write("""
This tool is for generating IMS calibration reference files to calibrate your data. 
Upload a ZIP file containing folders with your text files. Each folder should be named with the protein name, 
and each file should contain a 'charge state'. The files should be in the format 'chargestate.txt'.
""")

# File uploader widget
uploaded_zip = st.file_uploader("Upload ZIP File", type=["zip"])

if uploaded_zip:
    # Show the uploaded ZIP file name immediately
    st.write(f"Uploaded file: {uploaded_zip.name}")

    # Get the folder names after extraction
    folder_names, tmpdirname = process_uploaded_files(uploaded_zip)
    
    # Immediately show a list of the calibrant folders
    st.write(f"### Found the following calibrant folders in the ZIP file:")
    st.write(folder_names)
    
    # Iterate over each protein folder and display results
    for protein_name in folder_names:
        st.write(f"### Processing Folder: {protein_name}")

        protein_results = []
        protein_plots = []

        folder_path = os.path.join(tmpdirname, protein_name)
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.txt') and filename[0].isdigit():
                file_path = os.path.join(folder_path, filename)

                # Load the data from the file
                data = np.loadtxt(file_path)
                drift_time = data[:, 0]
                intensity = data[:, 1]

                # Perform Gaussian fit
                params, r2, fitted_values = fit_gaussian_with_retries(drift_time, intensity)

                # Store results and plots
                if params is not None:
                    amp, apex, stddev = params
                    protein_results.append([protein_name, filename, apex, r2, amp, stddev])
                    protein_plots.append((drift_time, intensity, fitted_values, filename, apex, r2))

        # Display the results and plots for this protein folder
        if protein_plots:
            n_plots = len(protein_plots)
            n_cols = 3
            n_rows = (n_plots + n_cols - 1) // n_cols

            # Display all the plots for the current protein folder
            plt.figure(figsize=(12, 4 * n_rows))
            for i, (drift_time, intensity, fitted_values, filename, apex, r2) in enumerate(protein_plots):
                plt.subplot(n_rows, n_cols, i + 1)
                plt.plot(drift_time, intensity, 'b.', label='Raw Data', markersize=3)
                plt.plot(drift_time, fitted_values, 'r-', label='Gaussian Fit', linewidth=1)
                plt.title(f'{filename}\nApex: {apex:.2f}, R²: {r2:.3f}')
                plt.xlabel('Drift Time')
                plt.ylabel('Intensity')
                plt.legend()
                plt.grid()

            plt.tight_layout()
            st.pyplot()

            # Show a table of results for the current protein folder
            results_df = pd.DataFrame(protein_results, columns=['Protein', 'File', 'Apex Drift Time', 'R²', 'Amplitude', 'Standard Deviation'])
            st.write(results_df)

            # Acceptance/Decline for each file
            for result in protein_results:
                protein, filename, apex, r2, amp, stddev = result
                st.write(f"### {filename} - {protein}")
                st.write(f"Apex: {apex:.2f}, R²: {r2:.3f}")
                st.write(f"Amplitude: {amp:.2f}, Standard Deviation: {stddev:.2f}")
                
                # Add Accept/Decline buttons for each file
                accept = st.button(f"Accept Fit for {filename}")
                decline = st.button(f"Decline Fit for {filename}")
                
                if accept:
                    st.write(f"You accepted the fit for {filename}")
                if decline:
                    st.write(f"You declined the fit for {filename}")
