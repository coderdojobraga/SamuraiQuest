# bot.py
import os
import discord
from datetime import datetime
from dotenv import load_dotenv
from events import on_ready, on_member_join, handle_reaction, handle_dm, handle_public_message
from utils import schedule_challenges

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
    'introduction' : 1285598108524347413,
    'languages' : 1285619669268566117, 
    'participants' : 1285221109406502962,
    'scratch-challenges' : 1285220596942115002,
    'python-challenges' : 1285220641028440074,
    'support' : 1285223260572745761
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

        introduction_channel = self.get_channel(channel_ids['introduction'])
        async for message in introduction_channel.history(limit=1):
            if message.author == self.user:
                break
        else:
            introduction_message = (
                "👋 Bem vindos aos desafios do discord do CoderDojo Braga!\n\n"
                "🙋‍♂️ Para participar, basta escolherem a(s) linguagen(s) dos desafios que pretendem fazer, no canal <#1285619669268566117>.\n\n"
                "📣 Os novos desafios irão surgir nos canais <#1285220596942115002> e <#1285220641028440074>.\n\n"
                "📮 Para submeter as respostas, enviem uma mensagem ao <@1285612642945339434>, o nosso bot dos desafios.\n"
                "A única regra para ser aceite, é que a mensagem deve começar com a linha:\n"
                "```Scratch - Desafio x```"
                "para os desafios de Scratch.\n\n"
                "Ou uma linha:\n"
                "```Python - Desafio x```"
                "para os desafios de Python.\n\n"
                "O x representa o nível do desafio atual.\n\n"
                "🏆 Os nomes dos participantes que tiverem concluído cada desafio vão aparecer no canal <#1285221109406502962>\n\n"
                "🆘 Para pedir ajuda com alguma dúvida relativa aos desafios, podem escrever no canal <#1285223260572745761>, e chamar um dos nossos mentores ajudantes, mencionando <@&1285597424060207178>!\n\n"
                "🥳 Esperamos que se divirtam muito com estes desafios complementares, e vemo-nos nas sessões!"
            )
            await introduction_channel.send(introduction_message)
            print('Introduction message sent.')

        schedule_time = datetime(2024, 11, 17, 11, 00)
        self.loop.create_task(schedule_challenges(self, channel_ids, schedule_time, message_ids))

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
