import numpy as np

from strategy import strategy_returns


def optimize_strategy(data):
    best_return = -np.inf
    best_short_window, best_long_window = None, None

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
