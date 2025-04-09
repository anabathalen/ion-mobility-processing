import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Simple x-y Plot App")

# Sidebar for user input
st.sidebar.header("Input Parameters")
num_points = st.sidebar.slider("Number of Points", min_value=10, max_value=1000, value=100)
slope = st.sidebar.slider("Slope (m)", min_value=-10.0, max_value=10.0, value=1.0)
intercept = st.sidebar.slider("Intercept (b)", min_value=-50.0, max_value=50.0, value=0.0)

# Generate x and y
x = np.linspace(0, 10, num_points)
y = slope * x + intercept

# Create a DataFrame for display (optional)
df = pd.DataFrame({'x': x, 'y': y})

# Show the data
st.subheader("Generated Data")
st.write(df)

# Plot using Matplotlib
fig, ax = plt.subplots()
ax.plot(x, y, label=f"y = {slope}x + {intercept}")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()

st.subheader("Line Plot")
st.pyplot(fig)
