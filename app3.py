# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config (must be the first Streamlit command)
#st.set_page_config(page_title="CFO Financial Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    journal_entry_df = pd.read_csv('data/journalEntry.csv')
    budget_df = pd.read_csv('data/budget.csv')
    
    # Rename columns for consistency
    journal_entry_df.columns = [
        'Date', 'Month', 'Year', 'Journal Entry ID', 'Account',
        'Debit', 'Credit', 'Solde', 'Description',
        'Document Reference', 'Currency', 'Supplier/client', 'Component'
    ]
    
    # Convert 'Date' to datetime
    journal_entry_df['Date'] = pd.to_datetime(journal_entry_df['Date'])
    
    # Ensure 'Solde' is of type float
    journal_entry_df['Solde'] = journal_entry_df['Solde'].astype(float)
    
    return journal_entry_df, budget_df

journal_entry_df, budget_df = load_data()

# Sidebar for input parameters
st.sidebar.header("Dashboard Parameters")
valid_sales_accounts = budget_df.columns[1:]
sales_account = st.sidebar.selectbox("Sales Account", valid_sales_accounts)
cogs_account = st.sidebar.selectbox("Cost of Goods Sold Account", journal_entry_df['Account'].unique())
opex_accounts = st.sidebar.multiselect("Operating Expense Accounts", journal_entry_df['Account'].unique())
current_month = st.sidebar.slider("Current Month", 1, 12, 4)
current_year = st.sidebar.slider("Current Year", journal_entry_df['Year'].min(), journal_entry_df['Year'].max(), 2022)

# Calculate dashboard metrics
def calculate_dashboard_metrics(journal_df, budget_df, sales_account, cogs_account, opex_accounts, current_month, current_year):
    # Filter data for the selected month and year
    filtered_sales = journal_df[
        (journal_df['Account'] == sales_account) &
        (journal_df['Month'] == current_month) &
        (journal_df['Year'] == current_year)
    ]
    filtered_cogs = journal_df[
        (journal_df['Account'] == cogs_account) &
        (journal_df['Month'] == current_month) &
        (journal_df['Year'] == current_year)
    ]
    
    # Calculate metrics
    sales_revenue = -filtered_sales['Solde'].sum()
    sales_revenue_k = sales_revenue / 1000
    
    # Retrieve budget value
    if sales_account in budget_df.columns:
        budget_value = budget_df.loc[budget_df['Month'] == current_month, sales_account].values[0]
    else:
        budget_value = 0
        st.warning(f"No budget data found for {sales_account}")
    
    percentage_variance_budget = round(((sales_revenue_k - budget_value) / budget_value) * 100, 2) if budget_value != 0 else 0

    # Previous period calculations
    prev_month = 12 if current_month == 1 else current_month - 1
    prev_year = current_year - 1 if current_month == 1 else current_year
    filtered_prev_sales = journal_df[
        (journal_df['Account'] == sales_account) &
        (journal_df['Month'] == prev_month) &
        (journal_df['Year'] == prev_year)
    ]
    prev_sales_revenue = -filtered_prev_sales['Solde'].sum()
    prev_sales_revenue_k = prev_sales_revenue / 1000
    percentage_variance_previous = round(((sales_revenue_k - prev_sales_revenue_k) / prev_sales_revenue_k) * 100, 2) if prev_sales_revenue_k != 0 else 0
    
    # Margin calculations
    cogs = filtered_cogs['Solde'].sum()
    gross_margin = sales_revenue - cogs
    margin_percentage = (gross_margin / sales_revenue) * 100 if sales_revenue != 0 else 0
    
    # EBITDA calculations
    filtered_opex = journal_df[
        journal_df['Account'].isin(opex_accounts) &
        (journal_df['Month'] == current_month) &
        (journal_df['Year'] == current_year)
    ]
    operating_expenses = filtered_opex['Solde'].sum()
    ebitda = gross_margin - operating_expenses
    ebitda_k = ebitda / 1000
    ebitda_budget = budget_df.loc[budget_df['Month'] == current_month, 'EBITDA'].values[0]
    ebitda_variance_budget = round(((ebitda_k - ebitda_budget) / ebitda_budget) * 100, 2) if ebitda_budget != 0 else 0
    
    return {
        'Sales Revenue (K$)': round(sales_revenue_k, 2),
        'Budget (K$)': round(budget_value, 2),
        'Variance from Budget (%)': percentage_variance_budget,
        'Previous Sales Revenue (K$)': round(prev_sales_revenue_k, 2),
        'Variance from Previous (%)': percentage_variance_previous,
        'Margin (%)': round(margin_percentage, 2),
        'EBITDA (K$)': round(ebitda_k, 2),
        'EBITDA Variance from Budget (%)': ebitda_variance_budget,
    }

# Calculate and display metrics
metrics = calculate_dashboard_metrics(
    journal_entry_df, budget_df, sales_account, cogs_account, opex_accounts,
    current_month, current_year
)

# Styling the dashboard
st.markdown(
    """
    <style>
    .dashboard-container {
        background-color: #2a2a2a;
        padding: 20px;
        border-radius: 10px;
    }
    .kpi {
        color: white;
        font-size: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True
)

# Display KPIs
st.markdown("<div class='dashboard-container'><h2 style='text-align: center; color: white;'>Key Performance Indicators</h2></div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Sales Revenue",
    f"${metrics['Sales Revenue (K$)']:,.2f}K",
    f"{metrics['Variance from Previous (%)']}% vs Prev"
)
col2.metric(
    "Budget",
    f"${metrics['Budget (K$)']:,.2f}K",
    f"{metrics['Variance from Budget (%)']}% vs Budget"
)
col3.metric("Margin", f"{metrics['Margin (%)']}%")
col4.metric(
    "EBITDA",
    f"${metrics['EBITDA (K$)']:,.2f}K",
    f"{metrics['EBITDA Variance from Budget (%)']}% vs Budget"
)

# Additional metrics
st.markdown("<h3 style='text-align: center; color: white;'>Additional Metrics</h3>", unsafe_allow_html=True)

# Revenue and Expenses Over Time
revenue_expenses_df = journal_entry_df[
    journal_entry_df['Account'].isin([sales_account, cogs_account] + opex_accounts)
]
revenue_expenses_df = revenue_expenses_df.groupby(['Date', 'Account'])['Solde'].sum().reset_index()
revenue_expenses_df['Solde'] = revenue_expenses_df['Solde'].abs()

# Plotting with dark theme
fig_revenue_expenses = px.line(
    revenue_expenses_df,
    x='Date',
    y='Solde',
    color='Account',
    title='Revenue and Expenses Over Time',
    template='plotly_dark'
)
st.plotly_chart(fig_revenue_expenses, use_container_width=True)

# Display the filtered data table
st.markdown("<h2 style='text-align: center; color: white;'>Transaction Data</h2>", unsafe_allow_html=True)
st.dataframe(journal_entry_df)
