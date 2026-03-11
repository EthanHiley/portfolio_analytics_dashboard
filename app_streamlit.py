import streamlit as st
st.set_page_config(page_title="Portfolio Risk & Optimisation Dashboard", layout="wide")
st.title("Portfolio Risk & Optimisation Dashboard")

st.markdown("""
Welcome to the dashboard.

This platform allows you to:

- Analyse historical portfolio performance
- Simulate future portfolio outcomes using Monte Carlo methods
- Estimate risk using Value at Risk and drawdown analysis
- Explore diversification using correlation heatmaps
- Construct efficient portfolios using Modern Portfolio Theory
- Stress test portfolios under macroeconomic scenarios

Use the sidebar to navigate between modules.
""")

st.subheader("Suggested workflow")
st.markdown("""
1. Go to **Portfolio Analysis** to analyse performance and risk
2. Go to **Portfolio Optimisation** to explore the efficient frontier
3. Go to **Stress Testing** to test macro scenarios
4. Read **About** for methodology and project details
""")
