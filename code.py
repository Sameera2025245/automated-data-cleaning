# Filename: automated_data_dashboard.py

import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit page setup
st.set_page_config(page_title="Automated Data Cleaning & Stats Dashboard", layout="wide")

st.title("Automated Data Cleaning & Statistics Dashboard")

# 1. File upload
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.subheader("Raw Data")
    st.dataframe(df.head(10))
    
    # 2. Automated Data Cleaning
    st.subheader("Data Cleaning Options")
    
    # Handle missing values
    missing_option = st.selectbox("How to handle missing values?", 
                                  ["Drop rows with missing values", 
                                   "Fill with mean (numerical) / mode (categorical)",
                                   "Leave as is"])
    
    df_clean = df.copy()
    
    if missing_option == "Drop rows with missing values":
        df_clean = df_clean.dropna()
    elif missing_option == "Fill with mean (numerical) / mode (categorical)":
        for col in df_clean.columns:
            if df_clean[col].dtype in [np.float64, np.int64]:
                df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
            else:
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    st.subheader("Cleaned Data")
    st.dataframe(df_clean.head(10))
    
    # 3. Descriptive Statistics
    st.subheader("Descriptive Statistics")
    st.write(df_clean.describe(include='all'))
    
    # 4. Visualizations
    st.subheader("Visualizations")
    
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        st.write("### Histogram of a Numeric Column")
        selected_col = st.selectbox("Select column for histogram", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df_clean[selected_col], kde=True, ax=ax)
        st.pyplot(fig)
        
        st.write("### Correlation Heatmap")
        corr = df_clean[numeric_cols].corr()
        fig2, ax2 = plt.subplots()
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax2)
        st.pyplot(fig2)
    
    # 5. Export Cleaned Data
    st.subheader("Export Cleaned Data")
    export_csv = df_clean.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Cleaned Data as CSV", data=export_csv, file_name="cleaned_data.csv", mime="text/csv")
