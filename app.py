
import streamlit as st
from config import setup_page_config, add_custom_css
from data_generation import (
    generate_financial_data, 
    get_expense_breakdown, 
    get_revenue_breakdown,
    calculate_percent_change
)
from finance_form import display_finance_form
from dashboard_metrics import display_dashboard_metrics

# Set up page configuration
setup_page_config()
add_custom_css()

# Title and introduction
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.title("NovaPay Financial Dashboard")
st.markdown("Track key metrics and financial health of your FinTech business.")
st.markdown('</div>', unsafe_allow_html=True)

# Display personal finance form
name, age, monthly_salary, monthly_expenses, total_expenses, savings, savings_rate, expense_data = display_finance_form()

# Generate dashboard data
df = generate_financial_data()
expense_breakdown = get_expense_breakdown()
revenue_breakdown = get_revenue_breakdown()

# Calculate KPIs
current_month = df.iloc[-1]
previous_month = df.iloc[-2]

mom_revenue_growth = calculate_percent_change(current_month['revenue'], previous_month['revenue'])
mom_users_growth = calculate_percent_change(current_month['users'], previous_month['users'])
mom_profit_growth = calculate_percent_change(current_month['profit'], previous_month['profit'])

# Display dashboard metrics in an expandable section
display_dashboard_metrics(df, current_month, mom_revenue_growth, mom_profit_growth, 
                         mom_users_growth, expense_breakdown, revenue_breakdown)
