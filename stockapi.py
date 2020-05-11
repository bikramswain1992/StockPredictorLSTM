from pandas_datareader import data as pdr
import yfinance as yf
import json
#import pickle

def get_data():
    yf.pdr_override()
    config_data = get_config()
    data = pdr.get_data_yahoo(    # could also use yf.download( if you don't need data frame
        # tickers list or string as well
        tickers = config_data[0],

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        # <  period="ytd"   >

        # start date and end date can be used instead of period
        start=config_data[1],
        end=config_data[2],

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval=config_data[3],

        # group by ticker (to access via data['TATAMOTORS.NS'])
        # (optional, default is 'column')
        group_by="ticker",

        # adjust all OHLC automatically
        # (optional, default is False)
        # <  auto_adjust = True  >

        # download pre/post regular market hours data
        # (optional, default is False)
        # <  prepost = True  >

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads=True

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        # <  proxy=None  >
    )
    stocks = config_data[0].split(" ")
    create_stock_data_files(stocks,config_data[3],data)

    del stocks,data,config_data

def get_config():
    # Reading config file
    with open("config.json") as f:
        config_data = json.load(f)
    
    # Get stock names in required format
    stocks = ""
    for names in config_data["stocks"]:
        stocks += names["name"]+ " "
    stocks = stocks.strip()

    # Get start date
    start_date = config_data["start_date"]

    # Get end date
    end_date = config_data["end_date"]

    #Get ticker duration
    ticker_duration = config_data["ticker_duration"]

    return stocks, start_date, end_date, ticker_duration

def create_stock_data_files(stocks,interval,data):
    for stock in stocks:
        data[stock].to_csv("downloads/"+stock+"_"+interval+".csv",index=False)
        #with open("downloads/" + stock + ".txt", "wb") as file:
        #   pickle.dump(data[stock], file)
            

get_data()

#Can also directly download as below
#print(yf.download("TATAMOTORS.NS", start="2020-05-07", end="2020-05-08", interval="15m"))

#Can also use pickle to save and retive data to and from files as below
#pickle.dump(data[stock], file)
#data = pickle.load(file)