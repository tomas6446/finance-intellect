import numpy as np

from strategy import strategy_returns


def optimize_strategy(data):
    best_return = -np.inf
    best_short_window = None
    best_long_window = None

    for short_window in range(5, 50, 5):
        for long_window in range(50, 200, 5):
            if short_window >= long_window:
                continue
            current_return = strategy_returns(data.copy(), short_window, long_window)
            if current_return > best_return:
                best_return = current_return
                best_short_window = short_window
                best_long_window = long_window

    return best_short_window, best_long_window, best_return


def calculate_sharpe_ratio(returns):
    """
    Calculates the Sharpe Ratio for given returns.
    Risk-free rate is assumed to be zero.
    """
    return returns.mean() / returns.std()

def optimize_parameters(data, short_window_range, long_window_range, take_profit, stop_loss, commission):
    best_sharpe_ratio = -np.inf
    best_params = (0, 0)

    for short_window in short_window_range:
        for long_window in long_window_range:
            if short_window >= long_window:
                continue

            # Assuming calculate_strategy_returns_with_costs also updates 'data' with returns
            temp_data, _ = calculate_strategy_returns_with_costs(
                data.copy(), short_window, long_window, take_profit, stop_loss, commission)

            # Calculate Sharpe Ratio
            sharpe_ratio = calculate_sharpe_ratio(temp_data['Strategy_Return'].dropna())

            if sharpe_ratio > best_sharpe_ratio:
                best_sharpe_ratio = sharpe_ratio
                best_params = (short_window, long_window)

    return best_params, best_sharpe_ratio
