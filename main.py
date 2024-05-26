import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

#Loading token
load_dotenv()
TOKEN: str = os.getenv('DISCORD_TOKEN')
print(TOKEN)

 #Setup intents

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)

#Message functionality

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty')
        return
    if requested_info := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if requested_info and not response == 'null':
            await message.channel.send(response)
    except Exception as e:
        print(e)

#Handling incoming messages

@client.event
async def on_message(message: Message) -> None:

    channel: str = message.channel.name.lower()

    if message.author == client.user and not channel == "minecraft":
        return
    
    user_message: str = message.content

    await send_message(message, user_message)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()