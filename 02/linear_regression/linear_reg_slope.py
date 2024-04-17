import mplfinance as mpf
import numpy as np


def linear_regression_slope(data, window=20):
    indices = np.arange(window)

    def slope(y_window):
        x = indices
        y = y_window
        m = ((np.mean(x) * np.mean(y)) - np.mean(x * y)) / ((np.mean(x) ** 2) - np.mean(x * x))
        return m

    return data.rolling(window=window).apply(slope, raw=True)


def plot_linear_regression(csv_data, start_date, end_date, figure_title):
    csv_data['LRS'] = linear_regression_slope(csv_data['Close'], window=20)
    plot_data = csv_data.loc[start_date:end_date]

    # Create a color list based on the sign of the LRS values
    colors = ['green' if val > 0 else 'red' for val in plot_data['LRS']]

    # Create an additional plot descriptor for the LRS bars
    lrs_bars = mpf.make_addplot(plot_data['LRS'], panel=2, type='bar', color=colors, ylabel='LRS')

    mpf.plot(plot_data,
             type='candle',
             style='charles',
             title=figure_title,
             addplot=[lrs_bars],
             volume=True,
             figratio=(14, 9),
             datetime_format='%Y-%m-%d %H:%M',
             tight_layout=False,
             show_nontrading=False,
             figsize=(12, 9))
