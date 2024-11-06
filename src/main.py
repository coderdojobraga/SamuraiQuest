# bot.py
import os

import discord
import re
from utils import update_message
from dotenv import load_dotenv

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
    'participants' : 1286373895078936640
}

react_roles = {
    '😺' : '1285620488697024663', 
    '🐍' : '1285598334752522352'
}

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'{client.user} has connected to Discord!')

    async def on_member_join(self, member):
        print("Member has joined")
        acolhimento_channel = self.get_channel(channel_ids['acolhimento'])
        
        if acolhimento_channel:
            await acolhimento_channel.send(f'Bem vindo ao Discord do CoderDojo Braga, {member.mention}!\nPara começares, envia uma mensagem para este canal e diz-nos olá! Coloca também o teu nickname como o teu primeiro e último nome para sabermos quem és e te darmos acesso ao resto do Discord!')

    async def handle_reaction_roles(self, payload, add):
        guild = self.get_guild(payload.guild_id)
        emoji = payload.emoji.name

        if emoji in react_roles:
            role_id = int(react_roles[emoji])
            role = guild.get_role(role_id)
            member = await guild.fetch_member(payload.user_id)
            if role and member:
                if add:
                    await member.add_roles(role)
                    print(f'Role {role.name} added to {member.display_name}.')
                else:
                    await member.remove_roles(role)
                    print(f'Role {role.name} removed from {member.display_name}.')
    
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji.name
        if emoji in react_roles.keys():
            await self.handle_reaction_roles(payload, add=True)

        if payload.channel_id == channel_ids['submissions'] and emoji == "✅":
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            if message.author == self.user:
                correct_pattern = re.match(r'^(Scratch|Python)\s(<@\d{17,19}>)', message.content)
                if correct_pattern:
                    language = correct_pattern.group(1)
                    participant = correct_pattern.group(2)

                    participants_channel = self.get_channel(channel_ids['participants'])
                    participants_message = await participants_channel.fetch_message(message_ids['participants'])

                    updated_message = update_message(participants_message.content, participant, language)
                    
                    await participants_message.edit(content=updated_message)


    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        if emoji in react_roles.keys():
            await self.handle_reaction_roles(payload, add=False)
    
    async def on_message(self, message):
        guild = self.get_guild(guild_id) 
        if isinstance(message.channel, discord.DMChannel):
            author = guild.get_member(message.author.id)

            if author is None:
                return

            if discord.utils.get(author.roles, name='Ninjas'):
                correct_pattern = re.match(r'^([sS]cratch|[Pp]ython)\s*-\s*Desafio\s\d+\s*\n(.*)', message.content)
                if correct_pattern:
                    language = (correct_pattern.group(1))[0].upper() + (correct_pattern.group(1))[1:]
                    message_content = correct_pattern.group(2)
                    submissions_channel = self.get_channel(channel_ids['submissions'])
                    await submissions_channel.send(f"{language} <@{author.id}> {message_content}")
                else:
                    return
            
        else:
            if re.match(r'[Oo]l[aá].*', message.content) and message.channel.id == channel_ids['acolhimento']:
                await(message.add_reaction('👋'))
                await message.add_reaction('❤️')

            if discord.utils.get(message.author.roles, name='Mentores'):
                correct_pattern = re.match(r'\*[sS]ubir a <@&(\d+)>(\s*<@\d+>)+', message.content)
                if correct_pattern:
                    cinturao = correct_pattern.group(1)
                    role = guild.get_role(int(cinturao))
                    user_ids = re.findall(r'<@(\d+)>', message.content)
                    for id in user_ids:
                        member = await guild.fetch_member(int(id))
                        if member and role:
                            await member.add_roles(role)



client = MyClient(intents=intents)
client.run(TOKEN)