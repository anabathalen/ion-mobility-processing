import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
            # Plot the data
            fig, ax = plt.subplots()
            ax.plot(df['x'], df['y'], marker='o', linestyle='-')
            ax.set_title("Plot of x vs y")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            st.pyplot(fig)
        else:
            st.error("CSV must contain 'x' and 'y' columns.")

