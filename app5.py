import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import st_tailwind as tw

# Set page config
#st.set_page_config(page_title="AIFINA Financial Dashboard", layout="wide")

# Custom CSS to ensure text visibility
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-title {
        font-size: 1rem;
        font-weight: 500;
        color: #4a5568;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.875rem;
        font-weight: 600;
        color: #1a202c;
        margin: 0.5rem 0;
    }
    .metric-detail {
        font-size: 0.875rem;
        color: #4a5568;
        margin: 0.25rem 0;
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }
    .down-arrow {
        color: #dc2626;
    }
    .up-arrow {
        color: #16a34a;
    }
    .hide-streamlit-elements div[data-testid="stToolbar"] {
        display: none;
    }
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0;
    }
    button {
        background-color: #2563eb !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sample data
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']
margin_data = [24, 23, 25, 26, 26, 26, 26, 25, 26, 26, 24]
ebitda_data = [100, 90, 110, 120, 115, 130, 125, 110, 120, 125, 95]
working_capital_data = {
    'dso': [74] * 11,
    'dio': [22] * 11,
    'dpo': [110] * 11
}

# Common chart layout
base_layout = dict(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#4a5568', size=10),
    xaxis=dict(
        gridcolor='#eee',
        showgrid=True,
        zeroline=False,
    ),
    yaxis=dict(
        gridcolor='#eee',
        showgrid=True,
        zeroline=False,
    ),
    margin=dict(l=40, r=20, t=20, b=20),
    height=200
)

# Create three columns
col1, col2, col3 = st.columns(3)

# Margin Section
with col1:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Margin</div>
            <div class="metric-value">24.44%</div>
            <div class="metric-detail">
                Budget: 24.85% <span class="down-arrow">↓ 2%</span>
            </div>
            <div class="metric-detail">
                Previous period: 26% <span class="down-arrow">↓ 7%</span>
            </div>
            <div class="metric-detail">
                Year-to-date: 26%
            </div>
    """, unsafe_allow_html=True)
    
    fig_margin = go.Figure()
    fig_margin.add_trace(go.Scatter(
        x=months,
        y=margin_data,
        mode='lines+markers',
        line=dict(color='#2563eb', width=1.5),
        marker=dict(size=4)
    ))
    
    margin_layout = base_layout.copy()
    margin_layout.update(
        showlegend=False,
        yaxis=dict(range=[0, 30])
    )
    fig_margin.update_layout(margin_layout)
    st.plotly_chart(fig_margin, use_container_width=True)
    
    st.button("Details", key="margin_details")
    st.markdown("</div>", unsafe_allow_html=True)

# EBITDA Section
with col2:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">EBITDA</div>
            <div class="metric-value">99.69 K$</div>
            <div class="metric-detail">
                Budget: 115.14 K$ <span class="down-arrow">↓ 13%</span>
            </div>
            <div class="metric-detail">
                Previous period: 338.85 K$ <span class="up-arrow">↑ 71%</span>
            </div>
            <div class="metric-detail">
                Year-to-date: 5,435.77 K$
            </div>
    """, unsafe_allow_html=True)
    
    fig_ebitda = go.Figure()
    fig_ebitda.add_trace(go.Bar(
        x=months,
        y=ebitda_data,
        marker_color='#818cf8'
    ))
    
    ebitda_layout = base_layout.copy()
    ebitda_layout.update(
        showlegend=False,
        bargap=0.4
    )
    fig_ebitda.update_layout(ebitda_layout)
    st.plotly_chart(fig_ebitda, use_container_width=True)
    
    st.button("Details", key="ebitda_details")
    st.markdown("</div>", unsafe_allow_html=True)

# Working Capital Section
with col3:
    st.markdown("""
        <div class="metric-card">
            <div class="metric-title">Working Capital</div>
            <div class="metric-value">-14</div>
            <div class="metric-detail">DSO: 74</div>
            <div class="metric-detail">DIO: 22</div>
            <div class="metric-detail">DPO: 110</div>
    """, unsafe_allow_html=True)
    
    fig_wc = go.Figure()
    fig_wc.add_trace(go.Scatter(
        x=months,
        y=working_capital_data['dso'],
        name='DSO',
        line=dict(color='#f43f5e', width=1.5)
    ))
    fig_wc.add_trace(go.Scatter(
        x=months,
        y=working_capital_data['dio'],
        name='DIO',
        line=dict(color='#22c55e', width=1.5)
    ))
    fig_wc.add_trace(go.Scatter(
        x=months,
        y=working_capital_data['dpo'],
        name='DPO',
        line=dict(color='#3b82f6', width=1.5)
    ))
    
    wc_layout = base_layout.copy()
    wc_layout.update(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig_wc.update_layout(wc_layout)
    st.plotly_chart(fig_wc, use_container_width=True)
    
    st.button("Details", key="wc_details")
    st.markdown("</div>", unsafe_allow_html=True)

# AI Insights section
st.markdown('<div style="height: 2rem"></div>', unsafe_allow_html=True)
st.markdown("### AI Insights")
insight_cols = st.columns(3)

with insight_cols[0]:
    st.markdown("""
    <div class="metric-card">
        In November, margin performance reflects a -2% impact from a slight decline in revenue, equating to -19 K$. 
        The revenue impact was largely offset by cost efficiencies, which contributed +220 K$ to the margin. 
        While the revenue dip was minimal, the cost management efforts helped limit the overall impact on margins.
    </div>
    """, unsafe_allow_html=True)

with insight_cols[1]:
    st.markdown("""
    <div class="metric-card">
        November's performance highlights the continued importance of cost control in maintaining profitability, 
        as pricing recovery remains a significant challenge. The company has made some strides in restoring sales volumes, 
        but the inability to fully recover price increases continues to weigh on margins.
    </div>
    """, unsafe_allow_html=True)

with insight_cols[2]:
    st.markdown("""
    <div class="metric-card">
        Tighter payment terms or restrictions on credit, should be considered for these clients. 
        The YTD insight indicates that despite earlier improvements, these efforts continue to push the DSO up, 
        threatening year-end liquidity. Without tighter control, the company may face the need for external financing 
        to bridge cash flow gaps.
    </div>
    """, unsafe_allow_html=True)
