import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, DMChannel
from discord.ext import commands
from responses import get_response
import time

# Import the Python logging module
import logging
# Set the logging settings
logging.basicConfig(level=logging.INFO,
   format='[%(asctime)s] [%(levelname)s]: %(message)s',
   handlers=[
      logging.FileHandler('bot.log'),  # Save logs to a file
      logging.StreamHandler()         # Display logs in the console
])

#Loading token
load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')

 #Setup intents

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

NUMBER_OF_RETRIES = 10
RETRY_DELAY = 5

#Message functionality

async def send_message(message: Message, user_message: str) -> None:

    message_sent = False

    for i in range(NUMBER_OF_RETRIES):
        if not message_sent:
            try:
                response: str = get_response(user_message)
                await message.channel.send(response)
                message_sent = True
                return

            except Exception as e:
                print(e)

        time.sleep(RETRY_DELAY)
async def debug_message(message: Message, user_message: str) -> None:

    message_sent = False
    retry_count = 0

    for i in range(NUMBER_OF_RETRIES):
        if not message_sent:
            try:
                response: str = f'''
                                Debug Message. 
                                \nChannel Type: {str(message.channel.type)}
                                \nMessage received: {str(user_message)}
                                \nRetry count: {str(retry_count)}  
                                '''
                await message.channel.send(response)
                message_sent = True
                return

            except Exception as e:
                print(e)
        time.sleep(RETRY_DELAY)
        retry_count += 1
        


#Handling incoming messages

@client.event
async def on_message(message: Message) -> None:

    user_message: str = message.content
    valid_channels = ["minecraft", "pollocraft-logs"]
    debug_channels = ["bot-tests"]

    if message.author == client.user or not user_message:
        return


    if  user_message[0] == '?' and (isinstance(message.channel, DMChannel) or (hasattr(message.channel, 'name') and message.channel.name in valid_channels)):
        await send_message(message, user_message[1:])

    if user_message.find("debug") != -1 and (isinstance(message.channel, DMChannel) or (hasattr(message.channel, 'name') and message.channel.name in debug_channels)):
        await debug_message(message, user_message[1:])
    

# Set what the bot does when encountering an error
@bot.event
async def on_command_error(ctx, error):
   error_message = f'Error occurred while processing command: {error}'
   logging.error(error_message)
   await ctx.send(error_message)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()