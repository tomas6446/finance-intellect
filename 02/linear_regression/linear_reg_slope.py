import numpy as np
import mplfinance as mpf


def linear_regression_slope(data, window=14):
    # Indices for each observation within the window
    indices = np.arange(window)

    def slope(y_window):
        # y_window contains the data points in the current rolling window
        x = indices
        y = y_window
        m = ((np.mean(x) * np.mean(y)) - np.mean(x * y)) / ((np.mean(x) ** 2) - np.mean(x * x))
        return m

    return data.rolling(window=window).apply(slope, raw=True)


def test_indicator_linear_slope(csv_data, start_date, end_date, figure_title):
    csv_data['LRS'] = linear_regression_slope(csv_data['Close'], window=14)
    plot_data = csv_data.loc[start_date:end_date]

    apds = [mpf.make_addplot(plot_data['LRS'], panel=2, color='purple', ylabel='LRS')]

    mpf.plot(plot_data,
             type='candle',
             style='charles',
             title=figure_title,
             addplot=apds,
             volume=True,
             figratio=(14, 9),
             datetime_format='%Y-%m-%d',
             tight_layout=False,
             show_nontrading=False,
             figsize=(12, 9))
