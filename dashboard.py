import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------
# Load Data
# ------------------------
st.set_page_config(page_title="Sales Dashboard", layout="wide")
df = pd.read_csv("superstore.csv", encoding="latin-1")

# Clean data (fix column names if needed)
df.columns = df.columns.str.strip()

# ------------------------
# Sidebar Filters
# ------------------------
st.sidebar.header("Filter Data")

region = st.sidebar.multiselect(
    "Select Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Select Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

df_selection = df.query("Region == @region & Category == @category")

# ------------------------
# Main Dashboard
# ------------------------
st.title("📊 Sales Dashboard (Superstore Data)")
st.markdown("Insights into **Sales Performance, Profit, and Trends**")

# KPIs
total_sales = int(df_selection["Sales"].sum())
total_profit = int(df_selection["Profit"].sum())
avg_discount = round(df_selection["Discount"].mean() * 100, 2)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,}")
col2.metric("Total Profit", f"${total_profit:,}")
col3.metric("Avg. Discount", f"{avg_discount}%")

st.markdown("---")

# Sales by Category
sales_by_category = (
    df_selection.groupby("Category")["Sales"].sum().reset_index()
)
fig_category = px.bar(
    sales_by_category,
    x="Category",
    y="Sales",
    title="Sales by Category",
    color="Category"
)
st.plotly_chart(fig_category, use_container_width=True)

# Sales by Region
sales_by_region = (
    df_selection.groupby("Region")["Sales"].sum().reset_index()
)
fig_region = px.pie(
    sales_by_region,
    names="Region",
    values="Sales",
    title="Sales Distribution by Region"
)
st.plotly_chart(fig_region, use_container_width=True)

# Sales Trend Over Time
df_selection["Order Date"] = pd.to_datetime(df_selection["Order Date"])
sales_trend = (
    df_selection.groupby(df_selection["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
)
sales_trend["Order Date"] = sales_trend["Order Date"].astype(str)

fig_trend = px.line(
    sales_trend,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend"
)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("✅ Dashboard ready — filter on the left to interact with data.")

