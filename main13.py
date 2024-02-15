import streamlit as st
from io import StringIO
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

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


def create_datatypes_table(df):
    # Group columns by data types
    grouped_cols = df.columns.to_series().groupby(df.dtypes).groups

    # Create a dictionary to store data types and corresponding column names
    datatype_dict = {str(key): value.tolist() for key, value in grouped_cols.items()}

    # Create a DataFrame from the dictionary
    datatypes_df = pd.DataFrame.from_dict(datatype_dict, orient='index').fillna('')
    # datatypes_df.index.name = 'Data Type'
    # datatypes_df.columns.name = 'Column Names'

    return datatypes_df


def find_correlation(df,col1,col2):
    if df[col1].dtype in ['int64','float64'] and df[col2].dtype in ['int64','float64']:
        corr1 = df[col1].corr(df[col2])
        return corr1
    else:
        return ('Both columns should contain numerical data for correlation calculation')

def value_counts(df,col1):
    value_counts = df[col1].value_counts().reset_index()
    value_counts.columns = [col1,'Count']
    return value_counts

def generate_plots(df,col):
    categorical_columns = df.select_dtypes(include=['object','category']).columns
    numerical_columns = df.select_dtypes(include=['int','float'])

    if col in categorical_columns:
        if len(df[col].unique()) > 1:
            # plot chart
            pie_chart = px.pie(df, names=col, title=f'Pie chart for {col}')
            st.plotly_chart(pie_chart)
            # Bar chart
            bar_chart = px.bar(df,x=col,title = f'Bar chart for {col}')
            st.plotly_chart(bar_chart)

    if col in numerical_columns:
        box_plot = px.box(df,y=col,title = f'Box Plot for {col}')
        st.plotly_chart(box_plot)

def bivariate_analysis(df,col1,col2):
    if col1 in df.select_dtypes(include=['object','category']).columns and col2 in df.select_dtypes(include=['object','category']).columns:
        st.header(f"Bivariate Analysis: {col1} - {col2}")
        grouped_bar_chart = px.histogram(df,x=col1,color=col2, barmode='group',title = f'Grouped Bar Chart: {col1} vs {col2}')
        st.plotly_chart(grouped_bar_chart)
        # stacked bar chart
        stacked_bar_chart = px.histogram(df,x=col1,color=col2,barmode='stack',title=f'Stacked Bar Chart: {col1} vs {col2}')
        st.plotly_chart(stacked_bar_chart)
    elif col1 in df.select_dtypes(include=['object','category']).columns and col2 in df.select_dtypes(include=['int','float']).columns:
        st.subheader("Bivariate Analysis: Categorical - Numerical")
        box_plot = px.box(df,x=col1,y=col2,color=col1,title=f'Box Plot:{col1} vs {col2}')
        st.plotly_chart(box_plot)
        # swarm plot
        swarm_plot = px.scatter(df,x=col1,y=col2,color=col1,title=f'Swarm Plot: {col1} vs {col2}')
        st.plotly_chart(swarm_plot)

    elif col1 in df.select_dtypes(include=['int','float']).columns and col2 in df.select_dtypes(include=['int','float']).columns:
        st.subheader("Bivariate analysis: Numerical - Numerical")
        scatter_plot = px.scatter(df,x=col1,y=col2,color=col1,title=f'Scatter Plot: {col1} vs {col2}')
        st.plotly_chart(scatter_plot)
        # hexbin plot
        # hexbin_plot = px.hexbin(df,x=col1,y=col2,color=col1,title=f'Hexbin Plot: {col1} vs {col2}')
        # st.plotly_chart(hexbin_plot)
        # Heatmap
        heatmap = px.density_heatmap(df,x=col1,y=col2,marginal_x = 'histogram',marginal_y = 'histogram',title=f'Heatmap: {col1} vs {col2}')
        st.plotly_chart(heatmap)

def summarize_columns(df,col):
    summary_df = pd.DataFrame(columns=['Count','Std Dev','Maximum','Minimum','Mean','Median','Skewness','kurtosis','25%','50%','75%','90%','95%','99%'])
    if col in df.select_dtypes(include=['int64','float64']).columns:
        col_data = df[col]
        summary_df.loc[col] = [
                               col_data.count(),
                               np.std(col_data),
                               np.max(col_data),
                               np.min(col_data),
                               np.mean(col_data),
                               np.median(col_data),
                               col_data.skew(),
                               col_data.kurtosis(),
                               np.percentile(col_data,25),
                               np.percentile(col_data,50),
                               np.percentile(col_data,75),
                               np.percentile(col_data,90),
                               np.percentile(col_data,95),
                               np.percentile(col_data,99)
                               ]
    elif col in df.select_dtypes(include=['object','category']).columns:
        pass



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
        insight = st.sidebar.selectbox("Select Option",['Missing value','Shape','Data Info',' Column Type Info','Correlation','Value Count','Summarize columns','Univariate plot','Bivariate plot'])
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


        elif insight == 'Column Type Info':
            if session_state.data is not None:
                data_table = create_datatypes_table(session_state.data)
                # st.write("Column Types:")
                # st.write(data_table)
        elif insight == 'summarize columns':
            if session_state is not None:
                column1 = st.selectbox('Select one from the option',session_state.data)
                pass


        elif insight == 'Correlation':
            if session_state.data is not None:
                numerical_columns = [col for col in session_state.data.columns if session_state.data[col].dtype in ['int64','float64']]
                if numerical_columns:
                    col1 = st.selectbox('Select first column: ',options = numerical_columns)
                    col2 = st.selectbox('Select second column: ',options = numerical_columns)

                    if st.button('Calculate Correlation'):
                        correlation = find_correlation(session_state.data,col1,col2)
                        st.write(f"Correlation coefficent between {col1} and {col2}:{round(correlation,4)}")

        elif insight == 'Value Count':
            if session_state.data is not None:
                col1 = st.selectbox('Selct Column',options=session_state.data.columns)
                if st.button('Value count'):
                    value_count = value_counts(session_state.data,col1)
                    st.write(value_count)

        elif insight == 'Univariate plot':
            if session_state.data is not None:
                col1 = st.selectbox('Select Column',options=session_state.data.columns)
                if st.button('PLOT'):
                    plot = generate_plots(session_state.data,col1)

        elif insight == 'Bivariate plot':
            st.subheader("Bivariate Analysis")
            if session_state.data is not None:
                col1 = st.selectbox('Select first column:',options = session_state.data.columns)
                col2 = st.selectbox('Select second column:',options = session_state.data.columns)
                st.write(f"Bivariate Analysis for {col1} and {col2}")
                bivariate_analysis(session_state.data,col1,col2)
            else:
                st.warning("Please upload the dataset first.")



if __name__ == "__main__":
    main()
