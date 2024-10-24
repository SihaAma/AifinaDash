def financial_dashboard(df, sales_account, cogs_account, opex_accounts, current_month, current_year):
    # Filter data for the selected month and year
    filtered_df = df[(df['Month'] == current_month) & (df['Year'] == current_year)]
    
    # Calculate metrics
    sales_revenue = -filtered_df[filtered_df['Account'] == sales_account]['Solde'].sum()
    cogs = filtered_df[filtered_df['Account'] == cogs_account]['Solde'].sum()
    opex = filtered_df[filtered_df['Account'].isin(opex_accounts)]['Solde'].sum()
    
    gross_margin = sales_revenue - cogs
    ebitda = gross_margin - opex
    
    margin_percentage = (gross_margin / sales_revenue) * 100 if sales_revenue != 0 else 0
    
    return {
        'Sales Revenue': sales_revenue,
        'COGS': cogs,
        'Gross Margin': gross_margin,
        'OPEX': opex,
        'EBITDA': ebitda,
        'Margin (%)': margin_percentage
    }