import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="NovaPay Financial Dashboard",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 0rem;
    }
    .title-container {
        background-color: #f5f7f9;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: white;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .positive {
        color: green;
    }
    .negative {
        color: red;
    }
    .sidebar .sidebar-content {
        background-color: #f8fafc;
    }
    .skills-header {
        font-weight: bold;
        margin-top: 1rem;
    }
    .skills-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 5px;
        box-shadow: 0 0 5px rgba(0,0,0,0.1);
    }
    .recruiter-note {
        font-style: italic;
        color: #666;
        border-left: 3px solid #ddd;
        padding-left: 10px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def format_currency(value):
    return f"£{value:,.0f}"

def format_currency_k(value):
    if abs(value) >= 1e6:
        return f"£{value/1e6:.1f}M"
    else:
        return f"£{value/1e3:.1f}K"

def calculate_percent_change(current, previous):
    if previous == 0:
        return 100 if current > 0 else -100
    return ((current - previous) / abs(previous)) * 100

# Generate financial data similar to your React app
def generate_financial_data(months=12):
    np.random.seed(42)  # For reproducible results
    
    # Starting values
    start_revenue = 100000
    start_expenses = 120000
    start_users = 5000
    
    # Growth rates
    revenue_growth = 0.08
    expenses_growth = 0.05
    users_growth = 0.12
    
    # Volatility
    revenue_vol = 0.1
    expenses_vol = 0.05
    users_vol = 0.08
    
    # Generate dates
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=30*(months-i-1))).strftime('%b') for i in range(months)]
    
    # Generate data
    data = []
    revenue = start_revenue
    expenses = start_expenses
    users = start_users
    
    for i in range(months):
        # Add randomness
        revenue_factor = 1 + (np.random.random() * revenue_vol * 2 - revenue_vol)
        expenses_factor = 1 + (np.random.random() * expenses_vol * 2 - expenses_vol)
        users_factor = 1 + (np.random.random() * users_vol * 2 - users_vol)
        
        # Update values
        revenue = revenue * (1 + revenue_growth) * revenue_factor
        expenses = expenses * (1 + expenses_growth) * expenses_factor
        users = users * (1 + users_growth) * users_factor
        
        # Calculate additional metrics
        profit = revenue - expenses
        profit_margin = (profit / revenue) * 100 if revenue > 0 else 0
        
        # Customer metrics
        arpu = revenue / users if users > 0 else 0
        
        # Marketing cost (30% of expenses)
        marketing_cost = expenses * 0.3
        
        # New users
        prev_users = start_users if i == 0 else data[i-1]['users']
        new_users = users - prev_users
        
        # CAC
        cac = marketing_cost / new_users if new_users > 0 else 0
        
        # Lifetime value
        churn_rate = 0.05
        avg_lifetime = 1 / churn_rate
        ltv = arpu * avg_lifetime
        
        # Runway
        cash = 2000000
        runway = cash / abs(profit) if profit < 0 else float('inf')
        
        data.append({
            'month': dates[i],
            'revenue': round(revenue),
            'expenses': round(expenses),
            'users': round(users),
            'profit': round(profit),
            'profit_margin': profit_margin,
            'arpu': arpu,
            'cac': cac,
            'ltv': ltv,
            'ltv_cac_ratio': ltv / cac if cac > 0 else 0,
            'runway': runway
        })
    
    return pd.DataFrame(data)

def get_expense_breakdown():
    return pd.DataFrame({
        'category': ['Engineering', 'Marketing', 'Operations', 'Sales', 'Admin', 'Other'],
        'value': [35, 25, 15, 10, 8, 7]
    })

def get_revenue_breakdown():
    return pd.DataFrame({
        'category': ['Transaction Fees', 'Subscription', 'B2B Services', 'Currency Exchange'],
        'value': [45, 30, 15, 10]
    })

# Generate data
df = generate_financial_data()
expense_breakdown = get_expense_breakdown()
revenue_breakdown = get_revenue_breakdown()

# Calculate KPIs
current_month = df.iloc[-1]
previous_month = df.iloc[-2]

mom_revenue_growth = calculate_percent_change(current_month['revenue'], previous_month['revenue'])
mom_users_growth = calculate_percent_change(current_month['users'], previous_month['users'])
mom_profit_growth = calculate_percent_change(current_month['profit'], previous_month['profit'])

# Main dashboard
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.title("NovaPay Financial Dashboard")
st.markdown("Track key metrics and financial health of your FinTech business.")
st.markdown('</div>', unsafe_allow_html=True)

