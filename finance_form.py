import streamlit as st
import plotly.express as px

def display_finance_form():
    """Display and process the personal finance information form."""
    st.markdown("## Personal Financial Information")
    st.markdown('<div class="form-container">', unsafe_allow_html=True)

    # Create two columns for the form
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=18, max_value=100, step=1)

    with col2:
        monthly_salary = st.number_input("Monthly Salary (£)", min_value=0.0, step=100.0)
        monthly_expenses = st.number_input("Monthly Expenses (£)", min_value=0.0, step=50.0)

    # Expense Breakdown
    st.subheader("Monthly Expense Breakdown")

    expense_categories = {
        "Housing/Rent": 0.0,
        "Utilities": 0.0,
        "Groceries": 0.0,
        "Transportation": 0.0,
        "Healthcare": 0.0,
        "Entertainment": 0.0,
        "Other": 0.0
    }

    # Create multiple columns for expense categories
    cols = st.columns(3)
    category_values = {}

    for i, (category, _) in enumerate(expense_categories.items()):
        with cols[i % 3]:
            category_values[category] = st.number_input(f"{category} (£)", min_value=0.0, step=10.0)

    total_expenses = sum(category_values.values())

    # Show calculated summaries
    savings = 0
    savings_rate = 0
    expense_data = {}
    
    if name and age > 0 and monthly_salary > 0:
        savings = monthly_salary - total_expenses
        savings_rate = (savings / monthly_salary * 100) if monthly_salary > 0 else 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"Total Monthly Expenses: £{total_expenses:,.2f}")
            st.info(f"Monthly Savings: £{savings:,.2f}")
        
        with col2:
            st.info(f"Savings Rate: {savings_rate:.1f}%")
            months_emergency = savings * 6 if savings > 0 else 0
            st.info(f"6 Month Emergency Fund Target: £{months_emergency:,.2f}")
        
        # Create a pie chart for expense breakdown if there are any expenses
        expense_data = {}
        if total_expenses > 0:
            expense_data = {category: value for category, value in category_values.items() if value > 0}
            if expense_data:
                fig = px.pie(
                    values=list(expense_data.values()),
                    names=list(expense_data.keys()),
                    title="Your Expense Distribution",
                    hole=0.4
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

    # Save button
    if st.button("Save Financial Information"):
        if name and age > 0 and monthly_salary > 0:
            st.success(f"Financial information for {name} has been saved successfully!")
        else:
            st.error("Please fill in all required fields (Name, Age, Monthly Salary)")

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Convert expense data to expected format for CustomerDataSummary
    expense_breakdown = []
    total = sum(expense_data.values()) if expense_data else 0
    
    if total > 0:
        for category, value in expense_data.items():
            expense_breakdown.append({
                "category": category,
                "value": round((value / total) * 100)
            })
        # Sort by value descending
        expense_breakdown = sorted(expense_breakdown, key=lambda x: x["value"], reverse=True)
    
    return name, age, monthly_salary, monthly_expenses, total_expenses, savings, savings_rate, expense_breakdown
