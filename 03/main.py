import yfinance as yf

from plot import plot_data, plot_buy_sell_comparison
from strategy import trend_following, optimize_strategy

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2021-01-01"
data = yf.download(ticker, start=start_date, end=end_date)

window = (10, 50)
take_profit = 0.05
stop_loss = 0.01


def main():
    strategy_data, strategy_cumulative_return, strategy_return = trend_following(data.copy(), window, take_profit, stop_loss)
    plot_data(strategy_data.copy(), ticker, window)
    print(f"Window: {window}")
    print(f"Strategy Return: {strategy_cumulative_return.iloc[-1]}")

    optimized_data, optimized_window, optimized_cumulative_return, optimized_return = optimize_strategy(data.copy(), take_profit, stop_loss)
    plot_data(optimized_data.copy(), ticker, optimized_window)
    print(f"Optimized Window: {optimized_window}")
    print(f"Best Return: {optimized_cumulative_return.iloc[-1]}")

    plot_buy_sell_comparison(strategy_return, optimized_return)


if __name__ == "__main__":
    main()
