# bot.py
import os
import discord
from dotenv import load_dotenv
from events import on_ready, on_member_join, handle_reaction, handle_dm, handle_public_message

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.guild_messages = True
intents.reactions = True
intents.messages = True

guild_id = 763043249287856142

channel_ids = {
    'acolhimento' : 763200168743927868,
    'submissions' : 1285597566188392529,
    'introduction' : 1285598108524347413, # canal de introducao dos desafios 
    'languages' : 1285619669268566117, 
    'participants' : 1285221109406502962,
}

message_ids = {
    'languages' : 1286373895959740491,
    'participants' : None
}

react_roles = {
    '😺' : '1285620488697024663', 
    '🐍' : '1285598334752522352'
}

class MyClient(discord.Client):
    async def on_ready(self):
        await on_ready(self)
        participants_channel = self.get_channel(channel_ids['participants'])
        async for message in participants_channel.history(limit=1):
            if message.author == self.user:
                message_ids['participants'] = message.id
                print(f'Loaded participants message ID: {message.id}')
                break

    async def on_member_join(self, member):
        await on_member_join(self, member, channel_ids)

    async def on_raw_reaction_add(self, payload):
        await handle_reaction(self, payload, add=True, react_roles=react_roles, channel_ids=channel_ids, message_ids=message_ids)

    async def on_raw_reaction_remove(self, payload):
        await handle_reaction(self, payload, add=False, react_roles=react_roles, channel_ids=channel_ids, message_ids=message_ids)

    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            await handle_dm(self, message, guild_id, channel_ids)
        else:
            await handle_public_message(self, message, guild_id, channel_ids)

client = MyClient(intents=intents)
client.run(TOKEN)
