import mplfinance as mpf


def money_flow_multiplier(close, low, high):
    return ((close - low) - (high - close)) / (high - low)


def money_flow_volume(mfm, volume):
    return mfm * volume


def accumulation_distribution_line(data):
    mfm = money_flow_multiplier(data['Close'],
                                data['Low'],
                                data['High'])

    mfv = money_flow_volume(mfm, data['Volume'])
    return mfv.cumsum()


def chaikin_oscillator(data):
    data['ADL'] = accumulation_distribution_line(data)
    data['3 day EMA of ADL'] = data['ADL'].ewm(span=3, adjust=False).mean()
    data['10 day EMA of ADL'] = data['ADL'].ewm(span=10, adjust=False).mean()
    data['CHO'] = data['3 day EMA of ADL'] - data['10 day EMA of ADL']
    return data


def test_indicator(csv_data, start_date, end_date, figure_title):
    data_cho = chaikin_oscillator(csv_data)
    plot_data = data_cho.loc[start_date:end_date]

    apds = [mpf.make_addplot(plot_data['ADL'], color='g', panel=1, ylabel='ADL'),
            mpf.make_addplot(plot_data['3 day EMA of ADL'], color='r', panel=1),
            mpf.make_addplot(plot_data['10 day EMA of ADL'], color='b', panel=1),
            mpf.make_addplot(plot_data['CHO'], color='fuchsia', panel=2, ylabel='CHO')]

    mpf.plot(plot_data,
             type='candle',
             style='charles',
             title=figure_title,
             addplot=apds,
             volume=True,
             figratio=(14, 9),
             datetime_format='%Y-%m-%d',
             tight_layout=False,
             show_nontrading=False,
             figsize=(12, 9))
