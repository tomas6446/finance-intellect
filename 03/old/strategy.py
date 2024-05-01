import numpy as np


# Buy Signal: Typically generated when the short SMA crosses above the long SMA.
# This indicates that recent prices are rising above the average of the longer period, suggesting an upward trend.

# Sell Signal: Generated when the short SMA crosses below the long SMA,
# indicating that recent prices are falling below the average of the longer period, suggesting a downward trend.


def calculate_strategy_returns(data, window):
    sma(data, window)
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)
    data['Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Return']
    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()

    return data['Cumulative_Strategy_Return']


def sma(data, window):
    short_window, long_window = window
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()


def calculate_strategy_returns_with_costs(data, window, take_profit, stop_loss):
    sma(data, window)
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)
    data['Strategy_Return'] = 0.0
    position_open_price = None
    for i in range(1, len(data)):
        current_signal = data['Signal'].iloc[i]
        previous_signal = data['Signal'].iloc[i - 1]
        current_price = data['Close'].iloc[i]

        if current_signal == 1 and previous_signal == -1:
            position_open_price = current_price

        elif position_open_price is not None:
            change = (current_price / position_open_price) - 1
            should_take_profit = change >= take_profit
            should_stop_loss = change <= -stop_loss
            should_sell_signal = current_signal == -1

            if should_take_profit or should_stop_loss or should_sell_signal:
                adjusted_return = max(min(change, take_profit), -stop_loss)
                data.at[data.index[i], 'Strategy_Return'] = adjusted_return
                position_open_price = None

    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()
    return data, data['Cumulative_Strategy_Return']


def sharpe_ratio(original_returns):
    return original_returns.mean() / original_returns.std()
