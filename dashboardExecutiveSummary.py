# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px


if 'data' not in st.session_state or st.session_state.data is None:
    st.warning("Please upload a CSV file on the main page.")
    st.stop()

# Use the data and filters from session state
#df = st.session_state.data
#current_month = st.session_state.selected_month
#current_year = st.session_state.selected_year

def display_bs(balance_sheet_df):
    st.header("💼 Balance Sheet")
    st.dataframe(balance_sheet_df)



def display_es(kpi_df, pl_df):
    st.header("🔑 Key Performance Indicators (KPIs)")
    current_month = st.session_state.selected_month
    current_year = st.session_state.selected_year
    filtered_kpi = kpi_df[
        (kpi_df['Month'] == current_month) &
        (kpi_df['Year'] == current_year)
    ]

    # Filter and display KPIs in a table
    st.dataframe(filtered_kpi.set_index('Year-Month'))

    # Visualizations using pl_df (unfiltered)
    st.subheader("💰 Sales Revenue Over Time")
    fig_sales = px.line(pl_df, x='Year-Month', y='Sales Revenue', title='Sales Revenue Over Time')
    st.plotly_chart(fig_sales, use_container_width=True, key="sales_select")

    st.subheader("📈 Gross Margin Over Time")
    fig_margin = px.line(pl_df, x='Year-Month', y='Gross Margin (%)', title='Gross Margin Over Time')
    st.plotly_chart(fig_margin, use_container_width=True, key="margin_select")

    st.subheader("📊 EBITDA Over Time")
    fig_ebitda = px.bar(pl_df, x='Year-Month', y='EBITDA', title='EBITDA Over Time')
    st.plotly_chart(fig_ebitda, use_container_width=True, key="ebitda_select")

    st.subheader("📉 Net Result Over Time")
    fig_net = px.line(pl_df, x='Year-Month', y='Net Result', title='Net Result Over Time')
    st.plotly_chart(fig_net, use_container_width=True, key="net_result_select")

def display_pl(pl_df):
    st.header("Profit & Loss Statement")
    current_month = st.session_state.selected_month
    tab1, tab2 = st.tabs(["Page Profit & Loss","LTM Profit & Loss"])
    with tab1:
        st.header("Profit & Loss Statement")
        current_month = st.session_state.selected_month
        current_year = st.session_state.selected_year
        filtered_pl = pl_df[
            (pl_df['Month'] == current_month) &
            (pl_df['Year'] == current_year)
        ]


        # Filter and display P&L in a table
        #filtered_pl = pl_df[pl_df['Year-Month'].isin(current_month)]
        st.dataframe(filtered_pl.set_index('Year-Month'))

        # Visualizations using pl_df (unfiltered)
        st.subheader("📊 Revenue vs. Expenses Over Time")
        fig_rev_exp = px.line(pl_df, x='Year-Month', y=['Sales Revenue', 'Cost of Goods Sold', 'Gross Margin'],
                                title='Revenue vs. Expenses Over Time')
        st.plotly_chart(fig_rev_exp, use_container_width=True, key="rev_exp_select")

        st.subheader("💰 Operating Expenses Breakdown")
        fig_opex = px.area(pl_df, x='Year-Month', y=['Personnel', 'Facility', 'Administration'],
                            title='Operating Expenses Breakdown')
        st.plotly_chart(fig_opex, use_container_width=True, key="opex_select")
    with tab2:
        st.header(" Profit & Loss Statement LTM")
        # Filter and display P&L in a table
        #filtered_pl = pl_df[pl_df['Year-Month'].dt.strftime('%Y-%m').isin(current_month)]
        st.dataframe(pl_df.set_index('Year-Month'))

        # Visualizations using pl_df (unfiltered)
        #st.subheader("📊 Revenue vs. Expenses Over Time")
        #fig_rev_exp = px.line(pl_df, x='Year-Month', y=['Sales Revenue', 'Cost of Goods Sold', 'Gross Margin'],
        #                        title='Revenue vs. Expenses Over Time')
       # st.plotly_chart(fig_rev_exp, use_container_width=True, key="rev_exp_select")

        st.subheader("💰 Operating Expenses Breakdown")
        fig_opex = px.area(pl_df, x='Year-Month', y=['Personnel', 'Facility', 'Administration'],
                            title='Operating Expenses Breakdown')
        st.plotly_chart(fig_opex, use_container_width=True,key="pl_month_select")





def display_revenue(revenue_per_product_df,top_clients_by_revenue_df):
    

    # Additional visualizations (outside tabs, using unfiltered data)
    #st.header("📈 Additional Insights")

    st.subheader("🏆 Top 5 Clients by Revenue")
    fig_top_clients = px.bar(top_clients_by_revenue_df, x='Supplier/client', y='Revenue', color='Supplier/client',
                             title='Top 5 Clients by Revenue', animation_frame='Year-Month')
    st.plotly_chart(fig_top_clients, use_container_width=True)

    st.subheader("📦 Revenue per Product")
    # Group by component and sum revenue
    revenue_per_product = revenue_per_product_df.groupby('Component')['Revenue'].sum()
    fig_revenue_product = px.pie(revenue_per_product, names=revenue_per_product.index, values='Revenue',
                                 title='Total Revenue per Product')
    st.plotly_chart(fig_revenue_product, use_container_width=True, key="revenue_product_select")



