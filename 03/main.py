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
stop_loss = 0.01
commission = 0.001


print(f"Using parameters: Short window = {window[0]}, Long window = {window[1]}")
strategy_data, strategy_return = calculate_strategy_returns_with_costs(
    data.copy(),
    window,
    take_profit,
    stop_loss,
    commission
)

optimized_params = optimize_strategy(data)
optimized_window = optimized_params[:2]
print(f"Optimized parameters: Short window = {optimized_window[0]}, Long window = {optimized_window[1]}")

plot_comparison(data, window, optimized_window, take_profit, stop_loss, commission)
plot_signals(strategy_data, window, take_profit, stop_loss)
plot_cumulative_returns(strategy_data)
plot_sharpe_comparison(data, window, optimized_window)
