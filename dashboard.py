import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import time

# Page Configuration

st.set_page_config(
    page_title="Executive Sales Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# CSS for styling and animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
    
    body, .main, .block-container {
        background-color: #ffffff !important;
    }

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

# Load Data with Error Handling

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

# Header with animatio
st.markdown('<h1 class="main-header">EXECUTIVE SALES DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time Business Intelligence & Performance Analytics</p>', unsafe_allow_html=True)

