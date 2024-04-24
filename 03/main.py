import yfinance as yf

from optimization import optimize_strategy
from strategy import calculate_strategy_returns_with_costs
from visualization import plot_signals, plot_cumulative_returns, plot_comparison, plot_sharpe_comparison

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2021-01-01"
data = yf.download(ticker, start=start_date, end=end_date)

window = (10, 50)
take_profit = 0.05
stop_loss = 0.02
commission = 0.001


def run_strategy_with_parameters(data, window, take_profit, stop_loss, commission):
    """Calculates and prints the return of the trading strategy for given parameters."""
    print(f"Using parameters: Short window = {window[0]}, Long window = {window[1]}")

    strategy_data, _ = calculate_strategy_returns_with_costs(
        data.copy(),
        window,
        take_profit,
        stop_loss,
        commission
    )
    return_with_costs = strategy_data.iloc[-1]
    return strategy_data, return_with_costs


original_data, original_return = run_strategy_with_parameters(data, window, take_profit, stop_loss, commission)
optimized_params = optimize_strategy(data)
optimized_window = optimized_params[:2]
print(f"Optimized parameters: Short window = {optimized_window[0]}, Long window = {optimized_window[1]}")
plot_comparison(data, window, optimized_window, take_profit, stop_loss, commission)
plot_signals(original_data, window, take_profit, stop_loss)
plot_cumulative_returns(original_data)
plot_sharpe_comparison(data, window)
