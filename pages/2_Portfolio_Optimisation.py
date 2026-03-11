import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from utils import parse_inputs, validate_inputs, get_price_data

st.title("Portfolio Optimisation")

tickers_input = st.text_input("Enter tickers (comma separated)", "AAPL,MSFT,NVDA")

if st.button("Run Optimisation"):
	tickers = [t.strip().upper() for t in tickers_input.split(",")]


	data = get_price_data(tickers)
	returns = data.pct_change().dropna()

	num_portfolios = 5000
	portfolio_returns_list = []
	portfolio_volatility_list = []
	portfolio_weights_list = []

	mean_returns = returns.mean()
	cov_matrix = returns.cov()

	for _ in range(num_portfolios):
		weights_random = np.random.random(len(tickers))
		weights_random /= np.sum(weights_random)

		portfolio_return = np.sum(mean_returns * weights_random) * 252
		portfolio_volatility = np.sqrt(
		np.dot(weights_random.T, np.dot(cov_matrix * 252, weights_random))
		)

		portfolio_returns_list.append(portfolio_return)
		portfolio_volatility_list.append(portfolio_volatility)
		portfolio_weights_list.append(weights_random)

	risk_free_rate = 0.02
	sharpe_ratios = (
		np.array(portfolio_returns_list) - risk_free_rate
	) / np.array(portfolio_volatility_list)

	max_sharpe_idx = np.argmax(sharpe_ratios)

	optimal_return = portfolio_returns_list[max_sharpe_idx]
	optimal_volatility = portfolio_volatility_list[max_sharpe_idx]
	optimal_weights = portfolio_weights_list[max_sharpe_idx]
	optimal_sharpe = sharpe_ratios[max_sharpe_idx]

	st.subheader("Efficient Frontier")

	fig5, ax5 = plt.subplots(figsize=(8, 5))
	scatter = ax5.scatter(
		portfolio_volatility_list,
		portfolio_returns_list,
		c=sharpe_ratios,
		cmap="viridis",
		alpha=0.6
	)

	cbar = plt.colorbar(scatter)
	cbar.set_label("Sharpe Ratio")	

	ax5.scatter(
		optimal_volatility,
		optimal_return,
		color="red",
		edgecolors="black",
		linewidth=2,
		s=200,
		label="Optimal Portfolio"
	)
	ax5.set_xlabel("Volatility")
	ax5.set_ylabel("Expected Return")
	ax5.set_title("Efficient Frontier")
	ax5.legend()

	st.pyplot(fig5)

	st.subheader("Optimal Portfolio Metrics")
	c1, c2, c3 = st.columns(3)
	c1.metric("Expected Return", f"{optimal_return:.2%}")
	c2.metric("Volatility", f"{optimal_volatility:.2%}")
	c3.metric("Sharpe Ratio", f"{optimal_sharpe:.2f}")

	st.subheader("Optimal Portfolio Allocation")
	
	fig6, ax6 = plt.subplots()

	ax6.pie(
		optimal_weights,
		labels=tickers,
		autopct="%1.2f%%",
		startangle=90
	)

	ax6.axis("equal")

	ax6.set_title("Optimal Portfolio Weights")

	st.pyplot(fig6)

	import pandas as pd

	allocation_df = pd.DataFrame({
		"Ticker": tickers,
		"Weight": optimal_weights
	})

	allocation_df = allocation_df.sort_values(by="Weight", ascending=False)
	
	allocation_df["Weight"] = allocation_df["Weight"].apply(lambda x: f"{x:.2%}")

	st.subheader("Allocation Table")
	st.dataframe(allocation_df)