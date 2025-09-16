import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import time

# ------------------------
# Page Configuration
# ------------------------
st.set_page_config(
    page_title="Executive Sales Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Custom CSS for professional styling and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
    
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(102, 126, 234, 0.5); }
        to { text-shadow: 0 0 30px rgba(118, 75, 162, 0.8); }
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: #f8fafc;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------
# Load Data with Error Handling
# ------------------------
@st.cache_data
def load_data(file_path=None, uploaded_file=None):
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, encoding="latin-1")
        elif file_path:
            df = pd.read_csv(file_path, encoding="latin-1")
        else:
            # Sample data if no file is provided
            np.random.seed(42)
            dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
            sample_data = {
                'Order Date': np.random.choice(dates, 1000),
                'Region': np.random.choice(['East', 'West', 'Central', 'South'], 1000),
                'Category': np.random.choice(['Technology', 'Furniture', 'Office Supplies'], 1000),
                'Sales': np.random.uniform(10, 5000, 1000),
                'Profit': np.random.uniform(-500, 1500, 1000),
                'Discount': np.random.uniform(0, 0.5, 1000)
            }
            df = pd.DataFrame(sample_data)
        
        # Clean data
        df.columns = df.columns.str.strip()
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'])
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Header with animation
st.markdown('<h1 class="main-header">EXECUTIVE SALES DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time Business Intelligence & Performance Analytics</p>', unsafe_allow_html=True)

# Data loading section
data_source = st.radio("Choose Data Source:", ["Upload File", "Use Sample Data", "Default File"], horizontal=True)

df = None
if data_source == "Upload File":
    uploaded_file = st.file_uploader("Upload your sales data", type=['csv', 'xlsx'])
    if uploaded_file is not None:
        df = load_data(uploaded_file=uploaded_file)
        st.success("✅ Data uploaded successfully!")
elif data_source == "Use Sample Data":
    df = load_data()
    st.info("Using sample data for demonstration")
else:
    try:
        df = load_data("superstore.csv")
    except:
        st.warning("⚠️ Default file not found. Using sample data instead.")
        df = load_data()

if df is None:
    st.stop()

# ------------------------
# Advanced Sidebar Filters
# ------------------------
st.sidebar.markdown("### 🔍 Filter Controls")

# Date range filter
if 'Order Date' in df.columns:
    min_date = df['Order Date'].min().date()
    max_date = df['Order Date'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Apply date filter
    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['Order Date'].dt.date >= start_date) & 
                (df['Order Date'].dt.date <= end_date)]

# Multi-select filters
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

# Sales range filter
if not df.empty:
    sales_range = st.sidebar.slider(
        "Sales Range",
        min_value=float(df["Sales"].min()),
        max_value=float(df["Sales"].max()),
        value=(float(df["Sales"].min()), float(df["Sales"].max())),
        format="$%.0f"
    )

# Apply filters
df_selection = df.query(
    "Region == @region & Category == @category & Sales >= @sales_range[0] & Sales <= @sales_range[1]"
)

if df_selection.empty:
    st.warning("No data matches the selected filters!")
    st.stop()

# ------------------------
# KPI Section with Advanced Metrics
# ------------------------
st.markdown("---")

# Calculate metrics
total_sales = df_selection["Sales"].sum()
total_profit = df_selection["Profit"].sum()
avg_discount = df_selection["Discount"].mean() * 100
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = len(df_selection)
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

# Calculate deltas (comparing with previous period)
if 'Order Date' in df_selection.columns and len(df_selection) > 0:
    current_period = df_selection[df_selection['Order Date'] >= df_selection['Order Date'].quantile(0.5)]
    previous_period = df_selection[df_selection['Order Date'] < df_selection['Order Date'].quantile(0.5)]
    
    sales_delta = ((current_period['Sales'].sum() - previous_period['Sales'].sum()) / 
                   previous_period['Sales'].sum() * 100) if previous_period['Sales'].sum() > 0 else 0
    
    profit_delta = ((current_period['Profit'].sum() - previous_period['Profit'].sum()) / 
                    previous_period['Profit'].sum() * 100) if previous_period['Profit'].sum() > 0 else 0
