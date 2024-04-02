import discord
from discord.ext import commands
from constants import *
import settings
import libs.jokes as joke_book
from discord import app_commands


logger = settings.logging.getLogger("cog")


class jokes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Cool Command Name",
            callback=self.cmds,  # set the callback of the context menu to "my_cool_context_menu"
        )
        self.bot.tree.add_command(self.ctx_menu)  # add the context menu to the tree

    @commands.Cog.listener()
    async def on_ready(self):
        """This will wait for someone to react with `😎`
        and add him a role

        Note: This will wait only for one reaction"""
        logger.info("jokes cog loaded")

        channel_id = 1216524312949817444
        # Getting the channel
        channel = self.bot.get_channel(channel_id)
        # Getting the role
        # role = discord.utils.get(channel.guild.roles, name="Orange")
        # Sending the message
        message = await channel.send("React to me")

        def check(reaction, user):
            """Checks if the reaction message is the one sent before
            and if the reaction is `😎`"""
            return reaction.message == message and str(reaction) == "😎"

        # Waiting for the reaction
        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        # Adding the role
        # await user.add_roles(role)
        await channel.send("Thats pretty cool")

    async def dm(self, ctx, user: discord.User):
        if user != None:
            if user != ctx.author:
                players = [ctx.author, user]
                for player in players:
                    message = await player.send("test")

                    await message.add_reaction("👍")
                    await message.add_reaction("👎")

                    def check(reaction, user):
                        return user == player and str(reaction.emoji) in ["👍", "👎"]

                    response = await self.bot.wait_for("reaction_add", check=check)
                    if str(response[0]) == "👍":
                        await player.send(str(response[0]))
                    else:
                        await player.send("👎")

        # @commands.Cog.listener("on_message")
        async def cmds(
            self, interaction: discord.Interaction, message: discord.Message
        ):
            command_list = ["99", "online", "offline", "dnd", "idle", "joke"]

            # msg_content = message.content.lower()

            print(message)
            Q, A = joke_book.tell_joke()


async def setup(bot):
    await bot.add_cog(jokes(bot))
