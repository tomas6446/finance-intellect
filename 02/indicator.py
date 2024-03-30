import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression

# Date,Time,Open,High,Low,Close,Volume
data_file_path = '../data/indicator_data.csv'
ticker = 'EURUSD=X'
from_date = '2004-01-01'
to_date = '2024-01-01'


# Calculate Linear Regression Slope
def calculate_LRS(data, lrs_window=14):
    data['LR_Slope'] = np.nan
    for i in range(lrs_window, len(data)):
        x = np.arange(lrs_window).reshape(-1, 1)
        y = data['Close'].iloc[i - lrs_window:i].values
        model = LinearRegression().fit(x, y)
        data.loc[data.index[i], 'LR_Slope'] = model.coef_[0]
    return data


# Calculate High-Low (H-L)
def calculate_HL(data):
    data['HL'] = data['High'] - data['Low']
    return data


# Calculate Balance of Power (BOP)
def calculate_BOP(data, bop_period=14):
    data['BOP_raw'] = (data['Close'] - data['Open']) / (data['High'] - data['Low'])
    data['BOP_raw'] = data['BOP_raw'].replace([np.inf, -np.inf], np.nan).fillna(0)
    data['BOP'] = data['BOP_raw'].rolling(window=bop_period).mean().fillna(0)

    return data


def plot_graph(dates, prices, slopes, title):
    fig, axs = plt.subplots(2, 1, figsize=(10, 12), sharex=True)

    # Plot Close Prices
    axs[0].plot(dates, prices, label='Close Prices', color='blue')
    axs[0].set_title('Close Prices')
    axs[0].set_ylabel('Price')
    axs[0].legend()

    axs[1].plot(dates, slopes, label=title, color='orange')
    axs[1].set_title(title)
    axs[1].set_xlabel('Date')
    axs[1].set_ylabel('Slope')
    axs[1].legend()

    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()


# Download data. Don't download if data file exists
data = pd.DataFrame()
if not os.path.exists(data_file_path):
    data = yf.download(ticker, start=from_date, end=to_date)
    data.to_csv(data_file_path)
data = pd.read_csv(data_file_path, index_col='Date', parse_dates=True)

##################################
lrs_data = calculate_LRS(data)
plot_graph(data.index, data['Close'], lrs_data['LR_Slope'], 'Linear Regression Slope')
##################################
hl_data = calculate_HL(data)
plot_graph(data.index, data['Close'], hl_data['HL'], 'High-Low')
##################################
bop_data = calculate_BOP(data)
plot_graph(data.index, data['Close'], bop_data['BOP'], 'Balance of Power')
