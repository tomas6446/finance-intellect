import matplotlib.pyplot as plt
import numpy as np

import optimization as opt
import strategy as st


def plot_signals(data, window, take_profit=None, stop_loss=None):
    """
    Plots the closing price, buy/sell signals, and points where Take Profit or Stop Loss was triggered.
    """
    # Calculate Bollinger Bands
    short_window, _ = window
    std_dev = data['Close'].rolling(window=short_window).std()

    data['Upper_Band'] = data['SMA_short'] + (std_dev * 2)
    data['Lower_Band'] = data['SMA_short'] - (std_dev * 2)
    data['Average'] = data['Close'].rolling(window=short_window).mean()
    data['Buy'] = np.where((data['Signal'] == 1) & (data['Signal'].shift(1) == -1), data['Close'], np.nan)
    data['Sell'] = np.where((data['Signal'] == -1) & (data['Signal'].shift(1) == 1), data['Close'], np.nan)
    data['TP_triggered'] = np.nan
    data['SL_triggered'] = np.nan

    # Get indices where trades are opened or closed
    open_positions = data[data['Buy'].notna()].index

    # Track open position price
    for idx in open_positions:
        position_index = data.index.get_loc(idx)  # Get the integer location for the label
        position_open_price = data.loc[idx, 'Close']

        for offset in range(1, len(data) - position_index):
            sub_idx = data.index[position_index + offset]
            current_price = data.loc[sub_idx, 'Close']
            trade_return = (current_price / position_open_price) - 1

            if trade_return >= take_profit:
                data.loc[sub_idx, 'TP_triggered'] = current_price
                break
            elif trade_return <= -stop_loss:
                data.loc[sub_idx, 'SL_triggered'] = current_price
                break

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['Average'], label='Average', color='green', alpha=0.3)

    plt.fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='grey', alpha=0.3, label='Bollinger Bands')

    plt.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', s=100, alpha=1)
    plt.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', s=100, alpha=1)
    plt.scatter(data.index, data['TP_triggered'], label='Take Profit Triggered', marker='*', color='blue', s=100, alpha=1)
    plt.scatter(data.index, data['SL_triggered'], label='Stop Loss Triggered', marker='*', color='orange', s=100, alpha=1)

    plt.title('Trading Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


def plot_cumulative_returns(data):
    """
    Plots the cumulative returns of the strategy over time.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(data.index, data['Cumulative_Strategy_Return'], label='Cumulative Strategy Return', color='blue')

    plt.title('Cumulative Returns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()


def plot_comparison(data, window, optimized_window, take_profit, stop_loss, commission):
    # Calculate returns for original parameters
    _, original_data = st.calculate_strategy_returns_with_costs(data.copy(), window, take_profit, stop_loss, commission)

    # Calculate returns for optimized parameters
    _, optimized_data = st.calculate_strategy_returns_with_costs(data.copy(), optimized_window, take_profit, stop_loss, commission)

    plt.figure(figsize=(14, 7))
    plt.plot(original_data, label=f'Original Params: {window}', color='blue')
    plt.plot(optimized_data, label=f'Optimized Params: {optimized_window}', color='green')

    plt.title('Cumulative Returns: Original vs. Optimized Parameters')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()


def plot_sharpe_comparison(data, window):
    # Calculate returns for original parameters
    original_returns = st.calculate_strategy_returns(data.copy(), window)
    original_sharpe = st.sharpe_ratio(original_returns)

    # Optimize the strategy
    optimized_params = opt.optimize_strategy(data)
    optimized_window = optimized_params[:2]
    optimized_returns = st.calculate_strategy_returns(data.copy(), optimized_window)
    optimized_sharpe = st.sharpe_ratio(optimized_returns)

    plt.figure(figsize=(14, 7))
    # Convert to cumulative returns if they aren't already
    plt.plot(original_returns, label=f'Original: Sharpe Ratio = {original_sharpe:.2f}', color='blue')
    plt.plot(optimized_returns, label=f'Optimized: Sharpe Ratio = {optimized_sharpe:.2f}', color='green')

    plt.title('Sharpe Ratio Comparison: Original vs. Optimized Strategies')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()
