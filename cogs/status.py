import discord
from discord.ext import commands


class status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("status cog loaded")


async def setup(bot):
    await bot.add_cog(status(bot))