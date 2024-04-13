import yfinance as yf

import strategy as st
from optimization import optimize_strategy
from visualization import plot_signals, plot_cumulative_returns, plot_comparison


def main():
    ticker = "AAPL"
    data = yf.download(ticker, start="2020-01-01", end="2021-01-01")

    # Original Parameters for comparison
    original_params = (20, 50)  # Example original short and long windows

    # Calculate returns with original parameters as a baseline
    print(f"Using original parameters: Short window = {original_params[0]}, "
          f"Long window = {original_params[1]}")
    original_data, original_return_with_costs = st.calculate_strategy_returns_with_costs(
        data.copy(), *original_params, 0.05, 0.02, 0.001)
    print(f"Baseline Return with Costs using Original Parameters: {original_return_with_costs}")

    # Optimize Strategy Parameters
    optimized_short_window, optimized_long_window, _ = optimize_strategy(data)
    optimized_params = (optimized_short_window, optimized_long_window)
    print(f"Optimized parameters: Short window = {optimized_short_window}, "
          f"Long window = {optimized_long_window}")

    # Visualization: Compare Original vs. Optimized Parameters
    plot_comparison(data, original_params, optimized_params, 0.05, 0.02, 0.001)

    data = original_data  # or optimized_data if you want to visualize the optimized strategy
    plot_signals(data, *optimized_params, 0.05, 0.02, 0.001)

    plot_cumulative_returns(data)


if __name__ == "__main__":
    main()
