import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from io import BytesIO
import base64

# Function to load CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to convert plot to bytes
def plot_to_bytes(plot):
    buffer = BytesIO()
    plot.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer

# Function to generate a download link for a plot
def get_download_link(file_bytes, plot_name, file_format):
    b64 = base64.b64encode(file_bytes.read()).decode()
    return f'<a href="data:file/{file_format};base64,{b64}" download="{plot_name}.{file_format}">Download {file_format.upper()}</a>'

# Load the custom CSS
load_css("main.css")

# Title of the app
st.title("CSV Data Visualization and Analysis App")

# Sidebar for file upload and options
st.sidebar.title("Options")

# Upload CSV file
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)
    
    # Display the data
    st.write("Data Preview:")
    st.write(data.head())
    
    # Sidebar selectbox for plot types
    plot_type = st.sidebar.selectbox("Choose Plot Type", ["Scatter Plot", "Line Plot", "Histogram", "Correlation Heatmap"])

    # Generate visualizations based on plot type
    st.subheader("Data Visualization")

    # Scatter Plot
    if plot_type == "Scatter Plot":
        st.subheader("Scatter Plot Configuration")
        x_axis_scatter = st.sidebar.selectbox("Choose X-axis", data.columns, key='scatter_x')
        y_axis_scatter = st.sidebar.selectbox("Choose Y-axis", data.columns, key='scatter_y')
        
        if st.sidebar.button("Submit"):
            st.subheader(f"Scatter Plot of {x_axis_scatter} vs {y_axis_scatter}")
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=data[x_axis_scatter], y=data[y_axis_scatter])
            plt.xlabel(x_axis_scatter)
            plt.ylabel(y_axis_scatter)
            plt.title(f"Scatter Plot of {x_axis_scatter} vs {y_axis_scatter}")
            st.pyplot(plt)
            
            # Download button for PNG format only
            st.subheader("Download Plot")
            buffer = plot_to_bytes(plt)
            st.markdown(get_download_link(buffer, 'scatter_plot', 'png'), unsafe_allow_html=True)

    # Line Plot
    elif plot_type == "Line Plot":
        st.subheader("Line Plot Configuration")
        x_axis_line = st.sidebar.selectbox("Choose X-axis", data.columns, key='line_x')
        y_axis_line = st.sidebar.selectbox("Choose Y-axis", data.columns, key='line_y')
        
        if st.sidebar.button("Submit"):
            st.subheader(f"Line Plot of {x_axis_line} vs {y_axis_line}")
            plt.figure(figsize=(10, 6))
            sns.lineplot(x=data[x_axis_line], y=data[y_axis_line])
            plt.xlabel(x_axis_line)
            plt.ylabel(y_axis_line)
            plt.title(f"Line Plot of {x_axis_line} vs {y_axis_line}")
            st.pyplot(plt)
            
            # Download button for PNG format only
            st.subheader("Download Plot")
            buffer = plot_to_bytes(plt)
            st.markdown(get_download_link(buffer, 'line_plot', 'png'), unsafe_allow_html=True)

    # Histogram
    elif plot_type == "Histogram":
        st.subheader("Histogram Configuration")
        column_hist = st.sidebar.selectbox("Choose Column for Histogram", data.columns, key='hist_column')
        
        if st.sidebar.button("Submit"):
            st.subheader(f"Histogram of {column_hist}")
            plt.figure(figsize=(10, 6))
            sns.histplot(data[column_hist], bins=30, kde=True)
            plt.xlabel(column_hist)
            plt.ylabel("Frequency")
            plt.title(f"Histogram of {column_hist}")
            st.pyplot(plt)
            
            # Download button for PNG format only
            st.subheader("Download Plot")
            buffer = plot_to_bytes(plt)
            st.markdown(get_download_link(buffer, 'histogram', 'png'), unsafe_allow_html=True)

    # Correlation Heatmap
    elif plot_type == "Correlation Heatmap":
        st.subheader("Correlation Heatmap Configuration")
        
        # Select only numeric columns for correlation heatmap
        numeric_data = data.select_dtypes(include=['float64', 'int64'])
        numeric_columns = numeric_data.columns.tolist()
        
        if len(numeric_columns) < 2:
            st.write("Not enough numeric columns to generate a correlation heatmap.")
        else:
            x_axis_heatmap = st.sidebar.selectbox("Choose X-axis", numeric_columns, key='heatmap_x')
            y_axis_heatmap = st.sidebar.selectbox("Choose Y-axis", numeric_columns, key='heatmap_y')
            
            if st.sidebar.button("Submit"):
                st.subheader("Correlation Heatmap")
                plt.figure(figsize=(10, 6))
                correlation_matrix = numeric_data[[x_axis_heatmap, y_axis_heatmap]].corr()
                sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
                plt.title(f"Correlation Heatmap between {x_axis_heatmap} and {y_axis_heatmap}")
                st.pyplot(plt)
                
                # Download button for PNG format only
                st.subheader("Download Plot")
                buffer = plot_to_bytes(plt)
                st.markdown(get_download_link(buffer, 'heatmap', 'png'), unsafe_allow_html=True)

    # Basic Statistical Analysis
    if st.sidebar.checkbox("Show Summary Statistics"):
        st.subheader("Basic Statistical Analysis")
        st.write(data.describe())
        
    # Perform a T-test
    if st.sidebar.checkbox("Perform T-test"):
        st.subheader("T-test")
        numeric_data = data.select_dtypes(include=['float64', 'int64'])
        numeric_columns = numeric_data.columns.tolist()
        
        if len(numeric_columns) >= 2:
            column1 = st.selectbox("Choose Column 1 for T-test", numeric_columns, key='ttest_col1')
            column2 = st.selectbox("Choose Column 2 for T-test", numeric_columns, key='ttest_col2')
            
            if st.button("Submit T-test"):
                t_stat, p_val = stats.ttest_ind(data[column1].dropna(), data[column2].dropna())
                st.write(f"T-test Results between {column1} and {column2}:")
                st.write(f"T-statistic: {t_stat}")
                st.write(f"P-value: {p_val}")
        else:
            st.write("Not enough numeric columns to perform a T-test.")
