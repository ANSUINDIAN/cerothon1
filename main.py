import streamlit as st
import pandas as pd


st.title("Dataset Viewer")

# Display a file uploader widget for CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Display the dataset
    st.write("Dataset Preview:")
    st.write(df)

