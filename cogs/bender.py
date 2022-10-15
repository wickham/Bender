import discord
from discord.ext import commands
from apikeys import *
import time
from libs import jokes


class bender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("bender cog loaded")

    @commands.Cog.listener("on_message")
    async def cmds(self, message):
        command_list = ["online", "offline", "dnd", "idle", "joke"]

        msg_content = message.content.lower()
        # Bot Primary Commands
        if any(word in msg_content for word in ["!bender"]) and any(
            word in msg_content for word in command_list
        ):
            if (
                STAFFROLE in [y.id for y in message.author.roles]
                and "online" in msg_content
            ):
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.listening, name="how great I am!"
                    ),
                    status=discord.Status.online,
                )
            elif (
                STAFFROLE in [y.id for y in message.author.roles]
                and "offline" in msg_content
            ):
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.listening, name="how great I am!"
                    ),
                    status=discord.Status.offline,
                )
            elif (
                STAFFROLE in [y.id for y in message.author.roles]
                and "dnd" in msg_content
            ):
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.listening, name="how great I am!"
                    ),
                    status=discord.Status.do_not_disturb,
                )
            elif (
                STAFFROLE in [y.id for y in message.author.roles]
                and "idle" in msg_content
            ):
                await self.bot.change_presence(
                    activity=discord.Activity(
                        type=discord.ActivityType.listening, name="how great I am!"
                    ),
                    status=discord.Status.idle,
                )
            elif "joke" in msg_content:
                Q, A = jokes.tell_joke()
                await message.channel.send(embed=Q)
                time.sleep(5)
                await message.channel.send(embed=A)
            elif "lastmessage" in msg_content:
                """Get the last message of a text channel."""
                channel = self.bot.get_channel(PENDINGID)
                if channel is None:
                    await message.channel.send("Could not find that channel.")
                    return
                # NOTE: get_channel can return a TextChannel, VoiceChannel,
                # or CategoryChannel. You may want to add a check to make sure
                # the ID is for text channels only

                message = await channel.fetch_message(channel.last_message_id)
                # NOTE: channel.last_message_id could return None; needs a check

                await message.channel.send(
                    f"Last message in {channel.name} sent by {message.author.name}:\n"
                    + message.content
                )
            else:
                await message.channel.send(
                    f"'{msg_content[8:]}' DOES NOT COMPUTE... Psh"
                )
            # await message.author.send(f"{msg_content}    yourself!")
            # time.sleep(5)
            await message.delete()


async def setup(bot):
    await bot.add_cog(bender(bot))
