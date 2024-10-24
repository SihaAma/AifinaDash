import pandas as pd
import numpy as np
import streamlit as st



def preprocess_pl(df):
    # Step 3: Define KPI Calculation Functions
    def calculate_sales_revenue(df):
        sales = df[df['Account'] == 'sales revenue'].groupby('Year-Month')['Solde'].sum().reset_index()
        sales['Sales Revenue'] = -sales['Solde']
        return sales[['Year-Month', 'Sales Revenue']]

    def calculate_cogs(df):
        cogs = df[df['Account'] == 'cost of goods sold'].groupby('Year-Month')['Solde'].sum().reset_index()
        cogs.rename(columns={'Solde': 'Cost of Goods Sold'}, inplace=True)
        return cogs[['Year-Month', 'Cost of Goods Sold']]

    def calculate_gross_margin(sales, cogs):
        gm = pd.merge(sales, cogs, on='Year-Month', how='outer')
        gm['Gross Margin'] = gm['Sales Revenue'] - gm['Cost of Goods Sold']
        gm['Gross Margin (%)'] = (gm['Gross Margin'] / gm['Sales Revenue']) * 100
        return gm

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
        ebitda = pd.merge(gross_margin, operating_expenses, on='Year-Month', how='outer')
        ebitda['EBITDA'] = ebitda['Gross Margin'] - (ebitda['Personnel'] + ebitda['Facility'] + ebitda['Administration'])
        return ebitda

    def calculate_financials(df):
        fin_income = df[df['Account'].str.lower() == 'financial income'].groupby('Year-Month')['Solde'].sum().reset_index()
        fin_income['Solde'] = -fin_income['Solde']
        fin_income.rename(columns={'Solde': 'Financial Income'}, inplace=True)
        
        fin_cost = df[df['Account'].str.lower() == 'financial cost'].groupby('Year-Month')['Solde'].sum().reset_index()
        fin_cost.rename(columns={'Solde': 'Financial Cost'}, inplace=True)
        
        financials = pd.merge(fin_income, fin_cost, on='Year-Month', how='outer').fillna(0)
        return financials

    def calculate_net_result(ebitda, financials):
        net = pd.merge(ebitda, financials, on='Year-Month', how='outer')
        net['Net Result'] = net['EBITDA'] + net['Financial Income'] - net['Financial Cost']
        return net

    # Step 4: Calculate Each KPI
    sales_revenue = calculate_sales_revenue(df)
    cogs = calculate_cogs(df)
    gross_margin = calculate_gross_margin(sales_revenue, cogs)
    operating_expenses = calculate_operating_expenses(df)
    ebitda = calculate_ebitda(gross_margin, operating_expenses)
    financials = calculate_financials(df)
    net_result = calculate_net_result(ebitda, financials)

    # Step 5: Consolidate KPIs
    profit_loss = net_result

    # Add Month and Year columns
    profit_loss['Month'] = profit_loss['Year-Month'].str.split('-').str[1].astype(int)
    profit_loss['Year'] = profit_loss['Year-Month'].str.split('-').str[0].astype(int)

    # Fill NaN values with 0 for financial figures
    financial_columns = ['Sales Revenue', 'Cost of Goods Sold', 'Gross Margin', 'Gross Margin (%)',
                         'Personnel', 'Facility', 'Administration', 'EBITDA',
                         'Financial Income', 'Financial Cost', 'Net Result']
    profit_loss[financial_columns] = profit_loss[financial_columns].fillna(0)
    #devide by 1000
    profit_loss[financial_columns] = profit_loss[financial_columns]
    
    #st.session_state.profit_loss = profit_loss

    return profit_loss

if __name__ == "__main__":
    profit_loss = preprocess_pl()
    st.write("**Profit and Loss Statement**")
    st.dataframe(profit_loss.set_index('Year-Month'))
