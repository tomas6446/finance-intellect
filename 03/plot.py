import matplotlib.pyplot as plt


def plot_data(data, ticker, window):
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(data['Close'], label='Close Price', color='green', alpha=1)

    if 'SMA_short' in data.columns and 'SMA_long' in data.columns:
        ax.plot(data['SMA_short'], label='SMA_short', color='red', alpha=0.3)
        ax.plot(data['SMA_long'], label='SMA_long', color='blue', alpha=0.3)
        ax.fill_between(data.index, data['SMA_short'], data['SMA_long'], color='grey', alpha=0.3, label='Bollinger Bands')

    if 'Signal' in data.columns:
        ax.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', s=100, alpha=1)
        ax.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', s=100, alpha=1)

    ax.set_title(f'{ticker} Close Price with {window} SMA')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.legend()
    plt.show()
    return fig, ax


def plot_buy_sell_comparison(original_return, optimized_return):
    original_ratio = (252 ** 0.5) * (original_return.mean() / original_return.std())
    optimized_ratio = (252 ** 0.5) * (optimized_return.mean() / optimized_return.std())

    plt.figure(figsize=(14, 7))
    plt.plot(original_return, label=f'Original: Sharpe Ratio = {original_ratio:.2f}', color='blue')
    plt.plot(optimized_return, label=f'Optimized: Sharpe Ratio = {optimized_ratio:.2f}', color='green')

    plt.title('Sharpe Ratio Comparison: Original vs. Optimized Strategies')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()
