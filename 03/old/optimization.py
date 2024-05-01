import numpy as np

from strategy import calculate_strategy_returns


def optimize_strategy(data):
    best_return = -np.inf
    best_short_window, best_long_window = None, None

    for short_window in range(5, 50, 5):
        for long_window in range(50, 200, 5):
            if short_window >= long_window:
                continue
            current_return = calculate_strategy_returns(data.copy(), window=(short_window, long_window))
            current_return = current_return.iloc[-1]
            if current_return > best_return:
                best_return = current_return
                best_short_window = short_window
                best_long_window = long_window

    return best_short_window, best_long_window, best_return
