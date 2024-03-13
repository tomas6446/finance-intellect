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


def calculate_MA(data, period=20):
    """
    Calculate Moving Average (MA)
    """
    data['MA'] = data['Close'].rolling(window=period).mean()


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

