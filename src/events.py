import re
import discord
from utils import update_message, create_initial_message, extract_sections

async def on_ready(client):
    print(f'{client.user} has connected to Discord!')

async def on_member_join(client, member, channel_ids):
    acolhimento_channel = client.get_channel(channel_ids['acolhimento'])
    if acolhimento_channel:
        await acolhimento_channel.send(f'Bem vindo ao Discord do CoderDojo Braga, {member.mention}!\nPara começares, envia uma mensagem para este canal e diz-nos olá! Coloca também o teu nickname como o teu primeiro e último nome para sabermos quem és e te darmos acesso ao resto do Discord!')

async def handle_reaction(client, payload, add, react_roles, channel_ids, message_ids):
    emoji = payload.emoji.name
    if emoji in react_roles:
        await handle_reaction_roles(client, payload, add, react_roles)

    if add and payload.channel_id == channel_ids['submissions'] and emoji == "✅":
        await update_participants_message(client, payload, channel_ids, message_ids)

async def handle_reaction_roles(client, payload, add, react_roles):
    guild = client.get_guild(payload.guild_id)
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

async def create_or_fetch_participants_message(client, participants_channel, message_ids):
    if message_ids['participants'] is None:
        initial_message = create_initial_message()
        new_message = await participants_channel.send(initial_message)
        message_ids['participants'] = new_message.id
        print(f'Initial participants message created with ID: {new_message.id}')
        return new_message

    try:
        return await participants_channel.fetch_message(message_ids['participants'])
    except discord.errors.NotFound:
        initial_message = create_initial_message()
        new_message = await participants_channel.send(initial_message)
        message_ids['participants'] = new_message.id
        print(f'Recreated participants message with ID: {new_message.id}')
        return new_message

async def update_participants_message(client, payload, channel_ids, message_ids):
    participants_channel = client.get_channel(channel_ids['participants'])
    participants_message = await create_or_fetch_participants_message(client, participants_channel, message_ids)

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    correct_pattern = re.match(r'^(Scratch|Python)\s(<@\d{17,19}>)', message.content)
    if correct_pattern:
        language = correct_pattern.group(1)
        participant = correct_pattern.group(2)

        scratch_section, python_section = extract_sections(participants_message.content)
        if (language == "Scratch" and participant not in scratch_section) or (language == "Python" and participant not in python_section):
            updated_message = update_message(participants_message.content, participant, language)
            await participants_message.edit(content=updated_message)
            print(f'Participants message updated with new content: {updated_message}')

async def handle_dm(client, message, guild_id, channel_ids):
    guild = client.get_guild(guild_id)
    author = guild.get_member(message.author.id)

    if author is None:
        return

    if discord.utils.get(author.roles, name='Ninjas'):
        correct_pattern = re.match(r'^([sS]cratch|[Pp]ython)\s*-\s*Desafio\s\d+\s*\n(.*)', message.content)
        if correct_pattern:
            language = (correct_pattern.group(1))[0].upper() + (correct_pattern.group(1))[1:]
            message_content = correct_pattern.group(2)
            submissions_channel = client.get_channel(channel_ids['submissions'])
            await submissions_channel.send(f"{language} <@{author.id}> {message_content}")

async def handle_public_message(client, message, guild_id, channel_ids):
    guild = client.get_guild(guild_id)
    if re.match(r'[Oo]l[aá].*', message.content) and message.channel.id == channel_ids['acolhimento']:
        await message.add_reaction('👋')
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
