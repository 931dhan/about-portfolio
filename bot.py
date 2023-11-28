import discord
from responses import get_response
import sqlite3
import trading_utility

token = ''


# Creates gateway specifying what content should be sent and received.
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Prefix to signal a bot command.
default_command1 = '!'
default_command2 = '?'

# Database
connection = sqlite3.connect('paper_trading.db')
cursor = connection.cursor()

# Memory for messages.
current_user = []
last_user_and_message = {}


# Retrieves response based on user message.
async def send_message(message, user_message, is_private):
    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)


# Creates specific response if the user's last message was "buy".
async def send_buy_message(message, user_message_list, is_private):
    input_error_message = "Invalid input. The format is !stock (ticker) (XXXX) (1-12) (1-31), or the datetime is out of range."

    # Retrieving stock.
    stock_price = trading_utility.get_realtime_stock(user_message_list, input_error_message)
    # Update data for user based on number of shares bought.
    buy_response = trading_utility.buying_stock(connection, cursor, message, stock_price, user_message_list)

    try:
        await message.author.send(buy_response) if is_private else await message.channel.send(buy_response)

    except Exception as e:
        print(e)


# Creates specific response if the user's last message was "sell"
async def send_sell_message(message, user_message_list, is_private):
    input_error_message = "Invalid input. The format is !stock (ticker) (XXXX) (1-12) (1-31), or the datetime is out of range."

    # Retrieving stock.
    stock_price = trading_utility.get_realtime_stock(user_message_list, input_error_message)
    # Update data for user based on number of shares bought.
    sell_response = trading_utility.selling_stock(connection, cursor, message, stock_price, user_message_list)

    try:
        await message.author.send(sell_response) if is_private else await message.channel.send(sell_response)
    except Exception as e:
        print(e)


# On "on_ready" event, signal ready.
@client.event
async def on_ready():
    print(f'{client.user} is now running!')


# On a message event.
@client.event
async def on_message(message):
    if message.author == client.user:
        return
        # This prevents an infinite loop from the bot talking to itself.

    # Reference for user id, message, and channel.
    username, user_message, channel = str(message.author), str(message.content), str(message.channel)
    print(f'{username} said: "{user_message}" in ({channel})')

    # Creates memory for current user ID.
    current_user.append(username)

    # If the user has a previous message, and the message is "buy" or "sell", send message depending on prefix.
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

    # Record last user's message and ID.
    last_user_and_message[username] = user_message.lower()

    # Depending on prefix, send public or private response based on user message.
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
