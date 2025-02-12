import pandas as pd
import numpy as np

def preprocess_pl(input_file, output_file, account_filters):
    # Step 1: Load the Data
    df = pd.read_csv(input_file)

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

    # Step 3: Filter based on account selection from the dashboard
    filtered_df = df[df['Account'].isin(account_filters)]

    # Step 4: Define KPI Calculation Functions
    def calculate_sales_revenue(df):
        sales = df[df['Account'] == 'sales revenue'].groupby('Year-Month')['Solde'].sum().reset_index()
        sales['Sales Revenue'] = -sales['Solde']
        return sales[['Year-Month', 'Sales Revenue']]

    def calculate_cogs(df):
        cogs = df[df['Account'] == 'cost of goods sold'].groupby('Year-Month')['Solde'].sum().reset_index()
        cogs.rename(columns={'Solde': 'Cost of Goods Sold'}, inplace=True)
        return cogs[['Year-Month', 'Cost of Goods Sold']]

    def calculate_gross_margin(sales, cogs):
        gm = pd.merge(sales, cogs, on='Year-Month', how='left')
        gm['Gross Margin'] = gm['Sales Revenue'] - gm['Cost of Goods Sold']
        gm['Gross Margin (%)'] = (gm['Gross Margin'] / gm['Sales Revenue']) * 100
        return gm[['Year-Month', 'Gross Margin', 'Gross Margin (%)']]

    def calculate_operating_expenses(df):
        personnel = df[df['Account'] == 'personnel'].groupby('Year-Month')['Solde'].sum().reset_index()
        personnel.rename(columns={'Solde': 'Personnel'}, inplace=True)
        
        facility = df[df['Account'] == 'facility'].groupby('Year-Month')['Solde'].sum().reset_index()
        facility.rename(columns={'Solde': 'Facility'}, inplace=True)
        
        administration = df[df['Account'] == 'administration'].groupby('Year-Month')['Solde'].sum().reset_index()
        administration.rename(columns={'Solde': 'Administration'}, inplace=True)
        
        operating_exp = pd.merge(personnel, facility, on='Year-Month', how='outer')
        operating_exp = pd.merge(operating_exp, administration, on='Year-Month', how='outer').fillna(0)
        
        return operating_exp

    def calculate_ebitda(gross_margin, operating_expenses):
        ebitda = pd.merge(gross_margin, operating_expenses, on='Year-Month', how='left')
        ebitda['EBITDA'] = ebitda['Gross Margin'] - (ebitda['Personnel'] + ebitda['Facility'] + ebitda['Administration'])
        return ebitda[['Year-Month', 'EBITDA']]

    def calculate_financials(df):
        fin_income = df[df['Account'] == 'financial income'].groupby('Year-Month')['Solde'].sum().reset_index()
        fin_income['Solde'] = -fin_income['Solde']
        fin_income.rename(columns={'Solde': 'Financial Income'}, inplace=True)
        
        fin_cost = df[df['Account'] == 'financial cost'].groupby('Year-Month')['Solde'].sum().reset_index()
        fin_cost.rename(columns={'Solde': 'Financial Cost'}, inplace=True)
        
        financials = pd.merge(fin_income, fin_cost, on='Year-Month', how='outer').fillna(0)
        return financials[['Year-Month', 'Financial Income', 'Financial Cost']]

    def calculate_net_result(ebitda, financials):
        net = pd.merge(ebitda, financials, on='Year-Month', how='left')
        net['Net Result'] = net['EBITDA'] + net['Financial Income'] - net['Financial Cost']
        return net[['Year-Month', 'Net Result']]

    # Step 5: Calculate KPIs and generate the Profit and Loss table
    sales_revenue = calculate_sales_revenue(filtered_df)
    cogs = calculate_cogs(filtered_df)
    gross_margin = calculate_gross_margin(sales_revenue, cogs)
    operating_expenses = calculate_operating_expenses(filtered_df)
    ebitda = calculate_ebitda(gross_margin, operating_expenses)
    financials = calculate_financials(filtered_df)
    net_result = calculate_net_result(ebitda, financials)

    # Step 6: Consolidate KPIs
    profit_loss = pd.merge(sales_revenue, cogs, on='Year-Month', how='outer')
    profit_loss = pd.merge(profit_loss, gross_margin[['Year-Month', 'Gross Margin', 'Gross Margin (%)']], on='Year-Month', how='outer')
    profit_loss = pd.merge(profit_loss, operating_expenses, on='Year-Month', how='outer')
    profit_loss = pd.merge(profit_loss, ebitda[['Year-Month', 'EBITDA']], on='Year-Month', how='outer')
    profit_loss = pd.merge(profit_loss, financials, on='Year-Month', how='outer')
    profit_loss = pd.merge(profit_loss, net_result[['Year-Month', 'Net Result']], on='Year-Month', how='outer')

    # Fill NaN values with 0 for financial figures
    financial_columns = ['Sales Revenue', 'Cost of Goods Sold', 'Gross Margin', 'Gross Margin (%)',
                         'Personnel', 'Facility', 'Administration', 'EBITDA',
                         'Financial Income', 'Financial Cost', 'Net Result']
    profit_loss[financial_columns] = profit_loss[financial_columns].fillna(0)

    # Export to CSV
    profit_loss.to_csv(output_file, index=False)
    print(f"Profit and Loss Statement saved to {output_file}")
