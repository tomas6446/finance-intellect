import numpy as np


def bollinger_bands(data, window):
    short_window, long_window = window
    data['SMA_short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_long'] = data['Close'].rolling(window=long_window).mean()
    data.dropna(inplace=True)


def trend_following(data, window, take_profit, stop_loss):
    bollinger_bands(data, window)

    data['Signal'] = np.where(data['SMA_short'] > data['SMA_long'], 1, -1)
    data['Buy'] = np.where((data['Signal'] == 1) & (data['Signal'].shift(1) == -1), data['Close'], np.nan)
    data['Sell'] = np.nan
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
                if should_take_profit:
                    adjusted_return = take_profit
                elif should_stop_loss:
                    adjusted_return = -stop_loss
                else:
                    adjusted_return = change

                data.at[data.index[i], 'Strategy_Return'] = adjusted_return
                data.at[data.index[i], 'Sell'] = current_price
                position_open_price = None

    data['Cumulative_Strategy_Return'] = data['Strategy_Return'].cumsum()
    data['Cumulative_Strategy_Return'].dropna(inplace=True)
    return data, data['Cumulative_Strategy_Return'], data['Strategy_Return']


def optimize_strategy(data, take_profit, stop_loss):
    best_cumulative_return = 0.0
    best_strategy_return = 0.0
    best_window = None
    best_data = None
    best_cumulative_return_series = None

    for short_window in range(5, 50, 5):
        for long_window in range(50, 200, 5):
            if short_window >= long_window:
                continue
            window = (short_window, long_window)
            strategy_data, cumulative_strategy_return, strategy_return = trend_following(data.copy(), window, take_profit, stop_loss)
            last_cumulative_return = cumulative_strategy_return.iloc[-1]

            if last_cumulative_return > best_cumulative_return:
                best_cumulative_return = last_cumulative_return
                best_strategy_return = strategy_return
                best_window = window
                best_data = strategy_data
                best_cumulative_return_series = cumulative_strategy_return

    return best_data, best_window, best_cumulative_return_series, best_strategy_return

