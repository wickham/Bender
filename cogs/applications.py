import discord
import emoji
from discord.utils import get
from discord.ext import commands
from apikeys import *
from discord.ext.commands import has_permissions, MissingPermissions


class applications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("applications cog loaded")

    @commands.Cog.listener("on_message")
    @has_permissions(manage_messages=True)
    async def incoming_app(self, message):
        msg_content = message.content.lower()
        # Bot Primary Commands
        if PENDINGID == message.channel.id:
            print("[applications] NEW APPLICATION")
            # Grab our last message content and replicate
            content = {}
            for item in message.embeds:
                content["author"] = item.author
                content["title"] = item.title
                content["description"] = item.description
                content["description"] = content["description"].split("\n")
                for index, item in enumerate(content["description"]):
                    if "**Discord**" == item:
                        discord_name = content["description"][index + 1]
                    if "Discord ID" in item:
                        discord_id = content["description"][index + 1]
            discord_obj_from_id = await self.bot.fetch_user(discord_id)
            if str(discord_name).lower() == str(discord_obj_from_id).lower():
                # we have a match, proceed
                print(f"[applications] DATA MATCH")
                """ check if user is on server and not already in group '1027839390849966092
                    if they are, we make a new post with same data, but with reaction approvals
                    ...
                    when approved, we delete the message and move to "APPROVED APPLICATIONS" """
                guild = self.bot.get_guild(GUILDID)

                if guild.get_member(int(discord_id)):
                    if "member" in [
                        y.name.lower()
                        for y in (guild.get_member(int(discord_id)).roles)
                    ]:
                        print("[applications] applicant already approved!")
                        title = "DINGUS, YOURE ALREADY APPROVED!\n"
                        msg = "Visit: [#👋・welcome](https://discord.gg/9VdHkjc5Vv)"
                        messageDM = "DINGUS, YOURE ALREADY APPROVED!\nVisit: [#👋・welcome](https://discord.gg/9VdHkjc5Vv)"
                        embed = discord.Embed(title=title, description=msg).set_author(
                            name="ChronoRP", icon_url="https://i.imgur.com/knLQPpi.png"
                        )
                        user = get(self.bot.get_all_members(), id=int(discord_id))

                        if user:
                            await user.send(embed=embed)
                            await message.delete()
                            # found the user
                        else:
                            # Not found the user
                            print("[applications] User is no longer in the discord!")
                    else:

                        # They need approval or denial (the river in Egypt)
                        yes = await guild.fetch_emoji(EMOJIS["yes"])
                        no = await guild.fetch_emoji(EMOJIS["no"])
                        warn = await guild.fetch_emoji(EMOJIS["warning"])

                        print("[applications] ADDING REACTIONS")
                        moji_list = [yes, no, warn]
                        for item in moji_list:
                            await message.add_reaction(f"{item}")
            else:
                print(
                    "[applications] EITHER NOT IN DISCORD OR INCORRECT INFORMATION FED"
                )

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self, reaction, user):
        embed = reaction.message.embeds[0]
        emoj = reaction.emoji
        guild = self.bot.get_guild(GUILDID)
        yes = await guild.fetch_emoji(EMOJIS["yes"])
        no = await guild.fetch_emoji(EMOJIS["no"])
        warn = await guild.fetch_emoji(EMOJIS["warning"])
        reverse = await guild.fetch_emoji(EMOJIS["unoreverse"])

        if user == self.bot.user:
            return
        content = {}
        for item in reaction.message.embeds:
            content["author"] = item.author
            content["title"] = item.title
            content["description"] = item.description

            for index, item in enumerate(content["description"]):
                if "**Discord**" == item:
                    discord_name = content["description"][index + 1]
                if "Discord ID" in item:
                    discord_id = content["description"][index + 1]

        content["description"] = content["description"].split("\n")

        for index, item in enumerate(content["description"]):
            if "**Discord**" == item:
                discord_name = content["description"][index + 1]
            if "Discord ID" in item:
                discord_id = content["description"][index + 1]

        if emoj == yes:
            print("YES")
            # APPROVE
            channel = self.bot.get_channel(APPROVEDID)

            await channel.send(
                embed=discord.Embed(
                    title="",
                    url="",
                    description=embed.description,
                    color=0x42FF5F,
                )
            )
            await reaction.message.delete()
            # Message user about good news
            # Giver user role

            member = guild.get_member(int(discord_id))
            role = get(guild.roles, id=MEMBERROLE)
            denied = get(guild.roles, id=DENIEDROLE)

            await member.add_roles(role)
            for role in member.roles:
                if role.id == DENIEDROLE:
                    print("removing denied role")
                    await member.remove_roles(denied)
            # message user
            title = "Congratulations!\n"
            msg = """You've been __**accepted**__\nNOW GET OUT THERE MEAT BAG AND MAKE BENDER PROUD!\n\n
                    Few Channels to Visit:\n
                    [👋・welcome](https://discord.gg/9VdHkjc5Vv)\n
                    [📜・table-of-contents](https://discord.com/channels/979545493577293824/1029181982783045646)\n
                    [✨・self-role](https://discord.com/channels/979545493577293824/1028127399583432735)\n
                    *and learn what to do next*."""
            embed = discord.Embed(
                title=title, description=msg, color=0x42FF5F
            ).set_author(
                name="ChronoRP",
                icon_url="https://i.imgur.com/knLQPpi.png",
            )
            await member.send(embed=embed)
        elif emoj == no:
            # DENY
            print("DENIED")
            channel = self.bot.get_channel(DENIEDID)

            # Move the document
            moved = await channel.send(
                embed=discord.Embed(
                    title="", url="", description=embed.description, color=0xF73B31
                )
            )
            await reaction.message.delete()
            await moved.add_reaction(f"{reverse}")
            # Message User
            member = guild.get_member(int(discord_id))
            role = get(guild.roles, id=DENIEDROLE)
            await member.add_roles(role)

            # message user
            application = await channel.fetch_message(channel.last_message_id)
            embed = discord.Embed(
                description=reaction.message.embeds[0].description,
                color=0xFFFFFF,
            )
            await member.send(embed=embed)

            title = "Sorry.\n"
            msg = f"""Your application was __**denied**__\nYou may be able to re-apply!\n\n
                    Review your application above to see maybe where it can be improved...\n
                    Visit the channel below if you would like to appeal or find out more.\n
                    [SUPPLY THIS DENIED URL!](https://discord.com/channels/{GUILDID}/{DENIEDID}/{application.id})\n
                    [🏰・appeal](https://discord.com/channels/979545493577293824/1029928358588465162)\n
                    """
            embed = discord.Embed(
                title=title,
                description=msg,
                color=0xF73B31,
            ).set_author(
                name="ChronoRP",
                icon_url="https://i.imgur.com/knLQPpi.png",
            )
            message = await member.send(embed=embed)
        elif emoj == warn:
            print("warning")
            channel = self.bot.get_channel(PENDINGID)
            await reaction.message.delete()
            message = await channel.send(
                embed=discord.Embed(
                    title="",
                    url="",
                    description=embed.description,
                    color=0xF5D60F,
                )
            )
            yes = await guild.fetch_emoji(EMOJIS["yes"])
            no = await guild.fetch_emoji(EMOJIS["no"])
            moji_list = [yes, no]
            for item in moji_list:
                await message.add_reaction(f"{item}")
        elif emoj == reverse:
            print("reversed ban")
            channel = self.bot.get_channel(PENDINGID)
            await reaction.message.delete()
            message = await channel.send(
                embed=discord.Embed(
                    title="",
                    url="",
                    description=embed.description,
                    color=0xF5D60F,
                )
            )
            moji_list = [yes, no, warn]
            for item in moji_list:
                await message.add_reaction(f"{item}")
        else:
            return


async def setup(bot):
    await bot.add_cog(applications(bot))