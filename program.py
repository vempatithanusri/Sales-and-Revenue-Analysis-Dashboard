# Sales & Revenue Analysis Dashboard
# Streamlit Dashboard Project

# Install required libraries before running:
# pip install streamlit pandas plotly openpyxl

import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Title
st.title("📊 Sales & Revenue Analysis Dashboard")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Excel or CSV File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Convert Date Column
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Product Filter
    if 'Product' in df.columns:
        product = st.sidebar.multiselect(
            "Select Product",
            options=df['Product'].unique(),
            default=df['Product'].unique()
        )
        df = df[df['Product'].isin(product)]

    # Region Filter
    if 'Region' in df.columns:
        region = st.sidebar.multiselect(
            "Select Region",
            options=df['Region'].unique(),
            default=df['Region'].unique()
        )
        df = df[df['Region'].isin(region)]

    # KPIs
    total_sales = df['Sales'].sum()
    total_revenue = df['Revenue'].sum()
    total_orders = len(df)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"{total_sales:,.2f}")
    col2.metric("Total Revenue", f"{total_revenue:,.2f}")
    col3.metric("Total Orders", total_orders)

    # Revenue Trend
    st.subheader("📈 Revenue Trend")

    if 'Date' in df.columns:
        revenue_trend = df.groupby('Date')['Revenue'].sum().reset_index()

        fig1 = px.line(
            revenue_trend,
            x='Date',
            y='Revenue',
            title='Revenue Over Time'
        )

        st.plotly_chart(fig1, use_container_width=True)

    # Top Products
    st.subheader("🏆 Top Performing Products")

    if 'Product' in df.columns:
        top_products = df.groupby('Product')['Revenue'].sum().reset_index()

        fig2 = px.bar(
            top_products,
            x='Product',
            y='Revenue',
            color='Revenue',
            title='Top Products by Revenue'
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Sales by Region
    st.subheader("🌍 Sales by Region")

    if 'Region' in df.columns:
        region_sales = df.groupby('Region')['Sales'].sum().reset_index()

        fig3 = px.pie(
            region_sales,
            names='Region',
            values='Sales',
            title='Regional Sales Distribution'
        )

        st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Please upload a CSV or Excel file to view the dashboard.")
