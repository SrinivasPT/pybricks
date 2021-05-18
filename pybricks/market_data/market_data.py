import pandas as pd
from nsepy import get_history
from datetime import datetime, timedelta
import os
from pathlib import Path
import time


def correct_instrument_names(instrument_series):
    return instrument_series.replace({'DMART-BE': 'DEMART'})


def get_sector_map():
    base_path = Path(__file__).parent
    file_path = (base_path / "../data/inbound/sector_map.csv").resolve()

    # print(f"Trying to read the holding file located @{file_path}")

    sector_map = pd.read_csv(file_path, index_col='Instrument')
    return sector_map


def get_stocks_in_sector(sector):
    sector_map = get_sector_map()
    return sector_map[sector_map['Sector'] == sector].index.tolist()


def get_holdings():
    base_path = Path(__file__).parent
    # file_path = (base_path / "../data/inbound/holdings.csv").resolve()
    file_path = "{0}/../data/inbound/holdings.csv".format(base_path)

    # print(f"Trying to read the holding file located @{file_path}")

    holdings = pd.read_csv(file_path)
    holdings['Instrument'] = correct_instrument_names(holdings['Instrument'])
    return holdings


def get_pnl():
    base_path = Path(__file__).parent
    file_path = (base_path / "../data/inbound/pnl.xlsx").resolve()

    # print(f"Trying to read the holding file located @{file_path}")

    pnl = pd.read_excel(file_path, skiprows=30).fillna(0)
    pnl['Symbol'] = correct_instrument_names(pnl['Symbol'])
    return pnl


def get_all_my_stocks():
    holdings = get_holdings()
    pnl = get_pnl()
    holding_list = holdings['Instrument'].tolist()
    pnl_list = pnl['Symbol'].tolist()
    final_list = holding_list + list(set(pnl_list) - set(holding_list))
    return final_list


def load_market_data():
    base_path = Path(__file__).parent

    end = datetime.now()
    start = end - timedelta(days=250)

    final_list = get_all_my_stocks()

    # print(f"Loading data for the date range {start} to {end}")
    for stock in final_list:
        # print(f"Stating with {stock}")
        historical_prices = get_market_data_for_stock(stock, start, end)
        #print("      Got the data from NSE")
        #pickle_path = (base_path / '../data/pickle/{stock}.pickle').resolve()
        tmp_path = '../data/pickle/{0}.pickle'.format(stock)
        pickle_path = (base_path / tmp_path).resolve()
        historical_prices.to_pickle(pickle_path)
        print("loaded {0}".format(pickle_path))
        time.sleep(3)


def get_market_data_for_stock(stock_code, start_date, end_date):
    price = get_history(symbol=stock_code, start=start_date, end=end_date)
    return price


def get_stock_history(stock_code):
    base_path = Path(__file__).parent
    # pickle_path = (base_path / f'../data/pickle/{stock_code}.pickle').resolve()
    temp_path = '../data/pickle/{0}.pickle'.format(stock_code)
    pickle_path = (base_path / temp_path).resolve()
    df = pd.read_pickle(pickle_path)

    price_series = df['Close']
    price_series.name = 'price'

    # delivery_pct_series = df['%Deliverble']
    # delivery_pct_series.name = 'delivery_pct'

    EMA13 = df['Close'].ewm(span=13, adjust=False).mean()
    EMA13.name = 'EMA13'

    EMA20 = df['Close'].ewm(span=20, adjust=False).mean()
    EMA20.name = 'EMA20'

    EMA50 = df['Close'].ewm(span=50, adjust=False).mean()
    EMA50.name = 'EMA50'

    EMA212 = df['Close'].ewm(span=212, adjust=False).mean()
    EMA212.name = 'EMA212'

    SMA20 = df['Close'].rolling(window=20).mean()
    SMA20.name = 'SMA20'

    SMA50 = df['Close'].rolling(window=50).mean()
    SMA50.name = 'SMA50'

    final_df = pd.concat(
        [price_series, EMA13, EMA20, EMA50, EMA212, SMA20, SMA50], axis=1)

    return final_df


def calculate_xma():
    holdings = get_holdings()

    for stock in holdings['Instrument']:
        price = pd.DataFrame()
        price['PRICE'] = get_stock_history(stock)['Close']

        price['EMA20'] = price['PRICE'].ewm(span=20, adjust=False).mean()
        price['EMA50'] = price['PRICE'].ewm(span=50, adjust=False).mean()
        price['SMA20'] = price['PRICE'].rolling(window=20).mean()
        price['SMA50'] = price['PRICE'].rolling(window=50).mean()
