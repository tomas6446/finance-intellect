import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from matplotlib.gridspec import GridSpec
from sklearn.linear_model import LinearRegression
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator

# Date,Time,Open,High,Low,Close,Volume
data_file_path = '../data/indicator_data.csv'
ticker = 'EURUSD=X'
from_date = '2004-01-01'
to_date = '2024-01-01'

lrs_window = 14
bop_period = 14

# Set global parameters to increase text and line sizes
mpl.rcParams['axes.labelsize'] = 14  # For x and y labels
mpl.rcParams['axes.titlesize'] = 16  # For the title
mpl.rcParams['xtick.labelsize'] = 12  # For x-axis tick labels
mpl.rcParams['ytick.labelsize'] = 11  # For y-axis tick labels
mpl.rcParams['legend.fontsize'] = 11  # For the legend
mpl.rcParams['lines.linewidth'] = 1  # For the lines in the plot
mpl.rcParams['figure.figsize'] = [21, 14]


# Calculate Linear Regression Slope
def calculate_LRS(data):
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
def calculate_BOP(data):
    data['BOP_raw'] = (data['Close'] - data['Open']) / (data['High'] - data['Low'])
    data['BOP_raw'] = data['BOP_raw'].replace([np.inf, -np.inf], np.nan).fillna(0)
    data['BOP'] = data['BOP_raw'].rolling(window=bop_period).mean().fillna(0)

    return data


def plot_stock_with_indicators(data, plot_LRS=False, plot_HL=False, plot_BOP=False, main_plot_type='line'):
    subplots_count = 1 + sum([plot_LRS, plot_HL, plot_BOP])
    height_ratios = [2] + [1] * (subplots_count - 1)
    fig = plt.figure()
    gs = GridSpec(subplots_count, 1, height_ratios=height_ratios, hspace=0.05)

    ax_main = fig.add_subplot(gs[0])
    if main_plot_type == 'column':
        ax_main.bar(data.index, data['Close'], label='Close Price', color='blue', width=0.5)
    else:  # Default to 'line'
        ax_main.plot(data.index, data['Close'], label='Close Price', color='skyblue')

    ax_main.set_ylabel('Stock Price')
    ax_main.legend()
    ax_main.yaxis.tick_right()
    ax_main.grid(True, which='both', linestyle='--')

    current_subplot = 1
    if plot_LRS:
        data = calculate_LRS(data)
        ax_lrs = fig.add_subplot(gs[current_subplot], sharex=ax_main)
        ax_lrs.plot(data.index, data['LR_Slope'], label='Linear Regression Slope', color='green')
        ax_lrs.set_ylim(-0.03, 0.02)
        ax_lrs.yaxis.set_major_locator(MultipleLocator(0.01))
        ax_lrs.set_ylabel('LRS', fontsize=12)
        ax_lrs.legend()
        ax_lrs.yaxis.tick_right()

        ax_lrs.grid(True, linestyle=':')
        current_subplot += 1

    if plot_HL:
        data = calculate_HL(data)
        ax_hl = fig.add_subplot(gs[current_subplot], sharex=ax_main)
        ax_hl.plot(data.index, data['HL'], label='High-Low', color='red', linewidth=2)
        ax_hl.set_ylim(-0.1, 1.5)
        ax_hl.yaxis.set_major_locator(MultipleLocator(0.5))
        ax_hl.set_ylabel('HL', fontsize=12)
        ax_hl.legend()
        ax_hl.yaxis.tick_right()
        ax_hl.grid(True, linestyle=':')
        current_subplot += 1

    if plot_BOP:
        data = calculate_BOP(data)
        ax_bop = fig.add_subplot(gs[current_subplot], sharex=ax_main)
        ax_bop.plot(data.index, data['BOP'], label='Balance of Power', color='purple', linewidth=2)
        ax_bop.set_ylim(-1, 1)
        ax_bop.yaxis.set_major_locator(MultipleLocator(0.5))
        ax_bop.set_ylabel('BOP', fontsize=12)
        ax_bop.legend()
        ax_bop.yaxis.tick_right()
        ax_bop.grid(True, linestyle=':')

    plt.setp(ax_main.get_xticklabels(), visible=False)
    ax_main.xaxis.set_major_locator(mdates.YearLocator())
    ax_main.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.autofmt_xdate()
    plt.show()


data = yf.download(ticker, start=from_date, end=to_date)
data.to_csv(data_file_path)
data = pd.read_csv(data_file_path, index_col='Date', parse_dates=True)

plot_stock_with_indicators(data, plot_LRS=True, plot_BOP=True, plot_HL=True, main_plot_type='line')
