import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from calculations import financial_dashboard

def revenue_analysis_page():
    st.title("Revenue Analysis")

    # Load data
    @st.cache_data
    def load_data():
        df = pd.read_csv('data/journalEntry.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    df = load_data()

    # Sidebar controls
    st.sidebar.title("Analysis Controls")
    selected_month = st.sidebar.selectbox("Select Month", range(1, 13), format_func=lambda x: f"Month {x}")
    selected_year = st.sidebar.selectbox("Select Year", df['Year'].unique())

    # Filter data
    filtered_df = df[(df['Month'] == selected_month) & (df['Year'] == selected_year) & (df['Account'] == 'Sales Revenue')]

    # Calculate total revenue
    total_revenue = -filtered_df['Solde'].sum() / 1000  # Convert to K$

    st.metric("Total Revenue", f"${total_revenue:,.2f}K")

    # Revenue by client
    revenue_by_client = filtered_df.groupby('Supplier/client')['Solde'].sum().sort_values(ascending=False)
    revenue_by_client = -revenue_by_client / 1000  # Convert to K$ and make positive

    # Bar chart of revenue by client
    fig_bar = px.bar(revenue_by_client, x=revenue_by_client.index, y=revenue_by_client.values,
                     title="Revenue by Client",
                     labels={'x': 'Client', 'y': 'Revenue (K$)'})
    st.plotly_chart(fig_bar)

    # Pie chart of revenue distribution
    fig_pie = px.pie(values=revenue_by_client.values, names=revenue_by_client.index,
                     title="Revenue Distribution by Client")
    st.plotly_chart(fig_pie)

    # Table of revenue by client
    st.subheader("Revenue by Client")
    revenue_table = pd.DataFrame({
        'Client': revenue_by_client.index,
        'Revenue (K$)': revenue_by_client.values,
        'Percentage': revenue_by_client.values / total_revenue * 100
    })
    st.dataframe(revenue_table.style.format({'Revenue (K$)': '${:,.2f}', 'Percentage': '{:.2f}%'}))

    # Revenue evolution (if data available)
    st.subheader("Revenue Evolution")
    monthly_revenue = df[df['Account'] == 'Sales Revenue'].groupby(['Year', 'Month'])['Solde'].sum().reset_index()
    monthly_revenue['Revenue'] = -monthly_revenue['Solde'] / 1000  # Convert to K$ and make positive
    fig_line = px.line(monthly_revenue, x='Month', y='Revenue', color='Year',
                       title="Monthly Revenue Evolution",
                       labels={'Revenue': 'Revenue (K$)'})
    st.plotly_chart(fig_line)

if __name__ == "__main__":
    revenue_analysis_page()
