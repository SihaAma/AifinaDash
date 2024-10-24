import streamlit as st
from st_pages import add_page_title, get_nav_from_toml
import pandas as pd

st.set_page_config(layout="wide", page_title="AIFINA Financial Dashboard")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = None
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = None

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    # Step 2: Data Cleaning
    numeric_cols = ['Debit', 'Credit', 'Solde']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    string_cols = ['Account', 'Supplier/client', 'Component']
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract Month and Year if not already present
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year

    # Add 'Year-Month' column for easier grouping
    df['Year-Month'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)

    # Lowercase account column for consistency
    df['Account'] = df['Account'].str.lower()


    st.session_state.data = df
    
    st.sidebar.header("Filter Options")

    # Get unique Year-Month values and sort them
    months = sorted(df['Year-Month'].unique())
    
    # Set default months to those starting with '2022'
    default_months = [month for month in months if month.startswith('2022')]
    
    #st.session_state.selected_month = st.sidebar.multiselect(
    #    "Select Month(s):", 
    #    options=months, 
    #    default=default_months
    #)
    currentmonth = st.sidebar.slider("Current Month", 1, 12, 4)
    current_year = st.sidebar.slider("Current Year", df['Year'].min(), df['Year'].max(), 2022)
    st.session_state.selected_year = current_year
    st.session_state.selected_month = currentmonth



    st.success("Data loaded and filtered successfully!")

# Navigation
nav = get_nav_from_toml(".streamlit/pages_sections.toml")
pg = st.navigation(nav)

add_page_title(pg)

pg.run()