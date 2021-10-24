import time
import discord
import pygit2
import itertools
import datetime

from discord.ext import commands
from handler import slash_command, InteractionContext
from utils.bot import SquidGame
from typing import Union

# Several Command are made by Nirlep and Blue.
# thank them uwu
# do it or I will eat you up 😏


def format_commit(commit: pygit2.Commit) -> str:
    # CREDITS: https://github.com/Rapptz/RoboDanny
    short, _, _ = commit.message.partition('\n')
    short_sha2 = commit.hex[0:6]
    commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
    commit_time = datetime.datetime.fromtimestamp(
        commit.commit_time).astimezone(commit_tz)

    offset = f'<t:{int(commit_time.astimezone(datetime.timezone.utc).timestamp())}:R>'
    return f'[`{short_sha2}`](https://github.com/KiritoGuy/SquidGame/commit/{commit.hex}) {short} ({offset})'


def get_commits(count: int = 3):
    # CREDITS: https://github.com/Rapptz/RoboDanny
    repo = pygit2.Repository('.git')
    commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
    return '\n'.join(format_commit(commit) for commit in commits)


class Info(commands.Cog):
    def __init__(self, bot: SquidGame):
        self.bot = bot

    @commands.command(name="github", help="The github repo to my source code.")
    @slash_command(name="github", help="The github repo to my source code.")
    async def github(self, ctx: Union[commands.Context, InteractionContext]):
        await ctx.reply(embed=discord.Embed(title="Github", description="Star the code on [github](https://github.com/QuantumGamerLive/SquidGame/) it means a lot", color=discord.Color.blurple()))

    @commands.command(name="invite", help="Invite me to your server uwu")
    @slash_command(name="invite", help="Invite me to your server uwu")
    async def invite(self, ctx: Union[commands.Context, InteractionContext]):
        await ctx.reply(embed=discord.Embed(
            title="🔗 Click here to invite Squid Game Bot!",
            description="""
links:
- [Invite](https://discord.com/oauth2/authorize?client_id=897715038587068456&permissions=8&scope=bot%20applications.commands)
- [Support Server](https://discord.gg/4URvnKHNK2)
- [Github](https://github.com/QuantumGamerLive/SquidGame)
                    """,
            url=f"https://discord.com/oauth2/authorize?client_id=897715038587068456&permissions=8&scope=bot%20applications.commands",
            color=discord.Color.blurple()
        ).set_footer(text="Thank you very much! 💖", icon_url=self.bot.get_user(753247226880589982).display_avatar.url))

    @commands.command(name="botinfo", help="Get some info about me!")
    @slash_command(name="botinfo", help="Get some info about me!")
    async def botinfo(self, ctx: Union[commands.Context, InteractionContext]):
        embed = discord.Embed(
            title=f"{self.bot.config.emojis.yes} Info about me!",
            description="A Discord Bot Which Is Based On A Famous Netflix Show Called Squid Game",
            color=discord.Color.blurple(),
            timestamp=datetime.datetime.utcnow()
        ).add_field(
            name="Stats:",
            value=f"""
**Servers:** {len(self.bot.guilds)}
**Users:** {len(self.bot.users)}
**Commands:** {len(self.bot.commands)}
            """,
            inline=True
        ).add_field(
            name="Links:",
            value=f"""
- [Support Server](https://discord.gg/4URvnKHNK2)
- [Github](https://github.com/QuantumGamerLive/SquidGame)
- [Invite](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands)
            """,
            inline=True
        ).set_footer(text=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        ).set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        ).set_thumbnail(url=self.bot.user.display_avatar.url)
        try:
            embed.add_field(
                name="Latest Commits:",
                value=get_commits(),
                inline=False
            )
        except Exception as e:
            print(f"{e}")
            pass
        await ctx.reply(embed=embed)

    @commands.command(name="credits", help="Credits to our contributors and helpers!")
    @slash_command(name="credits", help="Credits to our contributors and helpers!")
    async def credits(self, ctx: Union[commands.Context, InteractionContext]):
        embed = discord.Embed(
            title="Squid Game Bot Credits",
            description="""
**Owner:** [Kirito Guy#9521](https://discord.com/users/753247226880589982)

**took help from:** 
Nirlep_5252_#9798 and Blue.#1270

**Contributor(s):**
Currently no one :(

**Github:**
https://github.com/QuantumGamerLive/SquidGame
            """,
            color=discord.Color.blurple()
        ).set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar.url
        ).set_thumbnail(url=self.bot.user.display_avatar.url
        ).set_footer(text="Created By Kirito Guy", icon_url=self.bot.get_user(753247226880589982).display_avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(name="ping", help="Pong!")
    @slash_command(name="ping", help="Pong!")
    async def ping(self, ctx: Union[commands.Context, InteractionContext]):
        api_ping = round(self.bot.latency * 1000, 2)
        db_base_time = time.perf_counter()
        db_ping = round((time.perf_counter() - db_base_time) * 1000, 2)
        base_time = time.perf_counter()
        msg = await ctx.reply("Pinging...")
        msg = msg or await ctx.original_message()
        await msg.edit(content="UwU!~", embed=discord.Embed(
            title="Pong!",
            description=f"""
**API Ping:** {api_ping}ms
**Bot Ping:** {round((time.perf_counter() - base_time) * 1000, 2)}ms
**DB Ping:** {db_ping}ms
""",
            color=discord.Color.blurple()
        ))


def setup(bot):
    bot.add_cog(Info(bot))
