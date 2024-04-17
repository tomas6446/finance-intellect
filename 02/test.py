import pandas as pd

import chaikin.chaikin_oscillator as cho
import linear_regression.linear_reg_slope as lrs
import on_balance_volume.on_balance_volume as obv

data_file_name = '../data/eurusd_m1_data.csv'
date_format = "%Y.%m.%d %H:%M:%S"


def read_csv():
    data = pd.read_csv(data_file_name)
    data['Time'] = pd.to_datetime(data['Time'], format=date_format)
    data = data.set_index('Time')
    data = data.iloc[::-1]
    return data


csv_data = read_csv()

# Trend confirmation: The Chaikin Oscillator can help traders confirm the strength and direction of existing trends.
cho.plot_chaikin(
    csv_data,
    '2019.3.25 09:31:00', '2019.3.25 10:59:00',
    'Chaikin oscillator Minute OHLC data'
)

# Trend strength: The Linear Regression Slope can help traders determine the strength of a trend.
lrs.plot_linear_regression(
    csv_data,
    '2019.3.25 9:31:00', '2019.3.25 10:59:00',
    'Linear regression slope Minute OHLC data'
)

# Volume confirmation: The On Balance Volume indicator can help traders confirm the strength of a trend based on volume.
obv.plot_on_balance_vol(
    csv_data,
    '2019.3.25 09:31:00', '2019.3.25 10:59:00',
    'On balance volume Minute OHLC data'
)
