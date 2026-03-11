import yfinance as yf
import numpy as np

def parse_inputs(tickers_input, weights_input):
	tickers = [t.strip().upper() for t in tickers_input.split(",")]
	weights = np.array([float(w) for w in weights_input.split(",")])
	return tickers, weights

def validate_inputs(tickers, weights):
	if len(tickers) != len(weights):
		return "The number of tickers must match the number of weights."
	if abs(weights.sum()-1) > 0.01:
		return "Weights must sum to 1."
	return None


def get_price_data(tickers, start="2018-01-01"):
	data = yf.download(tickers, start=start)["Close"]
	return data

def monte_carlo_simulation(portfolio_returns, simulations=1000, days=252):

	results = []

	mean = portfolio_returns.mean()
	std = portfolio_returns.std()

	for _ in range(simulations):
		simulated_returns = np.random.normal(mean, std, days)
		cumulative_return = np.prod(1 + simulated_returns) - 1
		results.append(cumulative_return)

	return np.array(results)