import discord
import random
import os

from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta


import logging as log

from discord.ui import Select, View, Button

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
REVIEWS_CHANNEL_ID = 1288979882507894805
ORDERS_CHANNEL_ID = 1288986972257390602

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


    channel = bot.get_channel(REVIEWS_CHANNEL_ID)

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


# Crear un comando de barra usando el decorador tree.command
@bot.tree.command(name="ticket-template", description="Crea un ticket a través de una plantilla")
async def ticket_template(interaction: discord.Interaction):
    CUSTOMER_IN_SUPPORT_ROLE = "💻 Customer in Support 💻"
    CUSTOMER_RESOLVED_ROLE = "✅ Customer Resolved ✅"

    embed = discord.Embed(title="Orders System", description="Select an option to create an order")

    select = Select(
        placeholder="Selecciona el tipo de ticket...",
        options=[
            discord.SelectOption(label="Order from Fiverr", description="Support for Fiverr orders", emoji="🛒"),
            discord.SelectOption(label="Bot Improvement Support", description="Support to improve a bot", emoji="🤖")
        ]
    )

    # Definir la función callback para el select (desplegable)
    async def select_callback(interaction_select: discord.Interaction):
        selected_option = select.values[0]
        if selected_option == "Order from Fiverr":
            tipo_ticket = "Fiverr-order"
        elif selected_option == "Bot Improvement Support":
            tipo_ticket = "Bot-support"

        # Crear una categoría personalizada usando el username del cliente
        username = interaction_select.user.name
        category_name = f"{tipo_ticket}-{username}"
        category = discord.utils.get(interaction_select.guild.categories, name=category_name)
        if category is None:
            # Configuración de permisos
            overwrites = {
                interaction_select.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                # Ocultar canales para todos
                interaction_select.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                # Solo el usuario puede ver y enviar mensajes
                interaction_select.guild.me: discord.PermissionOverwrite(view_channel=True)
                # El bot debe ver los canales
            }
            category = await interaction_select.guild.create_category(category_name, overwrites=overwrites)

        # Crear canales de texto y voz asociados al ticket con los mismos permisos
        general_channel = await interaction_select.guild.create_text_channel('💬 ┆ General Chat', category=category,
                                                                             overwrites=overwrites)
        bot_tests_channel = await interaction_select.guild.create_text_channel('🤖 ┆ Bot tests', category=category,
                                                                               overwrites=overwrites)
        meetings_channel = await interaction_select.guild.create_voice_channel('🎧 ┆ Meetings', category=category,
                                                                               overwrites=overwrites)

        # Asignar el rol al usuario que abrió el ticket
        role = discord.utils.get(interaction_select.guild.roles, name=CUSTOMER_IN_SUPPORT_ROLE)
        if role:
            await interaction_select.user.add_roles(role)

        # Notificar al usuario sobre los canales creados
        await general_channel.send(
            f"{interaction_select.user.mention}, your ticket has been created. This is the general chat with your developer.")
        await bot_tests_channel.send(f"You can test your custom bot here!")
        await interaction_select.response.send_message(f"¡Your category and channels have been created: {category_name}!",
                                                       ephemeral=True)

        # Crear un botón para cerrar el ticket
        close_button = Button(label="Close Ticket", style=discord.ButtonStyle.danger)

        # Definir la función callback para cerrar el ticket
        async def close_ticket(interaction_close: discord.Interaction):
            # Obtiene la categoría donde se encuentra el ticket
            category = interaction.channel.category

            if category is None or not category.name.startswith("Fiverr-order-") and not category.name.startswith(
                    "Bot-support-"):
                await interaction.response.send_message(
                    "This command can only be used within a ticket category.", ephemeral=True)
                return

            # Asignar rol al usuario antes de eliminar
            role_to_assign = discord.utils.get(interaction.guild.roles, name=CUSTOMER_RESOLVED_ROLE)

            if role_to_assign:
                await interaction.user.add_roles(role_to_assign)
                await interaction.response.send_message(f"You've been assigned as: {role_to_assign.name}.",
                                                        ephemeral=True)

            # Eliminar los canales de texto y voz
            for channel in category.channels:
                await channel.delete()

            # Eliminar la categoría
            await category.delete()

            # Mensaje final
            await interaction.followup.send(
                "The ticket has been closed and all associated channels have been deleted.", ephemeral=True)

        # Asignar la función callback al botón
        close_button.callback = close_ticket

        # Crear una vista para el botón
        close_view = View()
        close_view.add_item(close_button)

        # Enviar el mensaje de confirmación con el botón
        await interaction_select.response.send_message(embed=embed, view=close_view)


    # Asignar el callback al select
    select.callback = select_callback

    # Crear una vista para el select (desplegable)
    view = View()
    view.add_item(select)

    # Enviar el embed con el select (desplegable) a un canal específico
    target_channel = bot.get_channel(ORDERS_CHANNEL_ID)  # Obtén el canal por su ID
    if target_channel:
        await target_channel.send(embed=embed, view=view)
        await interaction.response.send_message("Embed created in Orders channel", ephemeral=True)
    else:
        await interaction.response.send_message("Channel not found", ephemeral=True)


def run_bot():
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_bot()
