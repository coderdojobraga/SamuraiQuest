import re
import discord
from utils import update_message, create_initial_message, extract_sections

async def on_ready(client):
    print(f'{client.user} has connected to Discord!')

async def on_member_join(client, member, channel_ids):
    acolhimento_channel = client.get_channel(channel_ids['acolhimento'])
    if acolhimento_channel:
        await acolhimento_channel.send(f'Bem vindo ao Discord do CoderDojo Braga, {member.mention}!\nPara começares, envia uma mensagem para este canal e diz-nos olá! Diz-nos também o teu primeiro e último nome, se és ninja, guardião ou voluntário, para sabermos quem és e te darmos acesso ao resto do Discord!')

async def handle_reaction(client, payload, add, react_roles, channel_ids, message_ids):
    emoji = payload.emoji.name
    if emoji in react_roles:
        await handle_reaction_roles(client, payload, add, react_roles)

    if add and payload.channel_id == channel_ids['submissions']:
        if emoji == "✅":
            await update_participants_message(client, payload, channel_ids, message_ids)
        elif emoji == "❌":
            await create_support_thread(client, payload, channel_ids)

async def create_support_thread(client, payload, channel_ids):
    support_channel = client.get_channel(channel_ids['support'])
    if support_channel:
        try:
            message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if message:
                # Extract the challenge information and mention
                correct_pattern = re.match(r'^(Scratch|Python)\s-\sDesafio\s(\d+)\s(<@\d{17,19}>)', message.content)
                if correct_pattern:
                    challenge_info = f"{correct_pattern.group(1)} - Desafio {correct_pattern.group(2)} {correct_pattern.group(3)}"
                    support_message = await support_channel.send(content=challenge_info)
                    thread = await support_message.create_thread(name=f"Ajuda para {message.author.display_name}")
                    await thread.send(f"Olá, parece que precisas de ajuda com o teu desafio. Por favor, descreve a tua dúvida aqui.")
                    print(f"Support thread created for {message.author.display_name}.")
                else:
                    print(f"Message content does not match the expected pattern.")
            else:
                print(f"Message with ID {payload.message_id} not found.")
        except discord.errors.NotFound:
            print(f"Message with ID {payload.message_id} not found.")
        except discord.errors.HTTPException as e:
            print(f"Failed to create thread: {e}")

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
    correct_pattern = re.match(r'^(Scratch|Python)\s-\sDesafio\s(\d+)\s(<@\d{17,19}>)', message.content)
    if correct_pattern:
        language = correct_pattern.group(1)
        level = int(correct_pattern.group(2))
        participant = correct_pattern.group(3)

        scratch_level_1, scratch_level_2, scratch_level_3, python_level_1, python_level_2 = extract_sections(participants_message.content)
        if (language == "Scratch" and level in [1, 2, 3] and participant not in locals()[f'scratch_level_{level}']) or (language == "Python" and level in [1, 2] and participant not in locals()[f'python_level_{level}']):
            updated_message = update_message(participants_message.content, participant, language, level)
            await participants_message.edit(content=updated_message)
            print(f'Participants message updated with new content: {updated_message}')

async def handle_dm(client, message, guild_id, channel_ids):
    guild = client.get_guild(guild_id)
    author = guild.get_member(message.author.id)

    if author is None:
        return

    if discord.utils.get(author.roles, name='Ninjas'):
        correct_pattern = re.match(r'^([sS]cratch|[Pp]ython)\s*-\s*Desafio\s(\d+)\s*\n(.*)', message.content)
        if correct_pattern:
            language = (correct_pattern.group(1))[0].upper() + (correct_pattern.group(1))[1:]
            level = int(correct_pattern.group(2))
            message_content = correct_pattern.group(3)
            if (language == "Scratch" and level in [1, 2, 3]) or (language == "Python" and level in [1, 2]):
                submissions_channel = client.get_channel(channel_ids['submissions'])
                await submissions_channel.send(f"{language} - Desafio {level} <@{author.id}> {message_content}")
                await message.author.send("A tua submissão foi recebida com sucesso e será validada em breve.")
            else:
                await message.author.send("O nível do desafio está fora dos níveis disponíveis. Por favor, verifica e tenta novamente.")
        else:
            await message.author.send("O formato da mensagem está incorreto. Por favor, segue o formato: ```Linguagem - Desafio Nível\nConteúdo```")

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
