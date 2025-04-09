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
    df = pd.read_csv(uploaded_file)
    st.write("Preview of data:")
    st.dataframe(df.head())

    try:
        x = df.iloc[:, 0].values
        y = df.iloc[:, 1].values

        n_gaussians = st.slider("Number of Gaussians to fit", 1, 5, 1)

        # Initial guess: equally spaced means, fixed width, guess amps
        amps = [max(y) / n_gaussians] * n_gaussians
        cens = np.linspace(min(x), max(x), n_gaussians)
        wids = [1.0] * n_gaussians

        initial_guess = []
        for a, c, w in zip(amps, cens, wids):
            initial_guess += [a, c, w]

        popt, _ = curve_fit(multi_gaussian, x, y, p0=initial_guess)

        # Plot
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

        # Output parameters
        st.subheader("Fitted Parameters")
        for i in range(n_gaussians):
            st.write(f"Gaussian {i+1}:")
            st.write(f"  Amplitude = {popt[i*3]:.3f}")
            st.write(f"  Center = {popt[i*3+1]:.3f}")
            st.write(f"  Width = {popt[i*3+2]:.3f}")

    except Exception as e:
        st.error(f"Something went wrong with fitting: {e}")
