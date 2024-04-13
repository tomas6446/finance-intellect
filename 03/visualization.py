import matplotlib.pyplot as plt
import numpy as np

import strategy as st


def plot_signals(data, short_window, long_window, take_profit=None, stop_loss=None, commission=None):
    """
    Plots the closing price, moving averages, buy/sell signals, and optionally points where Take Profit or Stop Loss was triggered.
    """
    # Calculate short and long moving averages
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

    # Identify buy and sell signals
    data['Buy'] = np.where((data['Signal'] == 1) & (data['Signal'].shift(1) == -1), data['Close'], np.nan)
    data['Sell'] = np.where((data['Signal'] == -1) & (data['Signal'].shift(1) == 1), data['Close'], np.nan)

    if take_profit is not None and stop_loss is not None and commission is not None:
        position_open_price = None
        data['TP_triggered'] = np.nan
        data['SL_triggered'] = np.nan

        for i in range(1, len(data)):
            if data['Signal'].iloc[i] == 1 and not np.isnan(data['Buy'].iloc[i]):
                position_open_price = data['Close'].iloc[i]
            elif data['Signal'].iloc[i] == -1 and not np.isnan(
                    data['Sell'].iloc[i]) and position_open_price is not None:
                position_open_price = None  # Reset for the next trade
            elif position_open_price is not None:
                current_price = data['Close'].iloc[i]
                trade_return = (current_price / position_open_price) - 1

                if trade_return >= take_profit:
                    data.at[data.index[i], 'TP_triggered'] = data['Close'].iloc[i]
                    position_open_price = None  # Assume position is closed
                elif trade_return <= -stop_loss:
                    data.at[data.index[i], 'SL_triggered'] = data['Close'].iloc[i]
                    position_open_price = None  # Assume position is closed

    # Plotting
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['SMA_short'], label=f'{short_window}day SMA', alpha=0.75)
    plt.plot(data['SMA_long'], label=f'{long_window}day SMA', alpha=0.75)

    plt.scatter(data.index, data['Buy'], label='Buy Signal', marker='^', color='green', s=100, alpha=1)
    plt.scatter(data.index, data['Sell'], label='Sell Signal', marker='v', color='red', s=100, alpha=1)

    if take_profit is not None and stop_loss is not None:
        plt.scatter(data.index, data['TP_triggered'], label='Take Profit Triggered', marker='*', color='blue', s=100,
                    alpha=1)
        plt.scatter(data.index, data['SL_triggered'], label='Stop Loss Triggered', marker='*', color='orange', s=100,
                    alpha=1)

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

    # Ensure 'Cumulative_Strategy_Return' is calculated and exists
    if 'Cumulative_Strategy_Return' in data.columns:
        plt.plot(data.index, data['Cumulative_Strategy_Return'], label='Cumulative Strategy Return', color='blue')
        plt.title('Cumulative Returns Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.legend()
    else:
        print("Cumulative_Strategy_Return column not found. Ensure it's calculated before plotting.")

    plt.show()


def plot_comparison(data, original_params, optimized_params, take_profit, stop_loss, commission):
    # Calculate returns for original parameters
    original_data, _ = st.calculate_strategy_returns_with_costs(
        data.copy(), *original_params, take_profit, stop_loss, commission)

    # Calculate returns for optimized parameters
    optimized_data, _ = st.calculate_strategy_returns_with_costs(
        data.copy(), *optimized_params, take_profit, stop_loss, commission)

    plt.figure(figsize=(14, 7))
    plt.plot(original_data['Cumulative_Strategy_Return'], label=f'Original Params: {original_params}', color='blue')
    plt.plot(optimized_data['Cumulative_Strategy_Return'], label=f'Optimized Params: {optimized_params}', color='green')

    plt.title('Cumulative Returns: Original vs. Optimized Parameters')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Returns')
    plt.legend()
    plt.show()
