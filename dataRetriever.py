import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt


class CallAPI:

    def __init__(self, ticker, period1, period2, period3, interval):
        self.ticker = ticker
        self.period1 = period1
        self.period2 = period2
        self.period3 = period3
        self.interval = interval

    def day_constructor(self):
        # To call API for stock data for a specified date.
        day1 = int(time.mktime(datetime.datetime(self.period1, self.period2, self.period3, 0, 0).timetuple()))
        day2 = int(time.mktime(datetime.datetime(self.period1, self.period2, self.period3, 23, 59).timetuple()))
        interval = "1d"
        query_string = f"https://query1.finance.yahoo.com/v7/finance/download/{self.ticker}?period1={day1}&period2={day2}&interval={interval}&events=history&includeAdjustedClose=true"
        stockData = pd.read_csv(query_string)
        return stockData.to_dict(orient='list')

    def realtime_constructor(self):
        # To call API for stock data for today.
        day1 = int(time.mktime(datetime.datetime(self.period1, self.period2, self.period3, 0, 0).timetuple()))
        day2 = int(time.mktime(datetime.datetime(self.period1, self.period2, self.period3, 23, 59).timetuple()))
        interval = "1d"
        query_string = f"https://query1.finance.yahoo.com/v7/finance/download/{self.ticker}?period1={day1}&period2={day2}&interval={interval}&events=history&includeAdjustedClose=true"
        stockData = pd.read_csv(query_string)
        return stockData.to_dict(orient='list')

# class GetPlot:
#     def __init__(self, ticker, period1, period2, period3, period4, period5, period6, interval):
#         self.ticker = ticker
#         self.period1 = period1
#         self.period2 = period2
#         self.period3 = period3
#         self.period4 = period4
#         self.period5 = period5
#         self.period6 = period6
#         self.interval = interval
#
#     def plot_data_fetcher(self):
#         day1 = int(time.mktime(datetime.datetime(self.period1, self.period2, self.period3, 0, 0).timetuple()))
#         day2 = int(time.mktime(datetime.datetime(self.period4, self.period5, self.period6, 23, 59).timetuple()))
#         interval = "1d"
#         query_string = f"https://query1.finance.yahoo.com/v7/finance/download/{self.ticker}?period1={day1}&period2={day2}&interval={interval}&events=history&includeAdjustedClose=true"
#         stockData = pd.read_csv(query_string)
#         stockData.plot(kind='scatter', x='Date', y='Open')
#         return plt.show()


# Returns specific value of a stock, given a dictionary.
def get_stock(key, api_connector):
    modified_key = f"{key[0].upper()}{key[1:].lower()}"
    list_index = 0
    modified_value = api_connector[modified_key]
    modified_value = modified_value[list_index]
    return modified_value


# Returns adjusted close of a stock, given a dictionary.
def get_adj_close(key, api_connector):
    modified_key = f"{key[0].upper()}{key[1:3].lower()} {key[4].upper()}{key[5:].lower()}"
    list_index = 0
    modified_value = api_connector[modified_key]
    modified_value = modified_value[list_index]
    return modified_value

