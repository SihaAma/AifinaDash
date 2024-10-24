import streamlit as st
import pandas as pd
import os
from KPI import preprocess_kpi
from PL import preprocess_pl
from BS import preprocess_bs
from dashboardExecutiveSummary import display_es, display_pl, display_revenue, display_bs
#st.set_page_config(page_title="Financial Dashboard AIFINA v2", page_icon="💰")

#st.set_page_config(page_title="Financial Dashboard", layout="wide")

#st.title("📊 Financial Dashboard")

# File uploader
#uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

#if uploaded_file is not None:
    # Save the uploaded file
    #with open("data/journalEntry.csv", "wb") as f:
    #     f.write(uploaded_file.getbuffer())
    
    #st.success("File uploaded successfully!")

# Check if data is available before processing
if st.session_state.data is not None:
    with st.spinner("Processing data..."):
        df = st.session_state.data
        profit_loss_df = preprocess_pl(df)
        balance_sheet_df = preprocess_bs(df, profit_loss_df)
        kpi_df, revenue_per_product_df, top_clients_by_revenue_df = preprocess_kpi(profit_loss_df, balance_sheet_df)

    # Use a unique key for the selectbox
    page = st.sidebar.selectbox("Choose a page", ["Profit & Loss", "Balance Sheet"], key="page_selection")

    if page == "Profit & Loss":
        display_pl(profit_loss_df)
    elif page == "Balance Sheet":
        display_bs(balance_sheet_df)
    display_revenue(revenue_per_product_df, top_clients_by_revenue_df)

else:
    st.info("Please upload a CSV file to begin.")

#display_dashboard(kpi_df, profit_loss_df, revenue_per_product_df, top_clients_by_revenue_df)
#kpi = st.Page("app4.py", title="Visualization", icon="📊")
#pnl = st.Page("dashboard.py", title="P&L", icon="💰")
#pg = st.navigation([kpi, pnl])
    


#else:
#    st.info("Please upload a CSV file to begin.")

#pg.run()
