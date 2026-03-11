import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils import parse_inputs, validate_inputs, get_price_data, monte_carlo_simulation

st.title("Portfolio Analysis")

tickers_input = st.text_input("Enter tickers (comma separated)", "AAPL,MSFT,NVDA")
weights_input = st.text_input("Enter weights (comma separated)", "0.4,0.4,0.2")

if st.button("Run Portfolio Analysis"):
	tickers, weights = parse_inputs(tickers_input, weights_input)

	error = validate_inputs(tickers, weights)
	if error:
		st.error(error)
		st.stop()

	data = get_price_data(tickers)
	returns = data.pct_change().dropna()
	portfolio_returns = returns.dot(weights)
	portfolio_growth = (1 + portfolio_returns).cumprod()

	correlation_matrix = returns.corr()

	running_max = portfolio_growth.cummax()
	drawdown = (portfolio_growth - running_max) / running_max
	max_drawdown = drawdown.min()

	results = monte_carlo_simulation(portfolio_returns)
	var_95 = np.percentile(results, 5)

	fig3, ax3 = plt.subplots(figsize=(6, 4))
	portfolio_growth.plot(ax=ax3, linewidth=2)
	ax3.set_title("Historical Portfolio Performance", fontsize=14)
	ax3.set_ylabel("Portfolio Value")
	ax3.set_xlabel("Date")

	fig, ax = plt.subplots(figsize=(6, 4))
	ax.hist(results, bins=50)
	ax.set_title("Monte Carlo Portfolio Return Distribution")

	col1, col2 = st.columns(2)

	with col1:
		st.subheader("Historical Performance")
		st.pyplot(fig3)

	with col2:
		st.subheader("Return Distribution")
		st.pyplot(fig)

	st.subheader("Risk Metrics")
	m1, m2 = st.columns(2)

	with m1:
		st.metric("Expected Return", f"{np.mean(results):.2%}")
		st.metric("Probability of Loss", f"{np.mean(results < 0):.2%}")

	with m2:
		st.metric("Worst Simulated Return", f"{np.min(results):.2%}")
		st.metric("95% Value at Risk", f"{var_95:.2%}")

	st.metric("Maximum Drawdown", f"{max_drawdown:.2%}")

	fig4, ax4 = plt.subplots(figsize=(6, 4))
	drawdown.plot(ax=ax4, color="red", linewidth=2)
	ax4.set_title("Portfolio Drawdown")
	ax4.set_ylabel("Drawdown")
	ax4.grid(True, linestyle="--", alpha=0.6)

	fig2, ax2 = plt.subplots(figsize=(6, 4))
	sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", ax=ax2)

	col3, col4 = st.columns(2)

	with col3:
		st.subheader("Portfolio Drawdown")
		st.pyplot(fig4)

	with col4:
		st.subheader("Asset Correlation Heatmap")
		st.pyplot(fig2)
