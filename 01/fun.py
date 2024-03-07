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


def plot_data(data, dformat, plot_type='line', title='Stock Data', add_sessions=False):
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
        date_format = '%Y-%m-%d %H:%M:%S'
        if dformat == 'minute' or dformat == 'tick':
            date_format = '%H:%M:%S'
        ax.set_title(title)
        ax.set_xlabel('DateTime')
        ax.set_ylabel('Close Price')
        ax.legend()
        ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
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


def find_and_print_biggest_gaps(data, gap_number=10):
    """
    Finds and prints detailed information about the biggest gaps in time series data.

    Parameters:
    - data: A pandas DataFrame with a DateTime index.
    - gap_number: Number of gaps to find.
    """
    # Ensure the data is sorted by the index to correctly calculate time differences
    data = data.sort_index()

    # Calculate time differences between consecutive entries
    data['Time_Diff'] = data.index.to_series().diff()

    # Identify gaps
    gaps = data[data['Time_Diff'] > pd.Timedelta(minutes=1)].copy()
    gaps['Gap_Length'] = gaps['Time_Diff']

    # Sort the gaps by length to find the largest ones
    biggest_gaps = gaps.nlargest(gap_number, 'Gap_Length')

    print(f"The {gap_number} largest gaps in the data were:")
    for i, (index, row) in enumerate(biggest_gaps.iterrows(), start=1):
        gap_start = index - row['Time_Diff']
        gap_end = index
        print(f"{i}. Gap Length: {row['Gap_Length']}, Start: {gap_start}, End: {gap_end}")

        # Optionally, print data points just before and after the gap for context
        if gap_start in data.index:
            print(f"    Data before the gap: {data.loc[gap_start]}")
        else:
            print("    Data before the gap is not available.")

        if gap_end in data.index:
            print(f"    Data after the gap: {data.loc[gap_end]}")
        else:
            print("    Data after the gap is not available.")

    return gaps


def visualize_gaps_with_candlestick(data, gaps):
    """
    Visualizes gaps on a candlestick chart.

    Parameters:
    - data: The full pandas DataFrame with the stock data.
    - gaps: A pandas DataFrame containing the gaps data, with 'Time_Diff' indicating the gap length.
    """
    mc = mpf.make_marketcolors(up='green', down='red', edge='inherit', wick='inherit')
    s = mpf.make_mpf_style(marketcolors=mc, gridstyle='--')

    fig, ax = plt.subplots(figsize=(14, 7))
    mpf.plot(data, type='candle', style=s, ax=ax, show_nontrading=True)

    for i, (start, gap) in enumerate(gaps.iterrows()):
        end = start + gap['Time_Diff']  # Calculate the end of the gap
        # Shift the shaded area back by the length of the gap to highlight the correct range
        ax.axvspan(start - gap['Time_Diff'], end - gap['Time_Diff'], color='red', alpha=0.5)
        # Add text annotation for the gap number
        ax.text(start - gap['Time_Diff'], data['High'].max(), f'Gap {i + 1}', color='blue', fontsize=9)

    plt.show()


def resample_data(data, frequency='1min'):
    """
    Resamples the tick data into bars of a specified frequency.

    Parameters:
    - data: The pandas DataFrame with the tick data.
    - frequency: The frequency for resampling ('1T' for 1-minute bars, '1H' for 1-hour bars, etc.).
    """
    data['Price'] = data['Up'].astype(float)
    data['Volume'] = data['Down'].astype(int)

    # Resample the data according to the frequency
    resampled_data = data.resample(frequency).agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Up': 'sum',
        'Down': 'sum'
    })

    # Create a 'Volume' column by summing 'Up' and 'Down'
    resampled_data['Volume'] = resampled_data['Up'] + resampled_data['Down']
    resampled_data.drop(columns=['Up', 'Down'], inplace=True)

    # Drop rows with NaN values, which represent periods with no ticks
    resampled_data.dropna(inplace=True)

    return resampled_data
