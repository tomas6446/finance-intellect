import yfinance as yf

from plot import plot_data, plot_comparison
from strategy import trend_following, optimize_strategy

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2022-01-01"
data = yf.download(ticker, start=start_date, end=end_date)

window = (10, 50)
take_profit = 0.05
stop_loss = 0.01


def main():
    strategy_data, strategy_return = trend_following(data.copy(), window, take_profit, stop_loss)
    plot_data(strategy_data, ticker)
    print(f"Window: {window}")
    print(f"Strategy Return: {strategy_return.iloc[-1]}")

    optimized_data, optimized_window, best_return = optimize_strategy(data.copy(), take_profit, stop_loss)
    print(f"Optimized Window: {optimized_window}")
    print(f"Best Return: {best_return}")
    plot_data(optimized_data, ticker)

    plot_comparison(strategy_data['Strategy_Return'], optimized_data['Strategy_Return'])


if __name__ == "__main__":
    main()
