import pandas as pd
import numpy as np
import streamlit as st



def preprocess_bs(df, profit_loss_df):
    # Step 1: Load the Data
    # (Assuming df is already loaded and available)
    #ltmPL = st.session_state.profit_loss

    # Step 3: Define KPI Calculation Functions
    def calculate_cash_and_cash_equivalents(df):
        cash = df[df['Account'].str.lower() == 'cash and cash equivalents'].groupby('Year-Month')['Solde'].sum().reset_index()
        cash['cash and cash equivalents'] = cash['Solde']
        return cash[['Year-Month', 'cash and cash equivalents']]

    def calculate_accounts_receivable(df):
        ar = df[df['Account'].str.lower() == 'accounts receivable'].groupby('Year-Month')['Solde'].sum().reset_index()
        ar.rename(columns={'Solde': 'accounts receivable'}, inplace=True)
        return ar[['Year-Month', 'accounts receivable']]

    def calculate_raw_material_inventory(df):
        inventory = df[df['Account'].str.lower() == 'raw material inventory'].groupby('Year-Month')['Solde'].sum().reset_index()
        inventory.rename(columns={'Solde': 'raw material inventory'}, inplace=True)
        return inventory[['Year-Month', 'raw material inventory']]

    def calculate_ppe(df):
        ppe = df[df['Account'].str.lower() == 'property, plant, and equipment (ppe)'].groupby('Year-Month')['Solde'].sum().reset_index()
        ppe.rename(columns={'Solde': 'ppe'}, inplace=True)
        return ppe[['Year-Month', 'ppe']]

    def calculate_intangible_assets(df):
        intangible = df[df['Account'].str.lower() == 'intangible assets'].groupby('Year-Month')['Solde'].sum().reset_index()
        intangible.rename(columns={'Solde': 'intangible assets'}, inplace=True)
        return intangible[['Year-Month', 'intangible assets']]

    def calculate_accounts_payable(df):
        ap = df[df['Account'].str.lower() == 'accounts payable'].groupby('Year-Month')['Solde'].sum().reset_index()
        ap.rename(columns={'Solde': 'accounts payable'}, inplace=True)
        return ap[['Year-Month', 'accounts payable']]

    def calculate_short_term_debt(df):
        std = df[df['Account'].str.lower() == 'short-term debt'].groupby('Year-Month')['Solde'].sum().reset_index()
        std.rename(columns={'Solde': 'short-term debt'}, inplace=True)
        return std[['Year-Month', 'short-term debt']]

    def calculate_wages_payables(df):
        wp = df[df['Account'].str.lower() == 'wages payables'].groupby('Year-Month')['Solde'].sum().reset_index()
        wp.rename(columns={'Solde': 'wages payables'}, inplace=True)
        return wp[['Year-Month', 'wages payables']]

    def calculate_share_capital(df):
        sc = df[df['Account'].str.lower() == 'share capital'].groupby('Year-Month')['Solde'].sum().reset_index()
        #sc['share capital'] = -sc['Solde']
        sc.rename(columns={'Solde': 'share capital'}, inplace=True)
        return sc[['Year-Month', 'share capital']]

    def calculate_retained_earnings(df):
        re = df[df['Account'].str.lower() == 'retained earnings'].groupby('Year-Month')['Solde'].sum().reset_index()
        
        re.rename(columns={'Solde': 'retained earnings'}, inplace=True)
        return re[['Year-Month', 'retained earnings']]

    def calculate_net_income(profit_loss_df):
        #revenue_accounts = ['sales revenue']
        #expense_accounts = ['cost of goods sold', 'administration', 'financial cost', 'personnel', 'facility']
        
        #revenues = df[df['Account'].str.lower().isin(revenue_accounts)].groupby('Year-Month')['Solde'].sum().reset_index()
        #revenues.rename(columns={'Solde': 'total revenue'}, inplace=True)
        
        #expenses = df[df['Account'].str.lower().isin(expense_accounts)].groupby('Year-Month')['Solde'].sum().reset_index()
        #expenses.rename(columns={'Solde': 'total expenses'}, inplace=True)
        
        #net_income = pd.merge(revenues, expenses, on='Year-Month', how='outer').fillna(0)
        #net_income['net income'] = net_income['total revenue'] - net_income['total expenses']
        #net_income['cumulative net income'] = net_income['net income'].cumsum()
        net_income = profit_loss_df[['Year-Month', 'Net Result']]
        net_income.rename(columns={'Net Result': 'net income'}, inplace=True)
        net_income['cumulative net income'] = net_income['net income'].cumsum()
        return net_income[['Year-Month', 'net income', 'cumulative net income']]

    # Step 4: Calculate Balance Sheet Items
    cash = calculate_cash_and_cash_equivalents(df)
    ar = calculate_accounts_receivable(df)
    inventory = calculate_raw_material_inventory(df)
    ppe = calculate_ppe(df)
    intangible = calculate_intangible_assets(df)
    #st.write(intangible)
    ap = calculate_accounts_payable(df)
    std = calculate_short_term_debt(df)
    wp = calculate_wages_payables(df)
    sc = calculate_share_capital(df)
    re = calculate_retained_earnings(df)
    net_income = calculate_net_income(profit_loss_df)

    # Step 5: Compile the Balance Sheet
    balance_sheet = pd.DataFrame({'Year-Month': sorted(df['Year-Month'].unique())})
    
    for item in [cash, ar, inventory, ppe, intangible, ap, std, wp, sc, re]:
        if 'Year-Month' in item.columns:
            #item = item.rename(columns={'Year-Month': 'year-month'})
            balance_sheet = balance_sheet.merge(item, on='Year-Month', how='outer')
        else:
            st.warning(f"'Year-Month' column missing in one of the dataframes. Skipping this item.")

    balance_sheet = balance_sheet.merge(net_income[['Year-Month', 'cumulative net income']], on='Year-Month', how='outer')
    #balance_sheet = balance_sheet.drop('Year-Month', axis=1)
    balance_sheet = balance_sheet.rename(columns={'cumulative net income': 'ongoing earnings'})
    
    # Fill NaN with 0
    balance_sheet.fillna(0, inplace=True)
    
    # Debugging: Print all columns in the balance sheet
    #st.write("Columns in the balance sheet:")
    #st.write(balance_sheet.columns.tolist())
    
    # Adjust Signs Based on Accounting Principles
    liability_accounts = ['accounts payable', 'short-term debt', 'wages payables']
    equity_accounts = ['share capital', 'retained earnings', 'ongoing earnings']
    
    # Debugging: Check which accounts are present in the balance sheet
    #st.write("Checking for presence of accounts:")
    #for account in liability_accounts + equity_accounts:
    #    st.write(f"{account}: {'Present' if account in balance_sheet.columns else 'Missing'}")
    
    for col in liability_accounts + equity_accounts:
        if col in balance_sheet.columns:
            if col != 'ongoing earnings':
                balance_sheet[col] = -balance_sheet[col]
        else:
            st.warning(f"Column '{col}' not found in balance sheet. Skipping sign adjustment for this column.")

            
    
    # Calculate Totals
    asset_columns = ['cash and cash equivalents', 'accounts receivable', 'raw material inventory', 'ppe', 'intangible assets']
    balance_sheet['total assets'] = balance_sheet[asset_columns].sum(axis=1)
    balance_sheet['total liabilities'] = balance_sheet[liability_accounts].sum(axis=1)
    balance_sheet['total equity'] = balance_sheet[equity_accounts].sum(axis=1)
    balance_sheet['total equity'] = balance_sheet['total equity']
    balance_sheet['liabilities and equity'] = balance_sheet['total liabilities'] + balance_sheet['total equity']
    
    return balance_sheet

if __name__ == "__main__":
    balance_sheet = preprocess_bs()
    
    # Format financial columns to display amounts in thousands with 'K$'
    financial_columns = ['cash and cash equivalents', 'accounts receivable', 'raw material inventory', 'ppe', 'intangible assets',
                         'accounts payable', 'short-term debt', 'wages payables',
                         'share capital', 'retained earnings', 'ongoing earnings',
                         'total assets', 'total liabilities', 'total equity', 'liabilities and equity']
    
    # Convert amounts to thousands and format numbers
    balance_sheet[financial_columns] = balance_sheet[financial_columns] / 1000
    for col in financial_columns:
        balance_sheet[col] = balance_sheet[col].apply(lambda x: f"{x:,.0f} K$" if x != 0 else "0 K$")
    
    # Display the balance sheet
    st.write("**Balance Sheet**")
    st.dataframe(balance_sheet.set_index('Year-Month'))
