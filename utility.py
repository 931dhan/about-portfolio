import dataRetriever


def round_currency_down(price: str) -> str:
    buy_response = ""
    for i in range(len(price)):
        if price[i - 1] == '.':
            buy_response = price[0:i + 2]
    return buy_response


def summarize_stock_data(p_message, stock_data_dict):
    return f"""Symbol: {p_message[1].upper()}
Date: {dataRetriever.get_stock('Date', stock_data_dict)}
Open: ${round_currency_down(str(dataRetriever.get_stock('Open', stock_data_dict)))}
High: ${round_currency_down(str(dataRetriever.get_stock('High', stock_data_dict)))}
Low: ${round_currency_down(str(dataRetriever.get_stock('Low', stock_data_dict)))}
Close: ${round_currency_down(str(dataRetriever.get_stock('Close', stock_data_dict)))}
Adj Close: ${round_currency_down(str(dataRetriever.get_adj_close('Adj Close', stock_data_dict)))} 
Volume: {dataRetriever.get_stock('Volume', stock_data_dict)}"""


def buy_receipt(previous_balance, price, remaining_balance):
    return f"""Previous balance: {previous_balance}
Price: {price}
remaining_balance: {remaining_balance}"""
