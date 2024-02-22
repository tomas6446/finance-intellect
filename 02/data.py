import mplfinance as mpf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def load_data(file_path, date_col=None, time_col=None, parse_dates=True, index_col=None):
    """
    Loads data from a specified file path. Can handle combining date and time columns into a datetime index.

    Parameters:
    - file_path: Path to the CSV file.
    - date_col: Column name for the date.
    - time_col: Column name for the time.
    - parse_dates: Whether to parse dates. Default is True.
    - index_col: Column to set as index. Default is None.

    Returns:
    - A pandas DataFrame with the loaded data.
    """
    data = pd.read_csv(file_path, parse_dates=parse_dates, index_col=index_col)
    if date_col and time_col:
        data['DateTime'] = pd.to_datetime(data[date_col] + ' ' + data[time_col])
        data.set_index('DateTime', inplace=True)
        data.drop(columns=[date_col, time_col], inplace=True)
    return data


def plot_data(data, plot_type='line', title='Stock Data'):
    """
    Plots the data as either a line chart or a candlestick chart, with an optional volume panel.

    Parameters:
    - data: The pandas DataFrame with the stock data.
    - plot_type: The type of plot ('line' or 'candle'). Default is 'line'.
    - title: The title of the plot. Default is 'Stock Data'.
    """
    # Plot a line chart using matplotlib for 'line' plot type
    if plot_type == 'line':
        plt.figure(figsize=(14, 7))
        plt.plot(data.index, data['Close'], label='Close Price', color='blue', linewidth=1)
        plt.title(title)
        plt.xlabel('DateTime')
        plt.ylabel('Close Price')
        plt.xticks(rotation=45)
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.tight_layout()
        plt.legend()
        plt.show()
    # Plot a candlestick chart using mplfinance for 'candle' plot type
    else:
        # Check if required columns are available
        required_columns = ['Open', 'High', 'Low', 'Close']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"Data must contain {required_columns} for candlestick plot.")
        # Configure the plot style and type
        plot_kwargs = {
            'type': 'candle',
            'style': 'charles',
            'title': title,
            'figratio': (14, 7),
            'figscale': 1
        }
        # Check if volume data is available for a candlestick plot
        if 'Volume' in data.columns:
            plot_kwargs['volume'] = True
        # Plot the candlestick chart
        mpf.plot(data, **plot_kwargs)


def generate_market_data(initial_price=100, num_points=1000, volatility=0.1):
    """
    Generates random walk market data.

    Parameters:
    - initial_price: The starting price of the stock.
    - num_points: The number of data points to generate.
    - volatility: The volatility of the stock price, affecting the magnitude of price changes.

    Returns:
    - A pandas DataFrame with the generated market price data.
    """
    # Generate random price changes
    price_changes = np.random.randn(num_points) * volatility
    # Calculate the price path
    prices = initial_price + np.cumsum(price_changes)
    # Generate a DataFrame
    data = pd.DataFrame(prices, columns=['Close'])
    data['DateTime'] = pd.date_range(start='2024-01-01', periods=num_points, freq='min')  # Updated to use 'min'
    data.set_index('DateTime', inplace=True)

    return data


# Load and plot daily data
daily_data = load_data('../data/day_tsla.csv', index_col='Date')
print("Daily data:")
print(daily_data.head())
plot_data(daily_data, plot_type='candle', title='TSLA Daily Data')

# Load and plot tick data
tick_data = load_data('../data/100_tick_tsla.csv', date_col='Date', time_col='Time')
print("Tick data:")
print(tick_data.head())
plot_data(tick_data, title='TSLA Tick Data: Close Price Over Time')

# Load and plot minute data
minute_data = load_data('../data/one_minute_tsla.csv', date_col='Date', time_col='Time')
print("Minute data:")
print(minute_data.head())
plot_data(minute_data, title='TSLA Minute Data: Close Price Over Time')

# Generate and plot random walk market data
market_data = generate_market_data(initial_price=100, num_points=1000, volatility=0.1)
print("Random walk market data:")
print(market_data.head())
plot_data(market_data, title='Random Walk Market Data: Close Price Over Time')
