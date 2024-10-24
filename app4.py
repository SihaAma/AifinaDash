import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from calculations import financial_dashboard



# Check if data is available in session state
if 'data' not in st.session_state or st.session_state.data is None:
    st.warning("Please upload a CSV file on the main page.")
    st.stop()

# Use the data and filters from session state
df = st.session_state.data
current_month = st.session_state.selected_month
current_year = st.session_state.selected_year

# Get financial data
sales_account = 'Sales Revenue'
cogs_account = 'Cost of goods sold'
opex_accounts = ['Personnel', 'Facility', 'Administration']
current_month = 11  # November
current_year = 2022

dashboard_data = financial_dashboard(df, sales_account, cogs_account, opex_accounts, current_month, current_year)

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

metrics = [
    ("Margin", f"{dashboard_data['Margin (%)']}%", "24.85%", "26%", "26%"),
    ("EBITDA", "99.69 K$", "115.14 K$", "338.85 K$", "5,435.77 K$"),
    ("Working Capital", "-14", "DSO: 74", "DIO: 22", "DPO: 110")
]

for i, (label, value, budget, prev, ytd) in enumerate(metrics):
    col = [col1, col2, col3][i]
    with col:
        st.markdown(f"""
        <div class="bg-white rounded-lg shadow p-6 mb-4">
            <h3 class="text-xl font-semibold mb-2">{label}</h3>
            <p class="text-3xl font-bold mb-4">{value}</p>
            <p class="text-sm text-gray-600">Budget: {budget}</p>
            <p class="text-sm text-gray-600">Previous period: {prev}</p>
            <p class="text-sm text-gray-600">Year-to-date: {ytd}</p>
        </div>
        """, unsafe_allow_html=True)

# Charts
charts_data = pd.read_csv('data/budget.csv')

def create_chart(data, x, y, title, chart_type='scatter'):
    fig = go.Figure()
    if chart_type == 'scatter':
        fig.add_trace(go.Scatter(x=data[x], y=data[y], mode='lines+markers', line=dict(color='#3b82f6')))
    elif chart_type == 'bar':
        fig.add_trace(go.Bar(x=data[x], y=data[y], marker_color='#3b82f6'))
    fig.update_layout(
        title=title,
        xaxis_title='Month',
        yaxis_title=y,
        height=300,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#111827'),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig

charts = [
    create_chart(charts_data, 'Month', 'Margin (%)', 'Margin'),
    create_chart(charts_data, 'Month', 'EBITDA', 'EBITDA', 'bar'),
    create_chart(charts_data, 'Month', 'Sales Revenue', 'Working Capital')
]

for i, chart in enumerate(charts):
    col = [col1, col2, col3][i]
    with col:
        st.plotly_chart(chart, use_container_width=True, config={'displayModeBar': False})

# AI Insights
insights = [
    "In November, margin performance reflects a -2% impact from a slight decline in revenue, equating to -19 K$. The revenue impact was largely offset by cost efficiencies, which contributed +220 K$ to the margin. While the revenue dip was minimal, the cost management efforts helped limit the overall impact on margins.",
    "November's performance highlights the continued importance of cost control in maintaining profitability, as pricing recovery remains a significant challenge. The company has made some strides in restoring sales volumes, but the inability to fully recover price increases continues to weigh on margins.",
    "Tighter payment terms or restrictions on credit, should be considered for these clients. The YTD insight indicates that despite earlier improvements, these efforts continue to push the DSO up, threatening year-end liquidity. Without tighter control, the company may face the need for external financing to bridge cash flow gaps."
]

for i, insight in enumerate(insights):
    col = [col1, col2, col3][i]
    with col:
        st.markdown(f"""
        <div class="bg-white rounded-lg shadow p-4 mb-4">
            <h4 class="text-lg font-semibold mb-2">AI Insights</h4>
            <p class="text-sm">{insight}</p>
            <button class="mt-4 bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
                Details
            </button>
        </div>
        """, unsafe_allow_html=True)

# You may need to adjust the file paths and data processing based on your actual data structure and file locations.
