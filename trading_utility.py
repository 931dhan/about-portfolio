import dataRetriever
import datetime
import utility
from urllib.error import HTTPError
import requests
import json


def get_realtime_stock(user_message_list, input_error_message):
    now = datetime.datetime.today()
    day, month, year = now.day, now.month, now.year

    try:
        stock_data_dict = dataRetriever.CallAPI(f"{user_message_list[0]}", year, month, day, "1d").day_constructor()
        raw_stock_price = f"{dataRetriever.get_stock('Open', stock_data_dict)}"
        stock_price = float(utility.round_currency_down(raw_stock_price))
        return stock_price
    except HTTPError:
        return f"HTTP error occurred. " \
               f"{input_error_message}"

    except (IndexError, ValueError):
        return f"{input_error_message}"

    except requests.exceptions.RequestException as e:
        return f"HTTP error occurred: {e}" \
               f"{input_error_message}"


def buying_stock(connection, cursor, message, stock_price, user_message_list):
    try:
        res = cursor.execute(
            f"SELECT cash_balance, stocks FROM users WHERE user_id = '{str(message.author)}'")
        database_output = res.fetchall()[0]
        previous_balance, previous_stock_dictionary = float(database_output[0]), database_output[1]
        price = stock_price * float(user_message_list[1])
        remaining_balance = float(utility.round_currency_down(str(previous_balance - price)))

        if remaining_balance < 0:
            buy_response = f"Purchase unsuccessful, ${remaining_balance} missing"

        else:
            if previous_stock_dictionary == "":
                updating_stock_dictionary = dict()
                updating_stock_dictionary[str(user_message_list[0])] = int(user_message_list[1])
                final_stock_dictionary = json.dumps(updating_stock_dictionary)

            else:
                updating_stock_dictionary = json.loads(previous_stock_dictionary)
                previous_stock_amount = int(updating_stock_dictionary.get(user_message_list[0], 0))
                updating_stock_dictionary[str(user_message_list[0])] = int(user_message_list[1]) + previous_stock_amount
                final_stock_dictionary = json.dumps(updating_stock_dictionary)

            cursor.execute(
                f"UPDATE users SET cash_balance = '{str(remaining_balance)}', stocks = '{final_stock_dictionary}' WHERE user_id = '{str(message.author)}'")
            # UPDATE table_name SET column1 = value1, column2 = value2...., columnN = valueN WHERE [condition];
            buy_response = f"Purchase successful. Remaining balance: ${remaining_balance},  price: ${price}"
            connection.commit()

        return buy_response

    except Exception as e:
        print(e)


def selling_stock(connection, cursor, message, stock_price, user_message_list):
    try:
        res = cursor.execute(
            f"SELECT cash_balance, stocks FROM users WHERE user_id = '{str(message.author)}'")
        database_output = res.fetchall()[0]
        previous_balance, previous_stock_dictionary = float(database_output[0]), database_output[1]
        price = stock_price * float(user_message_list[1])
        remaining_balance = float(utility.round_currency_down(str(previous_balance + price)))

        if previous_stock_dictionary == "":
            buy_response = f"Sale unsuccessful, {user_message_list[1]} shares missing"
        else:
            updating_stock_dictionary = json.loads(previous_stock_dictionary)
            previous_stock_amount = int(updating_stock_dictionary[user_message_list[0]])
            stock_sum = previous_stock_amount - int(user_message_list[1])
            if stock_sum < 0:
                buy_response = f"Sale unsuccessful, {stock_sum} shares missing"
            elif stock_sum == 0:
                updating_stock_dictionary.pop(str(user_message_list[0]))
                final_stock_dictionary = json.dumps(updating_stock_dictionary)
                cursor.execute(
                    f"UPDATE users SET cash_balance = '{str(remaining_balance)}', stocks = '{final_stock_dictionary}' WHERE user_id = '{str(message.author)}'")
                # UPDATE table_name SET column1 = value1, column2 = value2...., columnN = valueN WHERE [condition];
                connection.commit()
                buy_response = f" Sale successful, {stock_sum} shares remaining, ${price} gained, balance: ${remaining_balance}."

            else:
                updating_stock_dictionary[str(user_message_list[0])] = stock_sum
                final_stock_dictionary = json.dumps(updating_stock_dictionary)
                cursor.execute(
                    f"UPDATE users SET cash_balance = '{str(remaining_balance)}', stocks = '{final_stock_dictionary}' WHERE user_id = '{str(message.author)}'")
                # UPDATE table_name SET column1 = value1, column2 = value2...., columnN = valueN WHERE [condition];
                connection.commit()
                buy_response = f" Sale successful, {stock_sum} shares remaining, ${price} gained, balance: ${remaining_balance}."

        return buy_response

    except Exception as e:
        print(e)
