import mplfinance as mpf


def on_balance_volume(data):
    # Initialize OBV value
    obv = [0]
    # Using vectorized approach to calculate OBV
    for i in range(1, len(data)):
        # If the closing price is higher than the previous closing price
        if data['Close'].iloc[i] > data['Close'].iloc[i - 1]:
            obv.append(obv[-1] + data['Volume'].iloc[i])
        elif data['Close'].iloc[i] < data['Close'].iloc[i - 1]:
            obv.append(obv[-1] - data['Volume'].iloc[i])
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
             datetime_format='%Y-%m-%d',
             tight_layout=False,
             show_nontrading=False,
             figsize=(12, 9))
