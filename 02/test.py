import pandas as pd

import chaikin.chaikin_oscillator as cho
import linear_regression.linear_reg_slope as lrs
import on_balance_volume.on_balance_volume as obv

data_file_name = '../data/eurusd_m1_data.csv'

date_format = "%Y.%m.%d %H:%M:%S"
csv_data = pd.read_csv(data_file_name)
csv_data['Time'] = pd.to_datetime(csv_data['Time'], format=date_format)
csv_data = csv_data.set_index('Time')
csv_data = csv_data.iloc[::-1]

cho.test_indicator(
    csv_data,
    '2019.3.25 09:31:00', '2019.3.25 10:59:00',
    'Chaikin oscillator Minute OHLC data'
)

lrs.test_indicator_linear_slope(
    csv_data,
    '2019.3.25 9:31:00', '2019.3.25 10:59:00',
    'Linear regression slope Minute OHLC data'
)

obv.test_indicator(
    csv_data,
    '2019.3.25 09:31:00', '2019.3.25 10:59:00',
    'On balance volume Minute OHLC data'
)
