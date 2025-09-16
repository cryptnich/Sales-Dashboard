# KPI Section
st.markdown("### Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Total Sales</h4>
        <p class='big-number'>${total_sales:,.0f}</p>
        <p class='small-note'>Change: {sales_delta:+.1f}%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Avg Order Value</h4>
        <p class='big-number'>${avg_order_value:,.2f}</p>
        <p class='small-note'>Based on transactions</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Total Customers</h4>
        <p class='big-number'>{total_customers:,}</p>
        <p class='small-note'>Unique buyers</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <h4>Conversion Rate</h4>
        <p class='big-number'>{conversion_rate:.1f}%</p>
        <p class='small-note'>vs last month</p>
    </div>
    """, unsafe_allow_html=True)
