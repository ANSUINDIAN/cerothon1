import streamlit as st
from io import StringIO
import pandas as pd

# Function to load data
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df

# Function to generate insights - Data Shape
def data_shape(df):
    st.subheader("Data Shape")
    st.write(df.shape)

# Function to generate insights - Data Info
def data_info(df):
    st.subheader("Data Info")
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.text(info_str)
    return info_str

# Function to generate insights - Data Types
def data_types(data):
    st.subheader("Data Types")
    st.write(data.dtypes)

# Function to generate insights - Missing Value Analysis
def missing_value_analysis(df):
    dict_missing_value = {}
    for col in df.columns:
        dict_missing_value[col] = df[col].isnull().sum()

    frame = pd.DataFrame.from_dict(dict_missing_value, orient='index', columns=['Missing value count'])
    return frame

def main():
    st.title("Insight Generator App")

    # Get session state or initialize it
    session_state = st.session_state
    if 'data' not in session_state:
        session_state.data = None

    # Sidebar
    st.sidebar.title("Options")
    option = st.sidebar.selectbox("Select Option", ["Upload","Insights"])

    if option == "Upload":
        st.sidebar.subheader("File Upload")
        uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file is not None:
            # Display file details and load data
            st.sidebar.write("File Details:")
            file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
            st.sidebar.write(file_details)

            data = load_data(uploaded_file)
            session_state.data = data  # Store data in session state
            st.write("### Sample Data")
            st.write(data.head())

    if option == "Insights":
        st.sidebar.subheader('Page of Insights')
        insight = st.sidebar.selectbox("Select Option",['Missing value','Shape','Data Info','Type Info'])
        if insight == 'Missing value':
            if session_state.data is not None:
                st.subheader("Missing values")
                missing_data = missing_value_analysis(session_state.data)
                st.write(missing_data)
            else:
                st.warning('Please upload the dataset')
        elif insight == 'Shape':
            if session_state.data is not None:
                data_shape(session_state.data)

        elif insight == 'Data Info':
            if session_state.data is not None:
                data_info(session_state.data)

if __name__ == "__main__":
    main()
