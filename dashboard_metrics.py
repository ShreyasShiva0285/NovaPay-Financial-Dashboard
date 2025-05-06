import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_generation import format_currency, format_currency_k

def display_dashboard_metrics(df, current_month, mom_revenue_growth, mom_profit_growth, 
                             mom_users_growth, expense_breakdown, revenue_breakdown):
    """Display business dashboard metrics in an expandable section."""
    with st.expander("Business Dashboard Metrics", expanded=False):
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

        # Using plotly for the revenue vs expenses chart
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

        # User Growth Chart - using plotly
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
