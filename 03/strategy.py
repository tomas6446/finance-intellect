import numpy as np


def strategy_returns(data, short_window, long_window):
    """
    Calculates strategy returns based on short and long moving averages.
    """
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()

    # Signals: 1 (buy), -1 (sell)
    data['Signal'] = 0
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)

    # Portfolio returns
    data['Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Return']

    # Cumulative strategy returns
    total_return = data['Strategy_Return'].cumsum().iloc[-1]

    return total_return


def calculate_strategy_returns_with_costs(data, short_window, long_window, take_profit, stop_loss, commission):
    """
    Calculates strategy returns with Take Profit, Stop Loss, and commission costs.
    """
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)
    data['Return'] = data['Close'].pct_change()
    data['Strategy_Return'] = 0.0
    position_open_price = None

    for i in range(1, len(data)):
        if data['Signal'].iloc[i] == 1 and data['Signal'].iloc[i - 1] == -1:  # Buy signal
            position_open_price = data['Close'].iloc[i]
            # Deduct commission for opening position
            data.loc[data.index[i], 'Strategy_Return'] -= commission
        elif (data['Signal'].iloc[i] == -1 and data['Signal'].iloc[i - 1] == 1 and
              position_open_price is not None):  # Sell signal
            trade_return = (data['Close'].iloc[i] / position_open_price) - 1 - commission  # Deduct commission for closing position
            data.loc[data.index[i], 'Strategy_Return'] = trade_return
            position_open_price = None
        elif position_open_price is not None:
            current_price = data['Close'].iloc[i]
            trade_return = (current_price / position_open_price) - 1

            if trade_return >= take_profit:
                # Deduct commission for closing position with profit
                data.loc[data.index[i], 'Strategy_Return'] = take_profit - commission
                position_open_price = None
            elif trade_return <= -stop_loss:
                # Deduct commission for closing position with loss
                data.loc[data.index[i], 'Strategy_Return'] = -stop_loss - commission
                position_open_price = None

    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()

    return data, data['Cumulative_Strategy_Return'].iloc[-1]
