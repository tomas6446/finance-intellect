import importlib
import numpy as np
import seaborn as sns
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

    strategy_data, optimized_window, strategy_cumulative_return, strategy_return = optimize_strategy(
        data.copy(), take_profit, stop_loss
    )

    print(f"Ticker: {ticker}")
    print(f"Optimized Window: {optimized_window}")
    print(f"Strategy Cumulative Return: {strategy_cumulative_return.iloc[-1]:.4f}")
    print(f"Strategy Sharpe Ratio: {(strategy_return.mean() / strategy_return.std()):.4f}")
    print("-" * 50)

    (fix, ax) = plot_data(strategy_data, ticker, window)
    daily_return = data['Close'].pct_change().dropna()
    return (fix, ax), strategy_cumulative_return, daily_return


def combine_plots(figs_axes):
    valid_figs_axes = [fa for fa in figs_axes if fa is not None]
    num_plots = len(valid_figs_axes)
    cols = 3
    rows = -(-num_plots // cols)

    _, axs = plt.subplots(rows, cols, figsize=(20, 13))

    for idx, (fig, ax) in enumerate(valid_figs_axes):
        row_idx = idx // cols
        col_idx = idx % cols

        for line in ax.get_lines():
            axs[row_idx, col_idx].plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), color=line.get_color())

        axs[row_idx, col_idx].legend()
        axs[row_idx, col_idx].set_title(ax.get_title())
        axs[row_idx, col_idx].set_xlabel(ax.get_xlabel())
        axs[row_idx, col_idx].set_ylabel(ax.get_ylabel())
        axs[row_idx, col_idx].set_xlim(ax.get_xlim())

    plt.tight_layout()
    plt.show()


def plot_combined_returns(portfolio_returns):
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_returns.index, portfolio_returns, label='Combined Portfolio Returns')
    plt.title('Combined Portfolio Profit Curve')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_correlation(data):
    returns_df = pd.DataFrame(data)
    corr = returns_df.corr()
    sns.set_theme(style="white")
    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.show()


if __name__ == "__main__":
    figs_axes = []
    all_returns = []
    daily_returns = {}
    for ticker in tickers:
        print(f"Running strategy for {ticker}...")
        (fig, ax), strategy_returns, daily_return = run(ticker)
        figs_axes.append((fig, ax))
        all_returns.append(strategy_returns)
        daily_returns[ticker] = daily_return

    combine_plots(figs_axes)
    plot_combined_returns(pd.DataFrame(all_returns).mean(axis=0))
    plot_correlation(daily_returns)
