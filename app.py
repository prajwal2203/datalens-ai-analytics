
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="DataLens AI",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #10141c;
    color: white;
}
[data-testid="stMetric"] {
    background: #1c2432;
    padding: 18px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 DataLens AI")
st.caption("Intelligent CSV Data Analysis & Visualization")

uploaded_file = st.sidebar.file_uploader(
    "Upload your CSV dataset",
    type=["csv"]
)

if uploaded_file is None:
    st.info("👈 Upload a CSV file to start analyzing your data.")

    st.subheader("What DataLens AI offers")
    c1, c2, c3 = st.columns(3)
    c1.metric("Feature 01", "Data Analysis")
    c2.metric("Feature 02", "Visual Reports")
    c3.metric("Feature 03", "Data Cleaning")

    st.stop()

try:
    df = pd.read_csv(uploaded_file)
except Exception as e:
    st.error(f"Unable to read CSV: {e}")
    st.stop()

if df.empty:
    st.error("Your CSV file is empty.")
    st.stop()

st.success("Dataset uploaded successfully!")

st.header("📌 Dataset Overview")

total_rows = len(df)
total_columns = len(df.columns)
missing_values = int(df.isnull().sum().sum())
duplicates = int(df.duplicated().sum())

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Rows", f"{total_rows:,}")
c2.metric("Total Columns", total_columns)
c3.metric("Missing Values", missing_values)
c4.metric("Duplicate Rows", duplicates)

st.divider()

st.header("📋 Dataset Preview")
st.dataframe(df.head(100), use_container_width=True)

st.header("📊 Statistical Summary")

numeric_df = df.select_dtypes(include=np.number)

if not numeric_df.empty:
    st.dataframe(
        numeric_df.describe().round(2),
        use_container_width=True
    )

    st.header("📈 Data Visualization")

    selected_column = st.selectbox(
        "Select a numerical column",
        numeric_df.columns
    )

    fig = px.histogram(
        df,
        x=selected_column,
        title=f"Distribution of {selected_column}",
        template="plotly_dark",
        color_discrete_sequence=["#00d4aa"]
    )

    st.plotly_chart(fig, use_container_width=True)

    if len(numeric_df.columns) >= 2:
        st.subheader("Correlation Heatmap")

        corr = numeric_df.corr()

        heatmap = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Teal",
            title="Feature Correlation",
            template="plotly_dark"
        )

        st.plotly_chart(heatmap, use_container_width=True)
else:
    st.warning("No numerical columns found for statistical analysis.")

st.divider()


st.header("🤖 Smart Business Insights")

# Best-selling product
if "Product" in df.columns and "Sales" in df.columns:
    product_sales = df.groupby("Product")["Sales"].sum()
    best_product = product_sales.idxmax()
    best_revenue = product_sales.max()

    st.success(
        f"🏆 Best-selling product: {best_product} "
        f"with sales of ₹{best_revenue:,.2f}"
    )

# Best-performing category
if "Category" in df.columns and "Sales" in df.columns:
    category_sales = df.groupby("Category")["Sales"].sum()
    best_category = category_sales.idxmax()

    st.info(
        f"📈 Top category: {best_category} "
        f"with ₹{category_sales.max():,.2f} in sales"
    )

# Total revenue and profit
if "Sales" in df.columns:
    total_revenue = df["Sales"].sum()
else:
    total_revenue = 0

if "Profit" in df.columns:
    total_profit = df["Profit"].sum()
else:
    total_profit = 0

c1, c2 = st.columns(2)

c1.metric("💰 Total Revenue", f"₹{total_revenue:,.2f}")
c2.metric("💵 Total Profit", f"₹{total_profit:,.2f}")

# Category chart
if "Category" in df.columns and "Sales" in df.columns:
    st.subheader("Category-wise Performance")

    fig = px.bar(
        df.groupby("Category", as_index=False)["Sales"].sum(),
        x="Category",
        y="Sales",
        color="Category",
        template="plotly_dark",
        title="Sales by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

# Download analysis report
st.subheader("📥 Export Analysis")

report = numeric_df.describe().round(2).to_csv()

st.download_button(
    "Download Statistical Report",
    data=report,
    file_name="datalens_analysis.csv",
    mime="text/csv"
)

st.caption("DataLens AI | Built with Python, Pandas, Streamlit & Plotly")
