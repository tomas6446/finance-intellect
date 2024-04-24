import numpy as np


# Buy Signal: Typically generated when the short SMA crosses above the long SMA.
# This indicates that recent prices are rising above the average of the longer period, suggesting an upward trend.

# Sell Signal: Generated when the short SMA crosses below the long SMA,
# indicating that recent prices are falling below the average of the longer period, suggesting a downward trend.


def calculate_strategy_returns(data, window):
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
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

    # Generate trading signals
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)
    data['Strategy_Return'] = 0.0
    position_open_price = None

    for i in range(1, len(data)):
        if data['Signal'].iloc[i] == 1 and data['Signal'].iloc[i - 1] == -1:
            # Open position
            position_open_price = data['Close'].iloc[i]
            data.at[data.index[i], 'Strategy_Return'] -= commission
        elif position_open_price is not None:
            # Check take profit and stop loss
            change = (data['Close'].iloc[i] / position_open_price) - 1
            if change >= take_profit or change <= -stop_loss or data['Signal'].iloc[i] == -1:
                # Close position
                adjusted_return = max(min(change, take_profit), -stop_loss)
                data.at[data.index[i], 'Strategy_Return'] = adjusted_return - commission
                position_open_price = None

    # Calculate cumulative returns
    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()

    return data, data['Cumulative_Strategy_Return']


def sharpe_ratio(original_returns):
    """
    Calculates the Sharpe ratio of the strategy.
    """
    return original_returns.mean() / original_returns.std()
