import matplotlib.pyplot as plt
import pandas as pd


# Date,Time,Open,High,Low,Close,Volume

def calculate_KVO(data, short_period=34, long_period=55):
    """
    Calculate Klinger Volume Oscillator (KVO)
    """
    dm = data['High'] - data['Low']
    cm = dm - dm.shift(1)
    volume_force = cm * data['Volume']
    kvo = volume_force.ewm(span=short_period, adjust=False).mean() - volume_force.ewm(span=long_period,
                                                                                      adjust=False).mean()
    data['KVO'] = kvo
    return data


def calculate_MA(data, period=20):
    """
    Calculate Moving Average (MA)
    """
    data['MA'] = data['Close'].rolling(window=period).mean()
    return data


def calculate_ATR(data, period=14):
    """
    Calculate Average True Range (ATR)
    """
    data['high-low'] = data['High'] - data['Low']
    data['high-prev_close'] = abs(data['High'] - data['Close'].shift(1))
    data['low-prev_close'] = abs(data['Low'] - data['Close'].shift(1))
    data['true_range'] = data[['high-low', 'high-prev_close', 'low-prev_close']].max(axis=1)
    data['ATR'] = data['true_range'].rolling(window=period).mean()
    return data.drop(columns=['high-low', 'high-prev_close', 'low-prev_close', 'true_range'])


def show_graph(data, plot_close=True, plot_ma=False, plot_kvo=False, plot_atr=False):
    """
    Show graph with options to plot Close Price, MA, KVO, and ATR.
    """
    fig, ax = plt.subplots(figsize=(14, 7))
    ax2 = ax.twinx()  # Prepare a second y-axis

    handles1, labels1 = [], []
    handles2, labels2 = [], []

    if plot_close:
        ax.plot(data['Close'], label='Close Price', color='black')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        handles1, labels1 = ax.get_legend_handles_labels()

    if plot_ma:
        ax.plot(data['MA'], label='Moving Average', color='blue')
        handles1, labels1 = ax.get_legend_handles_labels()

    if plot_kvo:
        ax2.plot(data['KVO'], label='KVO', color='red')
        ax2.axhline(y=0, color='gray', linestyle='--')
        ax2.set_ylabel('KVO')
        handles2, labels2 = ax2.get_legend_handles_labels()

    if plot_atr:
        ax.plot(data['ATR'], label='ATR', color='green')
        ax.set_ylabel('ATR')
        handles1, labels1 = ax.get_legend_handles_labels()

    # Combine handles and labels from both y-axes
    handles, labels = handles1 + handles2, labels1 + labels2

    # Create a single legend with entries from both axes
    fig.legend(handles, labels, loc='upper left')
    ax.grid(which='major', linestyle='--', linewidth=0.5, color='grey')
    plt.title('Tesla Stock Analysis')
    plt.show()


def read(file_path):
    data = pd.read_csv(file_path)
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data.set_index('DateTime', inplace=True)
    data.drop(columns=['Date', 'Time'], inplace=True)
    return data


data = read('../data/day_tsla.csv')

data_ma = calculate_MA(data)
show_graph(data_ma, plot_close=True, plot_ma=True)

data_kvo = calculate_KVO(data)
show_graph(data_ma, plot_close=True, plot_kvo=True)

data_atr = calculate_ATR(data)
show_graph(data_ma, plot_close=True, plot_atr=True)
