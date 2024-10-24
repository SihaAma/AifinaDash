#%%
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st



if 'data' not in st.session_state or st.session_state.data is None:
    st.warning("Please upload a CSV file on the main page.")
    st.stop()

# Use the data and filters from session state
df = st.session_state.data
current_month = st.session_state.selected_month
current_year = st.session_state.selected_year

def preprocess_kpi():
    
    # Define account categories
    revenue_accounts = ['Sales Revenue']
    expense_accounts = ['Cost of Goods Sold', 'Operating Expenses']
    expense_accounts_full = ['Cost of Goods Sold', 'Operating Expenses', 'Interest', 'Taxes', 'Depreciation', 'Amortization']

    # Group the data by 'Year-Month'
    grouped = df.groupby('Year-Month')

    # Initialize lists to store KPI values
    kpi_list = []

    for name, group in grouped:
        # Calculate KPIs
        sales = calculate_sales_revenue(group)
        cogs = calculate_cogs(group)
        margin = calculate_margin(sales, cogs)
        ebitda = calculate_ebitda(group, revenue_accounts, expense_accounts)
        net_result = calculate_net_result(group, expense_accounts_full)
        dso = calculate_dso(group, sales)
        dio = calculate_dio(group, cogs)
        dpo = calculate_dpo(group, cogs)
        ccc = calculate_ccc(dio, dso, dpo)
        cash = calculate_cash_position(group)
        shareholders_equity = calculate_shareholders_equity(group)
        total_assets = calculate_total_assets(group)
        total_debt = calculate_total_debt(group)
        roe = (net_result / shareholders_equity) * 100 if shareholders_equity != 0 else 0
        roa = (net_result / total_assets) * 100 if total_assets != 0 else 0
        debt_to_equity = total_debt / shareholders_equity if shareholders_equity != 0 else 0
        accounts_payable = group[group['Account'] == 'accounts payable']['Debit'].sum() - group[group['Account'] == 'accounts payable']['Credit'].sum()
        current_liabilities = accounts_payable + group[group['Account'] == 'short-term debt']['Debit'].sum() - group[group['Account'] == 'short-term debt']['Credit'].sum()
        accounts_receivable = group[group['Account'] == 'accounts receivable']['Credit'].sum() - group[group['Account'] == 'accounts receivable']['Debit'].sum()
        quick_ratio = calculate_quick_ratio(cash, accounts_receivable, current_liabilities)
        
        # Placeholder values for Available Credit Line and Overdraft Availability
        available_credit_line = 1000000  # Replace with actual data or calculations
        overdraft_availability = 500000  # Replace with actual data or calculations
        
        # Append to KPI list
        kpi_list.append({
            'Month': group['Month'].iloc[0],
            'Year': group['Year'].iloc[0],
            'Year-Month': name,
            'Sales Revenue': sales,
            'Margin (%)': margin,
            'EBITDA': ebitda,
            'Net Result': net_result,
            'DSO (days)': dso,
            'DIO (days)': dio,
            'DPO (days)': dpo,
            'CCC (days)': ccc,
            'Cash Position': cash,
            'Available Credit Line': available_credit_line,
            'Overdraft Availability': overdraft_availability,
            'ROE (%)': roe,
            'ROA (%)': roa,
            'Debt to Equity Ratio': debt_to_equity,
            'Quick Ratio': quick_ratio
        })

    # Create KPI DataFrame
    kpi_df = pd.DataFrame(kpi_list)
    #st.write(kpi_df)

    # Calculate Revenue per Product per Month
    revenue_per_product_list = []
    for name, group in grouped:
        sales_revenue = group[group['Account'] == 'sales revenue']
        revenue_product = sales_revenue.groupby('Component')['Credit'].sum() - sales_revenue.groupby('Component')['Debit'].sum()
        revenue_product = revenue_product.reset_index().rename(columns={0: 'Revenue'})
        revenue_product['Year-Month'] = name
        revenue_per_product_list.append(revenue_product)
    revenue_per_product_df = pd.concat(revenue_per_product_list, ignore_index=True)

    # Calculate Top Clients by Revenue per Month
    top_clients_list = []
    for name, group in grouped:
        sales_revenue = group[group['Account'] == 'sales revenue']
        clients_revenue = sales_revenue.groupby('Supplier/client')['Credit'].sum() - sales_revenue.groupby('Supplier/client')['Debit'].sum()
        top_clients = clients_revenue.sort_values(ascending=False).head(5).reset_index().rename(columns={0: 'Revenue'})
        top_clients['Year-Month'] = name
        top_clients_list.append(top_clients)
    top_clients_by_revenue_df = pd.concat(top_clients_list, ignore_index=True)

    # Save the dataframes to csv
    #revenue_per_product_df.to_csv(f'{output_folder}/revenue_per_product.csv', index=False)
    #top_clients_by_revenue_df.to_csv(f'{output_folder}/top_clients_by_revenue.csv', index=False)
    #kpi_df.to_csv(f'{output_folder}/kpi.csv', index=False)
    #print("Data processed successfully!")
    #print(f"Revenue per Product: {revenue_per_product_df.head()}")
    #print(f"Top Clients by Revenue: {top_clients_by_revenue_df.head()}")
    #print(f"KPI: {kpi_df.head()}")
    return kpi_df, revenue_per_product_df, top_clients_by_revenue_df

