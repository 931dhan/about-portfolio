import json

import dataRetriever
import requests
from urllib.error import HTTPError
import datetime
import sqlite3
import bot
import utility
import trading_utility


# Retrieves response based on user message.
def get_response(message):
    connection = sqlite3.connect('paper_trading.db')
    cursor = connection.cursor()

    p_message = message

    if p_message[0] == 'hello':
        return 'Hey there!'

    if p_message[0] == 'stock':
        input_error_message = "Invalid input. The format is !stock (ticker) (XXXX) (1-12) (1-31), or the datetime is not available"

        # To format parameters of the command, excepts parameters that are invalid.
        if len(p_message) >= 4:
            year = int(p_message[2])
            month = int(p_message[3])
            day = int(p_message[4])
            try:
                stock_data_dict = dataRetriever.CallAPI(f"{p_message[1]}", year, month, day, "1d").day_constructor()

            except HTTPError:
                return f"HTTP error occurred. " \
                       f"{input_error_message}"
            except (IndexError, ValueError):
                return f"{input_error_message}"
            except requests.exceptions.RequestException as e:
                return f"HTTP error occurred: {e}" \
                       f"{input_error_message}"

            return utility.summarize_stock_data(p_message, stock_data_dict)

        # If no datetime parameters are specified, return current stock data.
        elif len(p_message) == 2:
            now = datetime.datetime.today()
            day = now.day
            month = now.month
            year = now.year

            try:
                stock_data_dict = dataRetriever.CallAPI(f"{p_message[1]}", year, month, day, "1d").day_constructor()

            except HTTPError:
                return f"HTTP error occurred. " \
                       f"{input_error_message}"
            except (IndexError, ValueError):
                return f"{input_error_message}"
            except requests.exceptions.RequestException as e:
                return f"HTTP error occurred: {e}" \
                       f"{input_error_message}"

            return utility.summarize_stock_data(p_message, stock_data_dict)

        else:
            return f"{input_error_message}"

    # To create a new profile for users.
    if p_message[0] == 'create':
        cursor.execute('INSERT INTO users (user_id, cash_balance, stocks, log) VALUES (?, ?, ?, ?)',
                       (str(bot.current_user[-1]), int(100000), '', ''))
        connection.commit()
        connection.close()
        return 'Profile successfully created.'

    # To inform user of how to format following message to create a successful request to sell or buy.
    if p_message[0] == 'buy':
        return 'Enter stock ticker symbol and # of shares you would like to buy. (Ex: TSLA 3)'

    if p_message[0] == 'sell':
        return 'Enter stock ticker symbol and # of shares you would like to sell. (Ex: TSLA 3)'

    # To retrieve balance of user.
    if p_message[0] == 'balance':
        res = cursor.execute(
            f"SELECT cash_balance, stocks FROM users WHERE user_id = '{str(bot.current_user[-1])}'")
        database_output = res.fetchall()[0]
        balance = float(database_output[0])
        return f"Balance: ${balance}"

    # To return current stocks of user.
    if p_message[0] == 'portfolio':
        res = cursor.execute(
            f"SELECT cash_balance, stocks FROM users WHERE user_id = '{str(bot.current_user[-1])}'")
        database_output = res.fetchall()[0]
        stock_dictionary = json.loads(database_output[1])
        formatted_message = f""""""
        for key in stock_dictionary:

            # Looping through values in dictionary, formatting response.
            if formatted_message == "":
                formatted_message = f"""{key.upper()}: {stock_dictionary[key]}"""
                continue
            else:
                previous_formatted_message = formatted_message
                formatted_message = f"""{previous_formatted_message}
{key.upper()}: {stock_dictionary[key]}"""
        return formatted_message

    # To return worth of investments.
    if p_message[0] == 'investing':
        res = cursor.execute(
            f"SELECT cash_balance, stocks FROM users WHERE user_id = '{str(bot.current_user[-1])}'")
        database_output = res.fetchall()[0]
        stock_dictionary = json.loads(database_output[1])
        portfolio_worth = float(0)

        # For each stock, retrieve its value, # of shares, and add the product to the worth.
        for key in stock_dictionary:
            price = trading_utility.get_realtime_stock([key], "Error")
            stock_worth = float(price) * float(stock_dictionary[key])
            portfolio_worth += stock_worth
        return str(round(portfolio_worth, 2))

    # To return net worth of user.
    if p_message[0] == 'worth':

        # Investment worth.
        res = cursor.execute(
            f"SELECT cash_balance, stocks FROM users WHERE user_id = '{str(bot.current_user[-1])}'")
        database_output = res.fetchall()[0]
        stock_dictionary = json.loads(database_output[1])
        portfolio_worth = float(0)
        for key in stock_dictionary:
            price = trading_utility.get_realtime_stock([key], "Error")
            stock_worth = float(price) * float(stock_dictionary[key])
            portfolio_worth += stock_worth

        # Balance.
        res = cursor.execute(
            f"SELECT cash_balance, stocks FROM users WHERE user_id = '{str(bot.current_user[-1])}'")
        database_output = res.fetchall()[0]
        balance = float(database_output[0])

        return str(round(balance + portfolio_worth, 2))

    # To log current investment worth.
    if p_message[0] == 'log':
        res = cursor.execute(
            f"SELECT cash_balance, stocks, log FROM users WHERE user_id = '{str(bot.current_user[-1])}'")
        database_output = res.fetchall()[0]
        stock_dictionary = json.loads(database_output[1])
        portfolio_worth = float(0)

        for key in stock_dictionary:
            price = trading_utility.get_realtime_stock([key], "Error")
            stock_worth = float(price) * float(stock_dictionary[key])
            portfolio_worth += stock_worth

        cursor.execute(
            f"UPDATE users SET log = '{str(portfolio_worth)}' WHERE user_id = '{str(bot.current_user[-1])}'")
        connection.commit()
        connection.close()
        return f"${str(portfolio_worth)} successfully logged"

    if p_message[0] == 'growth':
        res = cursor.execute(
            f"SELECT cash_balance, stocks, log FROM users WHERE user_id = '{str(bot.current_user[-1])}'")
        database_output = res.fetchall()[0]

        log = database_output[2]

        stock_dictionary = json.loads(database_output[1])
        portfolio_worth = float(0)

        for key in stock_dictionary:
            price = trading_utility.get_realtime_stock([key], "Error")
            stock_worth = float(price) * float(stock_dictionary[key])
            portfolio_worth += stock_worth
        percent = (float(portfolio_worth)/float(log) * 100) - 100

        return f"Portfolio has grown from ${log} to ${portfolio_worth}, for a {round(percent, 2)}% growth"

    if p_message[0] == 'help':
        return """Here are the available commands: 
!create: Creates a paper portfolio with $100,000 available to trade. 
!buy: Prompts the user to buy a certain stock. 
!sell: Prompts the user to sell a certain stock. 
!portfolio: Returns a list of all the user's stocks.
!stock (ticker symbol): Returns realtime stock data on the specified stock. 
!stock (ticker symbol) 2XXX (year) 12 (Month) 23 (Day): Returns stock data available for the stock on the specified date.
!investing: Returns amount in investments.
!worth: Returns balance and investment worth. 
!log: Allows user to save current investment value. 
!growth: Compares current investment value to logged investment value. 

Changing the "!" command to a "?" command allows you to use commands within a private message channel!
"""

    # To direct user to available commands if command is not recognized.
    else:
        return "Type !help for available commands!"
