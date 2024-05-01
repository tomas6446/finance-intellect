import yfinance as yf

from plot import plot_data
from strategy import trend_following

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2021-01-01"
data = yf.download(ticker, start=start_date, end=end_date)

window = (10, 50)
take_profit = 0.05
stop_loss = 0.01


def main():
    new_data, _ = trend_following(data, window, take_profit, stop_loss)
    plot_data(new_data, ticker)


if __name__ == "__main__":
    main()
