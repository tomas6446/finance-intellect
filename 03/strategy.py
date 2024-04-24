import numpy as np


def strategy_returns(data, window):
    """
    Calculates strategy returns based on short and long moving averages.
    """
    short_window, long_window = window
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

    # Signals: 1 (buy), -1 (sell)
    data['Signal'] = 0
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)

    # Portfolio returns
    data['Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Return']

    # Cumulative strategy returns
    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()

    return data['Cumulative_Strategy_Return']


def calculate_strategy_returns_with_costs(data, window, take_profit, stop_loss, commission):
    """
    Calculates strategy returns with Take Profit, Stop Loss, and commission costs.
    """
    short_window, long_window = window
    # Calculate the short and long Simple Moving Averages (SMAs)
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

    # Generate trading signals based on the SMAs
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)
    data['Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = 0.0

    # Initialize a variable to track the price at which the current position was opened
    position_open_price = None

    for i in range(1, len(data)):
        current_signal, previous_signal = data['Signal'].iloc[i], data['Signal'].iloc[i - 1]
        current_price, _ = data['Close'].iloc[i], data['Close'].iloc[i - 1]

        # Check for a buy signal
        if current_signal == 1 and previous_signal == -1:
            position_open_price = current_price
            data.at[data.index[i], 'Strategy_Return'] -= commission

        # Check for a sell signal or if take profit/stop loss conditions are met
        elif position_open_price is not None and (current_signal == -1 or (current_price / position_open_price - 1) >= take_profit or (
                current_price / position_open_price - 1) <= -stop_loss):
            trade_return = (current_price / position_open_price - 1) - commission
            data.at[data.index[i], 'Strategy_Return'] = max(min(trade_return, take_profit), -stop_loss)  # Adjust for TP/SL
            position_open_price = None

    # Calculate cumulative strategy return
    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()

    return data, data['Cumulative_Strategy_Return']


def sharpe_ratio(original_returns):
    """
    Calculates the Sharpe ratio of the strategy.
    """
    return original_returns.mean() / original_returns.std()
