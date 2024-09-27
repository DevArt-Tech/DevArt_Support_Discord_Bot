import discord
import random
import os

from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta


import logging as log

# Configurar el sistema de logging
log.basicConfig(level=log.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# permissions
intents = discord.Intents.default()
# Allows the bot to read message content to process commands. This is essential if your bot will respond to messages.
intents.message_content = True

# Necessary if your bot needs to react to events related to members, such as when someone joins or leaves the server.
intents.members = True

# Required for handling events related to guilds, such as server configuration updates or when roles are added or
# removed.
intents.guilds = True

# Enables the bot to detect and respond to reactions on messages.
intents.reactions = True

DISCORD_TOKEN = os.environ["discord_token"]

# Configura tu bot con los intents y el prefijo
bot = commands.Bot(command_prefix='y!', intents=intents, help_command=None)


@bot.event
async def on_ready():
    log.info(f'{bot.user} is ready.')
    bot.start_time = datetime.now()
    try:
        synced = await bot.tree.sync()
        log.info(f'Sync {len(synced)} commands')

    except Exception as e:
        log.error(f'Error while sync commands: {e}')


@bot.tree.command(name="status")
async def status(interaction: discord.Interaction):
    """It shows information about the bot status"""
    latency = bot.latency  # Latencia en segundos
    status = "Online ✅️" if bot.is_ready() else "Offline ❌"
    uptime = datetime.now() - bot.start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="Bot Information",
        description=f"Relevant Data \n\n"
                    f"**Bot Status: **{status}\n"
                    f"**Latency: **{latency * 1000:.2f} ms\n"
                    f"**Time Online: **{days} days, {hours} hours, {minutes} minutes, {seconds} seconds\n\n",
        color=discord.Color.from_rgb(15, 33, 73)
    )
    current_directory = os.getcwd()
    log.info(current_directory)
    image_path = os.path.join('img', 'logo2.jpg')
    complete_path = os.path.join(current_directory, image_path)
    log.info(image_path)
    embed.set_thumbnail(url=complete_path)
    embed.set_footer(text="Powered by: 💻 DevArt 💻 - Arturo B.")

    with open(complete_path, 'rb') as f:
        file = discord.File(f, filename='logo2.jpg')
        embed.set_thumbnail(url='attachment://logo2.jpg')
        await interaction.response.send_message(file=file, embed=embed)


@bot.tree.command(name="reviews-template")
async def reviews_template(interaction: discord.Interaction):
    """It shows information about the reviews template"""

    reviews_channel_id = 1288979882507894805
    channel = bot.get_channel(reviews_channel_id)

    embed = discord.Embed(
        title="⭐ Reviews ⭐",
        description=f"*To post a review after the development of any project, please fill in the following template:* \n\n"
                    f"**Project Name: ** \n"
                    f"**Stars from 1 to 5 ⭐: ** \n"
                    f"**Comments: ** \n\n",
        color=discord.Color.from_rgb(15, 33, 73)
    )
    current_directory = os.getcwd()
    log.info(current_directory)
    image_path = os.path.join('img', 'logo2.jpg')
    complete_path = os.path.join(current_directory, image_path)
    log.info(image_path)
    embed.set_thumbnail(url=complete_path)
    embed.set_footer(text="Powered by: 💻 DevArt 💻 - Arturo B.")

    with open(complete_path, 'rb') as f:
        file = discord.File(f, filename='logo2.jpg')
        embed.set_thumbnail(url='attachment://logo2.jpg')
        await channel.send(file=file, embed=embed)
        await interaction.response.send_message("Template sent!")


'''@bot.tree.command(name="rank-up")
async def rank_up(interaction: discord.Interaction, member: discord.Member, new_role: discord.Role):
    """ Asciende a un miembro de la Yakuza y muestra un mensaje sobre ello """

    for category, subranks in c.config["ranks"].items():
        possible_roles = [category] + (subranks or [])
        member_roles = member.roles
        if any(role.name in possible_roles for role in member_roles):
            roles_to_remove = [role for role in member_roles if role.name == category or (subranks and role.name in subranks)]

            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)

    # Asigna el nuevo rango
    await member.add_roles(new_role)

    for category, subranks in c.config["ranks"].items():
        if subranks and new_role.name in subranks:
            category_role = discord.utils.get(member.guild.roles, name=category)
            if category_role:
                await member.add_roles(category_role)

    if new_role.name == "ASCENSO A KYODAI":
        random_answer = give_random_answer("rank_up", "bot_answers_phase")
    else:
        random_answer = give_random_answer("rank_up")

    await interaction.response.send_message(random_answer.format(member.mention, new_role.mention))


@bot.tree.command(name="rank-down")
async def rank_down(interaction: discord.Interaction, member: discord.Member, new_role: discord.Role):
    """ Desciende el rango a un miembro de la Yakuza y muestra un mensaje sobre ello """

    for category, subranks in c.config["ranks"].items():
        possible_roles = [category] + (subranks or [])
        member_roles = member.roles
        if any(role.name in possible_roles for role in member_roles):
            roles_to_remove = [role for role in member_roles if role.name == category or (subranks and role.name in subranks)]

            if roles_to_remove:
                await member.remove_roles(*roles_to_remove)

    # Asigna el nuevo rango
    await member.add_roles(new_role)

    for category, subranks in c.config["ranks"].items():
        if subranks and new_role.name in subranks:
            category_role = discord.utils.get(member.guild.roles, name=category)
            if category_role:
                await member.add_roles(category_role)

    if new_role.name == "ASCENSO A KYODAI":
        random_answer = give_random_answer("rank_down", "bot_answers_phase")
    else:
        random_answer = give_random_answer("rank_down")
    await interaction.response.send_message(random_answer.format(member.mention, new_role.mention))


def give_random_answer(command, sub_command="bot_answers"):
    if c.config is not None:
        bot_anwser = random.choice(c.config["commands"][command][sub_command])
        print(f'Respuesta escogida: {bot_anwser}')
        return bot_anwser'''


def run_bot():
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_bot()
