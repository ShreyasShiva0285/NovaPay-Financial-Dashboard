import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def format_currency(value):
    """Format a value as GBP currency."""
    return f"£{value:,.0f}"

def format_currency_k(value):
    """Format a value as GBP currency with K/M notation."""
    if abs(value) >= 1e6:
        return f"£{value/1e6:.1f}M"
    else:
        return f"£{value/1e3:.1f}K"

def calculate_percent_change(current, previous):
    """Calculate the percent change between two values."""
    if previous == 0:
        return 100 if current > 0 else -100
    return ((current - previous) / abs(previous)) * 100

def generate_financial_data(months=12):
    """Generate synthetic financial data for dashboard."""
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
    """Generate expense breakdown data."""
    return pd.DataFrame({
        'category': ['Engineering', 'Marketing', 'Operations', 'Sales', 'Admin', 'Other'],
        'value': [35, 25, 15, 10, 8, 7]
    })

def get_revenue_breakdown():
    """Generate revenue breakdown data."""
    return pd.DataFrame({
        'category': ['Transaction Fees', 'Subscription', 'B2B Services', 'Currency Exchange'],
        'value': [45, 30, 15, 10]
    })
