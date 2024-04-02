import asyncio
import enum
import os
import psutil
from re import A
import typing
import time
import inspect
import settings
import discord
from discord.ext import commands

# pip install git+https://github.com/Rapptz/discord.py
from discord import app_commands
from constants import *


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)
logger = settings.logging.getLogger("bot")


class GameServer:
    _current_servers = []

    def __init__(self, name, **kwargs):
        """GameServer class intended for tracking live servers"""
        self.name = name
        self.spawn_time = time.time()
        self.command_cooldown = kwargs.get("command_cooldown", 0)
        self.is_shutting_down = kwargs.get("is_shutting_down", False)
        self.is_running = kwargs.get("is_running", False)
        self.shutdown_delay = kwargs.get("shutdown_delay", 0)
        self.auto_start = kwargs.get("auto_start", False)

        GameServer._current_servers.append(
            {
                "name": self.name,
                "spawn_time": self.spawn_time,
                "command_cooldown": self.command_cooldown,
                "shutting_down": self.is_shutting_down,
                "is_running": self.is_running,
                "shutdown_delay": self.shutdown_delay,
                "auto_start": self.auto_start,
            }
        )
        print(GameServer._current_servers)

    def get_current_servers():
        return GameServer._current_servers

    def can_destroy(self):
        return time.time() > self.spawn_time + 6


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    bot.tree.copy_global_to(guild=settings.GUILDS_ID)
    await bot.tree.sync(guild=settings.GUILDS_ID)
    await set_status()


async def set_status():
    # Set Initial Status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="your commands"
        ),
        status=discord.Status.do_not_disturb,
    )
    logger.info("Bot Presence Set")


