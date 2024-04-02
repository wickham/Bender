import discord
from discord.ext import commands
from constants import *
import settings
import time
import logging
from libs import jokes

logger = settings.logging.getLogger("cog")


class hal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("hal cog loaded")

    # @commands.Cog.listener("on_message")
    async def cmds(self, message):
        import random

        command_dict = {
            "online": discord.Status.online,
            "offline": discord.Status.offline,
            "dnd": discord.Status.do_not_disturb,
            "idle": discord.Status.idle,
        }
        command = message.lower()
        logger.info(f"'{command}' was given!")
        # Bot Primary Commands
        if command in command_dict.keys():
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name=random.choice(
                        [
                            "your command",
                            "a bird chirping",
                            "nothing...",
                            "...",
                            "cheeks clapping",
                            "the silence",
                        ]
                    ),
                ),
                status=command_dict[command],
            )
            # elif "joke" in msg_content:
            #     Q, A = jokes.tell_joke()
            #     await message.channel.send(embed=Q)
            #     time.sleep(5)
            #     await message.channel.send(embed=A)
        else:
            print("ESCAPE ME")
            # await message.channel.send(f"'{msg_content}' DOES NOT COMPUTE... Psh")
            # await message.author.send(f"{msg_content}    yourself!")
            # await message.delete()


async def setup(bot):
    await bot.add_cog(hal(bot))
