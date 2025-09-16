st.markdown("""
<style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
    }

    /* Header */
    .main-header {
        font-size: 2.4rem;
        font-weight: 700;
        color: #222222;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555555;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* KPI Metric Cards */
    .metric-card {
        background: #f9fafb;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
        text-align: center;
    }
    .metric-card h4 {
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
        color: #333333;
    }
    .metric-card p {
        margin: 0.2rem 0;
    }
    .metric-card .big-number {
        font-size: 1.4rem;
        font-weight: 700;
        color: #111111;
    }
    .metric-card .small-note {
        font-size: 0.85rem;
        color: #666666;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0 18px;
        background-color: #f3f4f6;
        border-radius: 5px;
        border: 1px solid #d1d5db;
        color: #333333;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4ade80 !important;  /* soft green highlight */
        color: white !important;
        border: none !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #666666;
        font-size: 0.9rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)
