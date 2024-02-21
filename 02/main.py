import yfinance as yf

# Fetch historical data for Apple
apple_data = yf.Ticker("AAPL").history(period="1mo")
print(apple_data.dtypes)
apple_data_string = apple_data.to_string()
print(apple_data_string)
