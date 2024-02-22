import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import pandas as pd


def load_data(file_path, date_col=None, time_col=None, parse_dates=True, index_col=None):
    """
    Loads data from a specified file path. Can handle combining date and time columns into a datetime index.

    Parameters:
    - file_path: Path to the CSV file.
    - date_col: Column name for the date.
    - time_col: Column name for the time.
    - parse_dates: Whether to parse dates. Default is True.
    - index_col: Column to set as index. Default is None.
    """
    data = pd.read_csv(file_path, parse_dates=parse_dates, index_col=index_col)
    if date_col and time_col:
        data['DateTime'] = pd.to_datetime(data[date_col] + ' ' + data[time_col])
        data.set_index('DateTime', inplace=True)
        data.drop(columns=[date_col, time_col], inplace=True)
    return data


def plot_data(data, plot_type='line', title='Stock Data', add_sessions=False):
    """
    Plots the data as either a line chart or a candlestick chart, with an optional volume panel and session shading.

    Parameters:
    - data: The pandas DataFrame with the stock data.
    - plot_type: The type of plot ('line' or 'candle'). Default is 'line'.
    - title: The title of the plot. Default is 'Stock Data'.
    - add_sessions: Boolean flag to add session shading. Default is False.
    """
    # Plot a line chart using matplotlib for 'line' plot type
    if plot_type == 'line':
        fig, ax = plt.subplots(figsize=(14, 7))

        # Plot the Close price line chart
        ax.plot(data.index, data['Close'], label='Close Price', color='blue', linewidth=1)

        # Add volume plot below if volume data is available
        if 'Volume' in data.columns:
            volume_ax = ax.twinx()
            volume_ax.bar(data.index, data['Volume'], width=0.0005, alpha=0.3, color='orange')
            volume_ax.set_ylabel('Volume', color='orange')
            volume_ax.tick_params(axis='y', labelcolor='orange')

        # Add session shading
        if add_sessions:
            unique_dates = np.unique(data.index.date)
            for date in unique_dates:
                start_time = pd.Timestamp.combine(date, pd.Timestamp('09:30').time())
                end_time = pd.Timestamp.combine(date, pd.Timestamp('16:00').time())
                ax.axvline(x=start_time, color='black', linestyle='--')
                ax.axvline(x=end_time, color='black', linestyle='--')

        # Formatting the plot
        ax.set_title(title)
        ax.set_xlabel('DateTime')
        ax.set_ylabel('Close Price')
        ax.legend()
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Plot a candlestick chart using mplfinance for 'candle' plot type
    elif plot_type == 'candle':
        # Configure the plot style and type
        plot_kwargs = {
            'type': 'candle',
            'style': 'charles',
            'title': title,
            'figratio': (14, 7),
            'figscale': 1
        }
        # Plot the candlestick chart
        mpf.plot(data, **plot_kwargs)


def generate_market_data(initial_price=100, num_points=1000, volatility=0.1):
    """
    Generates random walk market data.

    Parameters:
    - initial_price: The starting price of the stock.
    - num_points: The number of data points to generate.
    - volatility: The volatility of the stock price, affecting the magnitude of price changes.
    """
    # Generate random price changes
    price_changes = np.random.randn(num_points) * volatility
    # Calculate the price path
    prices = initial_price + np.cumsum(price_changes)
    # Generate a DataFrame
    data = pd.DataFrame(prices, columns=['Close'])
    data['DateTime'] = pd.date_range(start='2024-01-01', periods=num_points, freq='min')
    data.set_index('DateTime', inplace=True)

    return data


def convert_timediff_to_seconds(largest_gaps):
    largest_gaps.dropna(inplace=True)
    # Convert time differences to seconds
    largest_gaps['Time_Diff'] = largest_gaps['Time_Diff'].dt.total_seconds()
    return largest_gaps


def biggest_gap(data, gap_number=10):
    data['Time_Diff'] = data.index.to_series().diff()
    # Sort to find the largest gaps
    largest_gaps = data.nlargest(gap_number, 'Time_Diff')
    # Return the rows corresponding to the gaps
    return largest_gaps[['Time_Diff']]


def plot_gaps(data, largest_gaps, title):
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot the Close price line chart
    ax.plot(data.index, data['Close'], label='Close Price', color='blue', linewidth=1)

    # Plot each gap as a vertical line
    for gap_start, row in largest_gaps.iterrows():
        gap_end = gap_start + pd.Timedelta(seconds=row['Time_Diff'])
        plt.axvline(x=gap_start, color='red', linestyle='--', label='Gap Start')
        plt.axvline(x=gap_end, color='green', linestyle='--', label='Gap End')

    # Add labels and title
    ax.set_title(title)
    ax.set_xlabel('DateTime')
    ax.set_ylabel('Close Price')

    # Remove duplicate labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.show()


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
plot_data(minute_data, title='TSLA Minute Data: Close Price Over Time', add_sessions=True)

# Generate and plot random walk market data
market_data = generate_market_data(initial_price=100, num_points=1000, volatility=0.1)
print("Random walk market data:")
print(market_data.head())
plot_data(market_data, title='Random Walk Market Data: Close Price Over Time')

# Find the biggest gaps in the minute data
largest_gap = biggest_gap(minute_data, gap_number=10)
largest_gaps_with_seconds = convert_timediff_to_seconds(largest_gap)
plot_gaps(minute_data, largest_gaps_with_seconds, title='TSLA Minute Data: Close Price Over Time with Gaps')