else:
    sales_delta = 0
    profit_delta = 0

# Display KPIs
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.0f}",
        delta=f"{sales_delta:+.1f}%"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}",
        delta=f"{profit_delta:+.1f}%"
    )

with col3:
    st.metric(
        "Profit Margin",
        f"{profit_margin:.1f}%"
    )

with col4:
    st.metric(
        "Avg Order Value",
        f"${avg_order_value:.0f}"
    )

with col5:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

with col6:
    st.metric(
        "🏷Avg Discount",
        f"{avg_discount:.1f}%"
    )

st.markdown("---")

# ------------------------
# Tabbed Interface for Charts
# ------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Trends", "🌍 Geographic", "📉 Performance", "🔍 Deep Dive"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Enhanced Sales by Category
        sales_by_category = df_selection.groupby("Category")["Sales"].sum().reset_index()
        fig_category = px.bar(
            sales_by_category,
            x="Category",
            y="Sales",
            title="Sales Performance by Category",
            color="Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_category.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    with col2:
        # Enhanced Sales by Region
        sales_by_region = df_selection.groupby("Region")["Sales"].sum().reset_index()
        fig_region = px.pie(
            sales_by_region,
            names="Region",
            values="Sales",
            title="Revenue Distribution by Region",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_region.update_traces(textposition='inside', textinfo='percent+label')
        fig_region.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_region, use_container_width=True)
    
    # Profit vs Sales Scatter
    col3, col4 = st.columns(2)
    
    with col3:
        fig_scatter = px.scatter(
            df_selection,
            x="Sales",
            y="Profit",
            color="Category",
            size="Discount",
            title="Sales vs Profit Analysis",
            hover_data=["Region"]
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col4:
        # Top performing categories by profit margin
        profit_margin_by_cat = df_selection.groupby("Category").apply(
            lambda x: x["Profit"].sum() / x["Sales"].sum() * 100 if x["Sales"].sum() > 0 else 0
        ).reset_index()
        profit_margin_by_cat.columns = ["Category", "Profit Margin"]
        
        fig_margin = px.bar(
            profit_margin_by_cat,
            x="Category",
            y="Profit Margin",
            title="Profit Margin by Category",
            color="Profit Margin",
            color_continuous_scale="RdYlGn"
        )
        fig_margin.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_margin, use_container_width=True)

with tab2:
    if 'Order Date' in df_selection.columns:
        # Monthly trend
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_sales = df_selection.groupby(df_selection["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
            monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)
            
            fig_trend = px.line(
                monthly_sales,
                x="Order Date",
                y="Sales",
                title="Monthly Sales Trend",
                markers=True
            )
            fig_trend.update_traces(line_color='#667eea', marker_color='#764ba2')
            fig_trend.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                title_font_size=16
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col2:
            # Quarterly comparison
            df_selection['Quarter'] = df_selection['Order Date'].dt.to_period('Q').astype(str)
            quarterly_data = df_selection.groupby(['Quarter', 'Category'])['Sales'].sum().reset_index()
            
            fig_quarterly = px.bar(
                quarterly_data,
                x="Quarter",
                y="Sales",
                color="Category",
                title="Quarterly Sales by Category",
                barmode="stack"
            )
            fig_quarterly.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                title_font_size=16
            )
            st.plotly_chart(fig_quarterly, use_container_width=True)

with tab3:
    # Geographic analysis
    regional_performance = df_selection.groupby("Region").agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order Date": "count"
    }).reset_index()
    regional_performance.columns = ["Region", "Total Sales", "Total Profit", "Order Count"]
    regional_performance["Profit Margin"] = (regional_performance["Total Profit"] / 
                                           regional_performance["Total Sales"] * 100).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_regional_sales = px.bar(
            regional_performance,
            x="Region",
            y="Total Sales",
            title="🗺Sales by Region",
            color="Total Sales",
            color_continuous_scale="Blues"
        )
        fig_regional_sales.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_regional_sales, use_container_width=True)
    
    with col2:
        fig_regional_profit = px.bar(
            regional_performance,
            x="Region",
            y="Profit Margin",
            title="Profit Margin by Region",
            color="Profit Margin",
            color_continuous_scale="RdYlGn"
        )
        fig_regional_profit.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_regional_profit, use_container_width=True)
    
    # Regional performance table
    st.subheader("Regional Performance Summary")
    st.dataframe(regional_performance, use_container_width=True)