# DRINK MENU HELPER
async def drink_autocompletion(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    drinks = ["beer", "milk", "tea", "coffee", "juice"]
    return [
        app_commands.Choice(name=drink_choice, value=drink_choice)
        for drink_choice in drinks
        if current.lower() in drink_choice.lower()
    ]


# DRINK
@bot.tree.command(description="take a drink from the bar")
@app_commands.autocomplete(item=drink_autocompletion)
@app_commands.describe(item="drinks to choose from")
async def drink(interaction: discord.Interaction, item: str):
    logger.info(
        f"[drink] '{interaction.user}' used /drink in channel #{interaction.channel}"
    )
    if item.lower() in ["beer", "milk", "tea", "coffee", "juice"]:
        await interaction.response.send_message(f"Enjoy your {item}", ephemeral=True)
    else:
        await interaction.response.send_message(
            f"We don't have any {item}", ephemeral=True
        )


# EMBED
@bot.tree.command(description="embeded respsonse example")
async def embed(interaction: discord.Interaction):
    logger.info(
        f"[embed] '{interaction.user}' used /embed in channel #{interaction.channel}"
    )
    embedVar = discord.Embed(
        title="Title - Example",
        description="Desc. This is where the description would go",
        color=0x00FF00,
    )
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    await interaction.response.send_message(
        embed=embedVar,
        ephemeral=True,
    )


# PING
@bot.tree.command(description="bot's ping")
async def ping(interaction: discord.Interaction):
    logger.info(
        f"[ping] '{interaction.user}' used /ping in channel #{interaction.channel}"
    )
    await interaction.response.send_message(
        f"```ansi\n"
        + f"""🏓pong: \u001b[{format.bold.value};{text_color.blue.value}m{bot.latency*1000:.2f}{CLEAR_FORMATTING}ms```""",
        ephemeral=True,
    )


# HELP
@bot.tree.command(description="get some help")
async def help(interaction: discord.Interaction):
    logger.info(
        f"[help] '{interaction.user}' used /help in channel #{interaction.channel}"
    )
    await interaction.response.send_message(
        f"No one can help you here... **{str(interaction.user).capitalize()}**",
        ephemeral=True,
    )


# CONTROL MENU HELPER
async def control_autocompletion(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    allowed_process = ["enshrouded"]
    return [
        app_commands.Choice(
            name=process_choice.capitalize(), value=process_choice.capitalize()
        )
        for process_choice in allowed_process
        if current.lower() in process_choice.lower()
    ]


async def action_autocompletion(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    allowed_action = ["start", "kill", "restart"]
    return [
        app_commands.Choice(name=action_choice, value=action_choice)
        for action_choice in allowed_action
        if current.lower() in action_choice.lower()
    ]


ALLOWED_DELAY = {
    "now": 0,
    "15 seconds": 15,
    "30 seconds": 30,
    "1 min": 60,
    "5 min": 300,
}


async def delay_autocompletion(
    interaction: discord.Interaction, delay: str = "now"
) -> list[app_commands.Choice[str]]:
    auto_delay = [key for key in ALLOWED_DELAY.keys()]
    return [
        app_commands.Choice(name=action_choice, value=action_choice)
        for action_choice in auto_delay
        if delay.lower() in action_choice.lower()
    ]


async def delay_error(interaction, delay):
    await interaction.response.send_message(
        f"Delay: '{delay}' not valid. Try selecting existing option or give the amount in seconds!",
        ephemeral=True,
    )


@bot.event
async def on_command_error(interaction, error):
    if isinstance(error, commands.CommandOnCooldown):
        await interaction.response.send_message(f"on cooldown")


# CONTROL
@bot.tree.command(description="control a game server once every 15 seconds")
@app_commands.autocomplete(
    game=control_autocompletion,
    action=action_autocompletion,
    delay=delay_autocompletion,
)
@app_commands.describe(
    game="game servers available for control",
    action="action to take",
    delay="delay action (in seconds)",
)
# @commands.cooldown(1, 15.0, commands.BucketType.user)  # NOT WORKING
async def control(
    interaction: discord.Interaction,
    game: str,
    action: str,
    delay: str = "now",
):
    # \u001b[{format};{color}m
    # \u001b[1;40;32m
    # \u001b[0;0m

    if int(settings.ROLE_POWER_TRIP) not in [
        role.id for role in interaction.user.roles
    ]:
        logger.info(
            f"{interaction.user} | {game.lower()} | {action.lower()} | {delay}-- DENIED"
        )
        await interaction.response.send_message(
            f"You are not allowed to use this command...", ephemeral=True
        )
        return
    if delay not in ALLOWED_DELAY.keys():
        try:
            delay_in_seconds = int(delay)
        except:
            logger.info(
                f"{interaction.user} | {game.lower()} | {action.lower()} | {delay} -- INVALID INPUT"
            )
            await interaction.response.send_message(
                f"**delay:**```{delay}```\n__not valid__\n\n*try selecting existing option or give the amount in seconds!*",
                ephemeral=True,
            )
            return
    else:
        delay_in_seconds = int(ALLOWED_DELAY[delay])

    logger.info(
        f"{interaction.user} | {game.lower()} | {action.lower()} | {delay} -- GRANTED"
    )
    allowed_process = ["enshrouded"]
    allowed_action = ["start", "kill", "restart"]
    if game.lower() not in allowed_process or action.lower() not in allowed_action:
        await interaction.response.send_message(
            f"No one can help you here, {interaction.user}", ephemeral=True
        )
        return

    action_format = 0
    action_emoji = None
    if action.lower() == "start":
        action_format = text_color.green.value
        action_emoji = "🟢"
        if "enshrouded" not in [
            server.get("name") for server in GameServer.get_current_servers()
        ]:
            server = GameServer("enshrouded")

        else:
            print("SERVER ALREADY STARTED")
            await interaction.response.send_message(
                f"```ansi\n" + f"Server Already Running```\n*no action taken*",
                ephemeral=True,
            )
            return
    elif action.lower() == "kill":
        action_format = text_color.red.value
        action_emoji = "🛑"
        for index, item in enumerate(GameServer.get_current_servers()):
            if item.get("name") == "enshrouded":
                print("FOUND SERVER IN LIST")
                GameServer.get_current_servers().pop(index)

    elif action.lower() == "restart":
        action_format = text_color.yellow.value
        action_emoji = "⚠️"

    print([key.get("name") for key in GameServer.get_current_servers()])

    await interaction.response.send_message(
        f"```ansi\n"
        + f"{action_emoji} \u001b[{format.underline.value};{action_format}m{action.capitalize()}ing\u001b[0;0m : \u001b[{format.bold.value};{text_color.blue.value}m{game.capitalize()}\u001b[0;0m {action_emoji}```",
        ephemeral=True,
    )


# Presence
# MOOD MENU HELPER
async def mood_autocompletion(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    mood = ["online", "offline", "dnd", "idle"]
    return [
        app_commands.Choice(name=mood_choice, value=mood_choice)
        for mood_choice in mood
        if current.lower() in mood_choice.lower()
    ]


# MOOD
@bot.tree.command(description="take a drink from the bar")
@app_commands.autocomplete(item=mood_autocompletion)
@app_commands.describe(item="moods to set")
async def mood(interaction: discord.Interaction, item: str):
    if int(settings.ROLE_POWER_TRIP) not in [
        role.id for role in interaction.user.roles
    ]:
        logger.info(f"{interaction.user} | mood | {item} -- DENIED")
        await interaction.response.send_message(
            f"You are not allowed to use this command...", ephemeral=True
        )
        return
    logger.info(f"{interaction.user} | mood | {item} -- GRANTED")
    presence = bot.get_cog("hal")
    await presence.cmds(item)
    await interaction.response.send_message(
        f"No one can help you here... **{str(interaction.user).capitalize()}**",
        ephemeral=True,
    )


# JOKE
@bot.tree.command(description="get some help")
async def joke(interaction: discord.Interaction):
    logger.info(
        f"[joke] '{interaction.user}' used /joke in channel #{interaction.channel}"
    )
    jokes = bot.get_cog("jokes")
    await jokes.cmds(interaction)
    # await interaction.response.send_message(
    #     embed=Q,
    #     ephemeral=True,
    # )


async def main():
    # load()
    await load()
    await bot.start(settings.DISCORD_API_SECRET)
    # bot.run(settings.DISCORD_API_SECRET)


if __name__ == "__main__":
    asyncio.run(main())
    # main()