# Define the KPI calculation functions here (unchanged from the original script)
def calculate_sales_revenue(group):
    sales_revenue = group[group['Account'] == 'sales revenue']
    total_sales = -sales_revenue['Solde'].sum()
    return total_sales

def calculate_cogs(group):
    cogs = group[group['Account'] == 'cost of goods sold']['Debit'].sum()
    return cogs

def calculate_margin(sales, cogs):
    if sales != 0:
        return ((sales - cogs) / sales) * 100
    else:
        return 0

def calculate_ebitda(group, revenue_accounts, expense_accounts):
    total_revenue = group[group['Account'].isin(revenue_accounts)]['Solde'].sum()
    total_operating_expenses = group[group['Account'].isin(expense_accounts)]['Solde'].sum()
    ebitda = total_revenue - total_operating_expenses
    return ebitda

def calculate_net_result(group, expense_accounts_full):
    total_revenue = group[group['Account'] == 'sales revenue']['Solde'].sum() 
    total_expenses = group[group['Account'].isin(expense_accounts_full)]['Solde'].sum() 
    net_result = total_revenue - total_expenses
    return net_result

def calculate_dso(group, sales):
    accounts_receivable = group[group['Account'] == 'accounts receivable']['Credit'].sum() - group[group['Account'] == 'accounts receivable']['Debit'].sum()
    dso = (accounts_receivable / sales) * 30 if sales != 0 else 0
    return dso

def calculate_dio(group, cogs):
    inventory_accounts = ['Raw material inventory', 'Inventory']
    inventory = group[group['Account'].isin(inventory_accounts)]['Debit'].sum() - group[group['Account'].isin(inventory_accounts)]['Credit'].sum()
    dio = (inventory / cogs) * 30 if cogs != 0 else 0
    return dio

def calculate_dpo(group, cogs):
    accounts_payable = group[group['Account'] == 'accounts payable']['Debit'].sum() - group[group['Account'] == 'accounts payable']['Credit'].sum()
    dpo = (accounts_payable / cogs) * 30 if cogs != 0 else 0
    return dpo

def calculate_ccc(dio, dso, dpo):
    return dio + dso - dpo

def calculate_cash_position(group):
    cash = group[group['Account'] == 'cash and cash equivalents']['Credit'].sum() - group[group['Account'] == 'cash and cash equivalents']['Debit'].sum()
    return cash

def calculate_shareholders_equity(group):
    share_capital = group[group['Account'] == 'share capital']['Credit'].sum() - group[group['Account'] == 'share capital']['Debit'].sum()
    retained_earnings = group[group['Account'] == 'retained earnings']['Credit'].sum() - group[group['Account'] == 'retained earnings']['Debit'].sum()
    shareholders_equity = share_capital + retained_earnings
    return shareholders_equity

def calculate_total_assets(group):
    asset_accounts = ['cash and cash equivalents', 'accounts receivable', 'raw material inventory', 
                      'inventory', 'property, plant, and equipment (ppe)', 'intangible assets']
    total_assets = group[group['Account'].isin(asset_accounts)]['Credit'].sum() - group[group['Account'].isin(asset_accounts)]['Debit'].sum()
    return total_assets

def calculate_total_debt(group):
    short_term_debt = group[group['Account'] == 'short-term debt']['Debit'].sum() - group[group['Account'] == 'short-term debt']['Credit'].sum()
    long_term_debt = group[group['Account'] == 'long-term debt']['Debit'].sum() - group[group['Account'] == 'long-term debt']['Credit'].sum()
    total_debt = short_term_debt + long_term_debt
    return total_debt

def calculate_quick_ratio(cash, accounts_receivable, current_liabilities):
    if current_liabilities != 0:
        return (cash + accounts_receivable) / current_liabilities
    else:
        return 0

if __name__ == "__main__":
    preprocess_kpi('data/journalEntry.csv', 'data')