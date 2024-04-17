import mplfinance as mpf


# How Do You Calculate the Accumulation Distribution Line?

# 1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low)
# 2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
# 3. ADL = Previous ADL + Current Period's Money Flow Volume

def money_flow_multiplier(close, low, high):
    return ((close - low) - (high - close)) / (high - low)


def money_flow_volume(mfm, volume):
    return mfm * volume


def accumulation_distribution_line(data):
    money_flow_mult = money_flow_multiplier(data['Close'],
                                            data['Low'],
                                            data['High'])

    money_flow_vol = money_flow_volume(money_flow_mult, data['Volume'])
    return money_flow_vol.cumsum()


def chaikin_oscillator(data):
    data['ADL'] = accumulation_distribution_line(data)
    # Exponential Moving Average Formula: EMA = (Close - EMA(previous day)) * (2/(span+1)) + EMA(previous day)
    data['3 day EMA of ADL'] = data['ADL'].ewm(span=3).mean()
    data['10 day EMA of ADL'] = data['ADL'].ewm(span=10).mean()
    data['CHO'] = data['3 day EMA of ADL'] - data['10 day EMA of ADL']
    return data


def plot_chaikin(csv_data, start_date, end_date, figure_title):
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
             datetime_format='%Y-%m-%d %H:%M',
             tight_layout=False,
             show_nontrading=False,
             figsize=(12, 9))
