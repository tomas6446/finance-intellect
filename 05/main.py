import importlib

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

plot_data = importlib.import_module("03.plot").plot_data
bollinger_bands_strategy = importlib.import_module("03.strategy").bollinger_bands_strategy
optimize_strategy = importlib.import_module("03.strategy").optimize_strategy

start_date = "2020-01-01"
end_date = "2021-01-01"
tickers = ["MARA", "AAPL", "GOOGL", "AMZN", "TSLA", "AMD", "NVDA", "AAL", "UAL", "DAL"]
data_dict = {
    ticker: yf.download(ticker, start=start_date, end=end_date, progress=False)
    for ticker in tickers
}

window = (10, 50)
take_profit = 0.05
stop_loss = 0.01


def run(ticker):
    data = data_dict.get(ticker, pd.DataFrame())
    data.set_index(pd.to_datetime(data.index), inplace=True)
    if data.empty:
        print(f"No data available for {ticker}. Skipping...")
        return

    print(data.head())

    strategy_data = bollinger_bands_strategy(data.copy(), window)
    strategy_data, optimized_window, strategy_cumulative_return, strategy_return = optimize_strategy(
        strategy_data, take_profit, stop_loss
    )

    print(f"Ticker: {ticker}")
    print(f"Optimized Window: {optimized_window}")
    print(f"Strategy Cumulative Return: {strategy_cumulative_return.iloc[-1]:.4f}")
    print(f"Strategy Sharpe Ratio: {(strategy_return.mean() / strategy_return.std()):.4f}")
    print("-" * 50)
    return plot_data(strategy_data, ticker, window)


def combine_plots(figs_axes):
    valid_figs_axes = [fa for fa in figs_axes if fa is not None]
    num_plots = len(valid_figs_axes)
    cols = 3
    rows = -(-num_plots // cols)

    combined_fig, axs = plt.subplots(rows, cols, figsize=(20, 13))

    for idx, (fig, ax) in enumerate(valid_figs_axes):
        row_idx = idx // cols
        col_idx = idx % cols
        for line in ax.get_lines():
            axs[row_idx, col_idx].plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), color=line.get_color())

        for scatter in ax.collections:
            offsets = scatter.get_offsets()
            colors = scatter.get_facecolor()
            axs[row_idx, col_idx].scatter(offsets[:, 0], offsets[:, 1], color=colors, label=scatter.get_label())

        axs[row_idx, col_idx].legend()
        axs[row_idx, col_idx].set_title(ax.get_title())
        axs[row_idx, col_idx].set_xlabel(ax.get_xlabel())
        axs[row_idx, col_idx].set_ylabel(ax.get_ylabel())
        axs[row_idx, col_idx].set_xlim(ax.get_xlim())

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    figs_axes = [run(ticker) for ticker in tickers]
    combine_plots(figs_axes)
