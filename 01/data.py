import fun

# Load and plot daily data
daily_data = fun.load_data('../data/day_tsla.csv', index_col='Date')
print("Daily data:")
print(daily_data.head())
fun.plot_data(daily_data, plot_type='candle', title='TSLA Daily Data')

# Load and plot tick data
tick_data = fun.load_data('../data/100_tick_tsla.csv', date_col='Date', time_col='Time')
print("Tick data:")
print(tick_data.head())
fun.plot_data(tick_data, plot_type='candle', title='TSLA Tick Data: Close Price Over Time')

# Load and plot minute data
minute_data = fun.load_data('../data/one_minute_tsla.csv', date_col='Date', time_col='Time')
print("Minute data:")
print(minute_data.head())
fun.plot_data(minute_data, title='TSLA Minute Data: Close Price Over Time', add_sessions=True)

# Generate and plot random walk market data
market_data = fun.generate_market_data(initial_price=100, num_points=1000, volatility=0.1)
print("Random walk market data:")
print(market_data.head())
fun.plot_data(market_data, title='Random Walk Market Data: Close Price Over Time')

# Find the biggest gaps in the minute data
biggest_gaps = fun.find_and_print_biggest_gaps(minute_data)
fun.visualize_gaps_with_candlestick(minute_data, biggest_gaps)

# 01/05/2018,05:44,314.31,314.83,314.07,314.56,8704,10641
# 01/05/2018,05:45,314.77,314.85,314.49,314.55,3625,6866

# 01/05/2018,06:05,315.28,315.63,315.06,315.20,3883,2400
# 01/05/2018,06:06,315.36,315.36,314.88,315.00,6950,5332
# 01/05/2018,06:07,315.11,315.41,315.11,315.29,2786,3870
# 01/05/2018,06:08,315.25,315.42,315.20,315.38,9650,5121
# 01/05/2018,06:09,315.40,315.63,315.25,315.63,6771,2081
# 01/05/2018,06:10,315.67,315.69,315.20,315.27,2770,4594
# 01/05/2018,06:11,315.13,315.21,314.78,314.81,5890,4899
# 01/05/2018,06:12,314.81,315.00,314.40,314.97,14327,17175
# 01/05/2018,06:13,314.92,315.19,314.65,314.76,12912,9294
# 01/05/2018,06:14,314.73,314.87,314.60,314.80,1420,3550
# 01/05/2018,06:15,314.93,314.93,314.39,314.71,5883,9758
# 01/05/2018,06:16,314.61,314.61,313.73,313.76,7277,13399

# Convert tick data into 1-hour bars
hourly_bars = fun.resample_data(tick_data, frequency='1h')
fun.plot_data(hourly_bars, plot_type='candle', title='TSLA 1-Hour Bars')
