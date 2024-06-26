import mplfinance as mpf

# Formula for On Balance Volume (OBV)
# 1. If the closing price is higher than the previous closing price, then:
#    OBV = Previous OBV + Current Volume
# 2. If the closing price is lower than the previous closing price, then:
#    OBV = Previous OBV - Current Volume
# 3. If the closing price is equal to the previous closing price, then:
#    OBV = Previous OBV

def on_balance_volume(data):
    # Initialize OBV value
    obv = [0]
    # Using vectorized approach to calculate OBV
    for i in range(1, len(data)):
        # If the closing price is higher than the previous closing price
        if data['Close'].iloc[i] > data['Close'].iloc[i - 1]:
            obv.append(obv[-1] + data['Volume'].iloc[i])  # Add the current volume to the previous OBV value
        elif data['Close'].iloc[i] < data['Close'].iloc[i - 1]:
            obv.append(obv[-1] - data['Volume'].iloc[i])  # Subtract the current volume from the previous OBV value
        else:
            obv.append(obv[-1])

    data['OBV'] = obv
    return data


def plot_on_balance_vol(csv_data, start_date, end_date, figure_title):
    data_with_obv = on_balance_volume(csv_data)
    plot_data = data_with_obv.loc[start_date:end_date]

    obv_plot = mpf.make_addplot(plot_data['OBV'], panel=2, color='fuchsia', ylabel='OBV')

    mpf.plot(plot_data,
             type='candle',
             style='charles',
             title=figure_title,
             addplot=[obv_plot],
             volume=True,
             figratio=(14, 9),
             datetime_format='%Y-%m-%d %H:%M',
             figsize=(12, 9))
