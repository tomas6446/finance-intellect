import yfinance as yf

from plot import plot_data
from strategy import trend_following, optimize_strategy

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2021-01-01"
data = yf.download(ticker, start=start_date, end=end_date)

window = (10, 50)
take_profit = 0.05
stop_loss = 0.01


def main():
    strategy_data, strategy_return = trend_following(data.copy(), window, take_profit, stop_loss)
    plot_data(strategy_data, ticker)

    optimized_data, optimized_window, best_return = optimize_strategy(data.copy(), take_profit, stop_loss)
    plot_data(optimized_data, ticker)

    plot_sharpe(strategy_data, window, optimized_window)
if __name__ == "__main__":
    main()
