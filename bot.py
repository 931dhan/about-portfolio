import discord
from responses import get_response
import sqlite3
import trading_utility

token = ''
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
default_command1 = '!'
default_command2 = '?'

connection = sqlite3.connect('paper_trading.db')
cursor = connection.cursor()
current_user = []
last_user_and_message = {}


async def send_message(message, user_message, is_private):
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


async def send_buy_message(message, user_message_list, is_private):
    input_error_message = "Invalid input. The format is !stock (ticker) (XXXX) (1-12) (1-31), or the datetime is out of range."
    stock_price = trading_utility.get_realtime_stock(user_message_list, input_error_message)
    buy_response = trading_utility.buying_stock(connection, cursor, message, stock_price, user_message_list)

    try:
        await message.author.send(buy_response) if is_private else await message.channel.send(buy_response)
    except Exception as e:
        print(e)


async def send_sell_message(message, user_message_list, is_private):
    input_error_message = "Invalid input. The format is !stock (ticker) (XXXX) (1-12) (1-31), or the datetime is out of range."
    stock_price = trading_utility.get_realtime_stock(user_message_list, input_error_message)
    sell_response = trading_utility.selling_stock(connection, cursor, message, stock_price, user_message_list)

    try:
        await message.author.send(sell_response) if is_private else await message.channel.send(sell_response)
    except Exception as e:
        print(e)


@client.event
async def on_ready():
    print(f'{client.user} is now running!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
        # This prevents an infinite loop from the bot talking to itself.

    username, user_message, channel = str(message.author), str(message.content), str(message.channel)
    print(f'{username} said: "{user_message}" in ({channel})')
    current_user.append(username)

    if username in last_user_and_message:
        user_message_list = user_message.split()
        if last_user_and_message[username] == f'{default_command1}buy':
            await send_buy_message(message, user_message_list, is_private=False)
        elif last_user_and_message[username] == f'{default_command2}buy':
            await send_buy_message(message, user_message_list, is_private=True)
    else:
        pass

    if username in last_user_and_message:
        user_message_list = user_message.split()
        if last_user_and_message[username] == f'{default_command1}sell':
            await send_sell_message(message, user_message_list, is_private=False)
        elif last_user_and_message[username] == f'{default_command2}sell':
            await send_sell_message(message, user_message_list, is_private=True)
    else:
        pass

    last_user_and_message[username] = user_message.lower()


    if user_message[0] == default_command1:
        user_message = user_message[1:]
        user_message = user_message.lower()
        user_message_list = user_message.split()  # Split user message into a list
        await send_message(message, user_message_list, is_private=False)

    elif user_message[0] == default_command2:
        user_message = user_message[1:]
        user_message = user_message.lower()
        user_message_list = user_message.split()  # Split user message into a list
        await send_message(message, user_message_list, is_private=True)
    else:
        return