# KPI metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Monthly Revenue")
    st.markdown(f"### {format_currency(current_month['revenue'])}")
    growth_class = "positive" if mom_revenue_growth > 0 else "negative"
    st.markdown(f"<span class='{growth_class}'>{'↑' if mom_revenue_growth > 0 else '↓'} {abs(mom_revenue_growth):.1f}%</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Monthly Profit/Loss")
    st.markdown(f"### {format_currency(current_month['profit'])}")
    growth_class = "positive" if mom_profit_growth > 0 else "negative"
    st.markdown(f"<span class='{growth_class}'>{'↑' if mom_profit_growth > 0 else '↓'} {abs(mom_profit_growth):.1f}%</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Total Users")
    st.markdown(f"### {int(current_month['users']):,}")
    growth_class = "positive" if mom_users_growth > 0 else "negative"
    st.markdown(f"<span class='{growth_class}'>{'↑' if mom_users_growth > 0 else '↓'} {abs(mom_users_growth):.1f}%</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Runway")
    if current_month['profit'] > 0:
        runway_text = "Profitable"
    else:
        runway_text = f"{int(current_month['runway'])} months"
    st.markdown(f"### {runway_text}")
    st.markdown('</div>', unsafe_allow_html=True)

# Charts
st.subheader("Revenue vs Expenses")

# Using plotly instead of altair for the revenue vs expenses chart
fig = px.bar(
    df,
    x="month",
    y=["revenue", "expenses"],
    barmode="group",
    labels={"value": "Amount (£)", "variable": "Category"},
    color_discrete_map={"revenue": "#3498ff", "expenses": "#f97316"}
)
fig.update_layout(height=300)
st.plotly_chart(fig, use_container_width=True)

# User Growth Chart - using plotly instead of altair
st.subheader("User Growth")
user_fig = px.line(
    df, 
    x="month", 
    y="users",
    markers=True,
    labels={"users": "Users", "month": "Month"}
)
user_fig.update_layout(height=300)
st.plotly_chart(user_fig, use_container_width=True)

# Pie Charts
col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Expense Breakdown")
    fig = px.pie(expense_breakdown, values='value', names='category', hole=0.4)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Revenue Streams")
    fig = px.pie(revenue_breakdown, values='value', names='category', 
                 color_discrete_sequence=['#3498ff', '#1364e4', '#1651b9', '#132d59'], hole=0.4)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.subheader("Key Unit Economics")
    
    # LTV/CAC Ratio
    ltv_cac = current_month['ltv_cac_ratio']
    st.markdown("**LTV/CAC Ratio**")
    progress_color = "green" if ltv_cac >= 3 else "orange"
    st.progress(min(ltv_cac/10, 1.0), text=f"{ltv_cac:.1f}x")
    st.caption("Target: 3.0x")
    
    # Monthly ARPU
    st.markdown("**Monthly ARPU**")
    arpu = current_month['arpu']
    st.progress(min(arpu/(arpu*1.5), 1.0), text=f"{format_currency_k(arpu)}")
    st.caption(f"Target: {format_currency_k(arpu*1.2)}")
    
    # CAC
    st.markdown("**Customer Acquisition Cost**")
    cac = current_month['cac']
    progress_color = "green" if cac < arpu * 6 else "red"
    st.progress(min(cac/(cac*2), 1.0), text=f"{format_currency_k(cac)}")
    st.caption(f"Target: {format_currency_k(cac*0.8)}")
    
    # Profit Margin
    st.markdown("**Profit Margin**")
    margin = current_month['profit_margin']
    progress_color = "green" if margin > 0 else "red"
    st.progress(min(margin/100, 1.0), text=f"{margin:.1f}%")
    st.caption("Target: 20.0%")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Graduate Skills Tracker
st.markdown("## Graduate Finance Analyst Skills")
st.markdown('<div class="skills-card">', unsafe_allow_html=True)

# Define skills with descriptions
skills = [
    {"title": "Financial Analysis", "description": "Demonstrated ability to analyze KPIs and present insights", "icon": "📊"},
    {"title": "Business Acumen", "description": "Understanding of key financial metrics for FinTech businesses", "icon": "💼"},
    {"title": "Technical Skills", "description": "Proficiency with financial dashboards and data visualization", "icon": "💻"},
    {"title": "Stakeholder Communication", "description": "Ability to present complex data in an accessible format", "icon": "🗣️"},
    {"title": "Innovation", "description": "Creating novel solutions to business intelligence challenges", "icon": "💡"}
]

# Display skills with checkboxes
for skill in skills:
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        st.markdown(f"### {skill['icon']}")
    with col2:
        st.markdown(f"**{skill['title']}**")
        st.markdown(f"{skill['description']}")
    st.checkbox("Skill demonstrated", key=f"skill_{skill['title']}")
    st.markdown("---")

# Recruiter note
st.markdown('<div class="recruiter-note">', unsafe_allow_html=True)
st.markdown("**Recruiter Note:** This dashboard demonstrates all key skills required for a graduate finance analyst position, with particular strength in data visualization and financial metric analysis.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
