#!/usr/bin/env python3
# main.py
import os
import asyncio
import discord
from discord.ext import commands
from apikeys import *

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print("BOT ONLINE!")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="how great I am!"
        ),
        status=discord.Status.do_not_disturb,
    )


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("__init__"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await bot.start(BOTTOKEN)


asyncio.run(main())