with tab4:
    # Performance analytics
    col1, col2 = st.columns(2)
    
    with col1:
        # Discount impact analysis
        discount_bins = pd.cut(df_selection['Discount'], bins=5, labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%'])
        discount_impact = df_selection.groupby(discount_bins).agg({
            'Sales': 'mean',
            'Profit': 'mean'
        }).reset_index()
        
        fig_discount = px.bar(
            discount_impact,
            x='Discount',
            y=['Sales', 'Profit'],
            title="🏷Impact of Discounts on Performance",
            barmode='group'
        )
        fig_discount.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_discount, use_container_width=True)
    
    with col2:
        # Sales distribution
        fig_dist = px.histogram(
            df_selection,
            x="Sales",
            nbins=30,
            title="Sales Distribution",
            color_discrete_sequence=['#667eea']
        )
        fig_dist.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12),
            title_font_size=16
        )
        st.plotly_chart(fig_dist, use_container_width=True)

with tab5:
    # Deep dive analytics
    st.subheader("🔍 Detailed Data Analysis")
    
    # Statistical summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Statistical Summary")
        stats_df = df_selection[['Sales', 'Profit', 'Discount']].describe()
        st.dataframe(stats_df, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Key Insights")
        
        # Calculate insights
        best_region = df_selection.groupby('Region')['Sales'].sum().idxmax()
        best_category = df_selection.groupby('Category')['Profit'].sum().idxmax()
        avg_discount_profitable = df_selection[df_selection['Profit'] > 0]['Discount'].mean() * 100
        
        insights = [
            f" **Best performing region**: {best_region}",
            f" **Most profitable category**: {best_category}",
            f" **Average discount on profitable sales**: {avg_discount_profitable:.1f}%",
            f" **Total transactions analyzed**: {len(df_selection):,}",
            f" **Overall profit margin**: {profit_margin:.1f}%"
        ]
        
        for insight in insights:
            st.markdown(insight)
    
    # Raw data viewer
    st.subheader("Raw Data Viewer")
    
    # Search functionality
    search_term = st.text_input("Search in data:", "")
    if search_term:
        mask = df_selection.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        filtered_df = df_selection[mask]
    else:
        filtered_df = df_selection
    
    # Display data with pagination
    page_size = st.selectbox("Rows per page:", [10, 25, 50, 100], index=1)
    
    if len(filtered_df) > 0:
        total_pages = len(filtered_df) // page_size + (1 if len(filtered_df) % page_size > 0 else 0)
        page = st.number_input("Page:", min_value=1, max_value=total_pages, value=1) - 1
        
        start_idx = page * page_size
        end_idx = start_idx + page_size
        
        st.dataframe(
            filtered_df.iloc[start_idx:end_idx],
            use_container_width=True
        )
        
        st.caption(f"Showing {start_idx + 1}-{min(end_idx, len(filtered_df))} of {len(filtered_df)} records")
    else:
        st.info("No records match your search criteria.")

# ------------------------
# Export Section
# ------------------------
st.markdown("---")
st.subheader("Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Export Filtered Data"):
        csv = df_selection.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

with col2:
    if st.button("Export Summary Report"):
        summary_data = {
            'Metric': ['Total Sales', 'Total Profit', 'Profit Margin', 'Total Orders', 'Avg Order Value'],
            'Value': [f"${total_sales:,.0f}", f"${total_profit:,.0f}", f"{profit_margin:.1f}%", 
                     f"{total_orders:,}", f"${avg_order_value:.0f}"]
        }
        summary_df = pd.DataFrame(summary_data)
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="Download Summary",
            data=csv,
            file_name=f"sales_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #64748b; font-size: 0.9rem; margin-top: 2rem;'>
        Executive Sales Dashboard | Built with Streamlit & Plotly | Last Updated: {}
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M")),
    unsafe_allow_html=True
)

