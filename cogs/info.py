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
    return f'[`{short_sha2}`](https://github.com/QuantumGamerLive/SquidGame/commit/{commit.hex}) {short} ({offset})'


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
            title="🔗 Click me to invite!",
            description="""
Other links:

- [Support Server](https://discord.gg/4URvnKHNK2)
- [Github](https://github.com/QuantumGamerLive/SquidGame)
                    """,
            url=f"https://discord.com/oauth2/authorize?client_id=897715038587068456&permissions=8&scope=bot%20applications.commands",
            color=discord.Color.blurple()
        ).set_footer(text="Thank you very much! 💖", icon_url=self.bot.get_user(753247226880589982).display_avatar.url))

    @commands.command(name="bot-info", help="Get some info about me!")
    @slash_command(name="bot-info", help="Get some info about me!")
    async def botinfo(self, ctx: Union[commands.Context, InteractionContext]):
        msg = await ctx.reply(embed=discord.Embed(title=f"Loading... {EMOJIS['loading']}"))
        embed = discord.Embed(
            title="Information About Me!",
            description="I am a simple, multipurpose Discord bot, built to make ur Discord life easier!",
            color=MAIN_COLOR
        ).set_thumbnail(url=self.client.user.display_avatar.url)
        embed.add_field(
            name="Stats",
            value=f"""
```yaml
Servers: {len(self.client.guilds)}
Users: {len(set(self.client.get_all_members()))}
Total Commands: {len(self.client.commands)}
Uptime: {str(datetime.timedelta(seconds=int(round(time.time()-start_time))))}
Version: alpha
```
            """,
            inline=False
        )
        async with self.client.session.get("https://statcord.com/logan/stats/751100444188737617") as r:
            ah_yes = await r.json()
        embed.add_field(
            name="Statcord Stats",
            value=f"""
```yaml
Commands Ran Today: {ah_yes['data'][::-1][0]['commands']}
Most Used Command: {ah_yes['data'][::-1][0]['popular'][0]['name']} - {ah_yes['data'][::-1][0]['popular'][0]['count']} uses
Memory Usage: {'%.1f' % float(int(ah_yes['data'][::-1][0]['memactive'])/1000000000)} GB / {'%.1f' % float(int(psutil.virtual_memory().total)/1000000000)} GB
Memory Load: {ah_yes['data'][::-1][0]['memload']}%
CPU Load: {ah_yes['data'][::-1][0]['cpuload']}%
```
            """,
            inline=False
        )
        embed.add_field(
            name="Links",
            value=f"""
- [Dashboard]({WEBSITE_LINK})
- [Support Server]({SUPPORT_SERVER_LINK})
- [Invite SquidGame Bot]({INVITE_BOT_LINK})
- [Vote SquidGame Bot]({WEBSITE_LINK}/vote)
- [Github](https://github.com/QuantumGamerLive/SquidGame)
            """,
            inline=True
        )
        embed.add_field(
            name="Owner Info",
            value="""
Made by: **[Kirito Guy#9521](https://discord.com/users/753247226880589982)**
            """,
            inline=True
        )
        try:
            embed.add_field(
                name="Latest Commits:",
                value=get_commits(),
                inline=False
            )
        except Exception:
            pass
        await msg.edit(embed=embed)

    @commands.command(name="credits", help="Credits to our contributors and helpers!")
    @slash_command(name="credits", help="Credits to our contributors and helpers!")
    async def credits(self, ctx: Union[commands.Context, InteractionContext]):
        embed = discord.Embed(
            title="Squid Game Bot Credits",
            description="""
**Owner:** [`Kirito Guy#9521`](https://discord.com/users/753247226880589982)
**took help from:** Nirlep_5252_#9798 and Blue.#1270
**Contributor(s):** Currently no one :(

**Github:** https://github.com/QuantumGamerLive/SquidGame
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
