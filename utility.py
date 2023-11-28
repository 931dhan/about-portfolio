import dataRetriever


def summarize_stock_data(p_message, stock_data_dict):
    return f"""Symbol: {p_message[1].upper()}
Date: {dataRetriever.get_stock('Date', stock_data_dict)}
Open: ${round(dataRetriever.get_stock('Open', stock_data_dict), 2)}
High: ${round(dataRetriever.get_stock('High', stock_data_dict), 2)}
Low: ${round(dataRetriever.get_stock('Low', stock_data_dict), 2)}
Close: ${round(dataRetriever.get_stock('Close', stock_data_dict), 2)}
Adj Close: ${round(dataRetriever.get_adj_close('Adj Close', stock_data_dict), 2)} 
Volume: {dataRetriever.get_stock('Volume', stock_data_dict)}"""


def buy_receipt(previous_balance, price, remaining_balance):
    return f"""Previous balance: {previous_balance}
Price: {price}
remaining_balance: {remaining_balance}"""
