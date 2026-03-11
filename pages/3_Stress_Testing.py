import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import parse_inputs, validate_inputs, get_price_data

st.title("Portfolio Stress Testing")

tickers_input = st.text_input("Enter tickers (comma separated)", "AAPL,MSFT,AMZN")

weights_input = st.text_input("Enter weights (comma separated)", "0.4,0.4,0.2")

tickers, weights = parse_inputs(tickers_input, weights_input)


error = validate_inputs(tickers, weights)
if error:
	st.error(error)
	st.stop()

st.subheader("Select Stress Scenario")

scenario = st.selectbox(
	"Scenario",
	[
		"2008 Financial Crisis (-40%)",
		"Tech Crash (-30%)",
		"Interest Rate Shock (-15%)",
		"Inflation Shock (-10%)"
	]
)

shock_dict = {}

if scenario == "2008 Financial Crisis (-40%)":
	for ticker in tickers:
		shock_dict[ticker] = -0.40

elif scenario == "Tech Crash (-30%)":
	for ticker in tickers:
		if ticker in ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META"]:
			shock_dict[ticker] = -0.30
		else:
			shock_dict[ticker] = -0.10

elif scenario == "Interest Rate Shock (-15%)":
	for ticker in tickers:
		shock_dict[ticker] = -0.15

elif scenario == "Inflation Shock (-10%)":
	for ticker in tickers:
		shock_dict[ticker] = -0.10

shock_series = pd.Series(shock_dict)

contribution = shock_series.values * weights
portfolio_shock = contribution.sum()

st.metric("Estimated Portfolio Impact", f"{portfolio_shock:.2%}")

st.subheader("Asset Shock Contributions")

contribution_df = pd.DataFrame({
	"Ticker": tickers,
	"Scenario Shock": shock_series.values,
	"Portfolio Contribution": contribution
})

contribution_df["Scenario Shock"] = contribution_df["Scenario Shock"].apply(lambda x: f"{x:.2%}")
contribution_df["Portfolio Contribution"] = contribution_df["Portfolio Contribution"].apply(lambda x: f"{x:.2%}")

st.dataframe(contribution_df)

st.subheader("Stress Contribution by Asset")

fig_stress, ax_stress = plt.subplots()
ax_stress.bar(tickers, contribution, color="red")
ax_stress.set_ylabel("Portfolio Contribution")
ax_stress.set_title("Asset Contributions Under Stress Scenario")

st.pyplot(fig_stress)