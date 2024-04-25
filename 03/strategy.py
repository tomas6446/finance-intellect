import numpy as np


# Buy Signal: Typically generated when the short SMA crosses above the long SMA.
# This indicates that recent prices are rising above the average of the longer period, suggesting an upward trend.

# Sell Signal: Generated when the short SMA crosses below the long SMA,
# indicating that recent prices are falling below the average of the longer period, suggesting a downward trend.


def calculate_strategy_returns(data, window):
    """
    Calculates strategy returns based on short and long moving averages.
    """
    sma(data, window)

    # Signals: 1 (buy), -1 (sell)
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)

    # Portfolio returns

    data['Return'] = data['Close'].pct_change()  # Percentage change in closing prices, representing the daily returns of the asset.
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Return']  # Multiplying previous day's signal with the current day's return.

    # Cumulative strategy returns
    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()

    return data['Cumulative_Strategy_Return']


def sma(data, window):
    short_window, long_window = window
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()


def calculate_strategy_returns_with_costs(data, window, take_profit, stop_loss, commission):
    """
    Calculates strategy returns with Take Profit, Stop Loss, and commission costs.
    """
    sma(data, window)

    # Signals: 1 (buy), -1 (sell)
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)

    data['Strategy_Return'] = 0.0
    position_open_price = None

    for i in range(1, len(data)):
        current_signal = data['Signal'].iloc[i]  # Current trading signal
        previous_signal = data['Signal'].iloc[i - 1]  # Previous trading signal
        current_price = data['Close'].iloc[i]  # Current closing price of the asset

        # Check for a new buy signal
        if current_signal == 1 and previous_signal == -1:
            # A new buy signal is confirmed, so we open a position.
            position_open_price = current_price
            # Deduct the commission for opening the position from the strategy return.
            data.at[data.index[i], 'Strategy_Return'] -= commission

        # If there's an open position, check if we need to close it.
        elif position_open_price is not None:
            # Calculate the return since the position was opened.
            change = (current_price / position_open_price) - 1

            # Check if the change meets the criteria for closing the position.
            should_take_profit = change >= take_profit  # Check if profit target has been reached.
            should_stop_loss = change <= -stop_loss  # Check if stop loss limit has been hit.
            should_sell_signal = current_signal == -1  # Check if there's a sell signal.

            # If any condition to close the position is met, proceed to close.
            if should_take_profit or should_stop_loss or should_sell_signal:
                # Calculate the adjusted return, ensuring it doesn't exceed take profit or fall below stop loss.
                adjusted_return = max(min(change, take_profit), -stop_loss)
                # Record the adjusted return, net of commission, for the strategy.
                data.at[data.index[i], 'Strategy_Return'] = adjusted_return - commission
                # Reset the open position price to None, as the position is now closed.
                position_open_price = None

    # Calculate cumulative returns
    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()

    return data, data['Cumulative_Strategy_Return']


def sharpe_ratio(original_returns):
    """
    Calculates the Sharpe ratio of the strategy.
    """
    return original_returns.mean() / original_returns.std()
