import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calculations import financial_dashboard
from revenue_analysis import revenue_analysis_page
from KPI import preprocess_kpi
from PL import preprocess_pl
from dashboardExecutiveSummary import display_dashboard

# Set page config
#st.set_page_config(page_title="Financial Dashboard", page_icon=":bar_chart:", layout="wide")

# Navigation
page = st.sidebar.selectbox("Choose a page", ["Executive Summary", "Profit & Loss"])

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if page == "Executive Summary":
    # Load data
    @st.cache_data
    def load_data():
        df = pd.read_csv('data/budget.csv')
        return df

    budget_df = load_data()

    # Sidebar
    st.sidebar.title("Dashboard Controls")
    selected_month = st.sidebar.selectbox("Select Month", range(1, 13), format_func=lambda x: f"Month {x}")
    selected_year = st.sidebar.selectbox("Select Year", [2022])

    # Calculate financial metrics
    sales_account = 'Sales Revenue'
    cogs_account = 'Cost of goods sold'
    opex_accounts = ['Personnel', 'Facility', 'Administration']
    metrics = financial_dashboard(sales_account, cogs_account, opex_accounts, selected_month, selected_year)

    # Main dashboard
    st.title("CEO Financial Dashboard")

    # Display selected month and year
    st.subheader(f"Showing data for Month {selected_month}, {selected_year}")

    # KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sales Revenue", f"${metrics['Sales Revenue (K$)']:,.2f}K")
    with col2:
        st.metric("Budget", f"${metrics['Budget (K$)']:,.2f}K")
    with col3:
        st.metric("Variance from Budget", f"{metrics['Variance from Budget (%)']}%")
    with col4:
        st.metric("Margin", f"{metrics['Margin (%)']:.2f}%")

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("EBITDA", f"${metrics['EBITDA (K$)']:,.2f}K")
    with col6:
        st.metric("DSO", f"{metrics['DSO (days)']} days")
    with col7:
        st.metric("DIO", f"{metrics['DIO (days)']} days")
    with col8:
        st.metric("DPO", f"{metrics['DPO (days)']} days")

    # Charts
    st.subheader("Monthly Financial Performance")

    # Line chart for Sales Revenue, Cost of Goods Sold, and EBITDA
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Scatter(x=budget_df['Month'], y=budget_df['Sales Revenue'], mode='lines+markers', name='Sales Revenue'))
    fig_monthly.add_trace(go.Scatter(x=budget_df['Month'], y=budget_df['Cost of goods sold'], mode='lines+markers', name='Cost of Goods Sold'))
    fig_monthly.add_trace(go.Scatter(x=budget_df['Month'], y=budget_df['EBITDA'], mode='lines+markers', name='EBITDA'))
    fig_monthly.update_layout(title='Monthly Sales, COGS, and EBITDA', xaxis_title='Month', yaxis_title='Amount')
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Bar chart for Gross Margin %
    fig_margin = px.bar(budget_df, x='Month', y='Margin (%)', title='Monthly Gross Margin %')
    st.plotly_chart(fig_margin, use_container_width=True)

    # Pie chart for Expenses
    expenses_df = budget_df[['Personnel', 'Facility', 'Administration']].sum()
    fig_expenses = px.pie(values=expenses_df.values, names=expenses_df.index, title='Expense Breakdown')
    st.plotly_chart(fig_expenses, use_container_width=True)

    # Table with monthly data
    st.subheader("Monthly Financial Data")
    st.dataframe(budget_df)

elif page == "Profit & Loss":
    revenue_analysis_page()

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit and Plotly")
