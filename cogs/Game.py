import discord
from handler import InteractionContext
from typing import Union
from utils.bot import SquidGame
from discord.ext import commands
import asyncio
import random


class Game(commands.Cog, name="play the game of death"):
    def __init__(self, bot: SquidGame):
        self.bot = bot

    @commands.command(name="Start Game", help="Start a new Game")
    @slash_command(name="Start Game", help="Start a New Game")
    async def start_game(self, ctx: Union[commands.Context, InteractionContext]):
        msg = await ctx.reply(embed=discord.Embed(title="Starting A New Game", description="Welcome To Squid Game. Creating a New Game...", color=discord.Color.red())).set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeXK3jXSdWsAMjTGuczb7dUhAsMnnnmXYnLw&usqp=CAU")
        await asyncio.sleep(5)
        await msg.edit(embed = discord.Embed(title="Room Created", description="The Room for Squid Game has been Created! Now, Click on `✋` to Join The Room")
        await msg.add_reaction(✋)
        new_msg = await channel.fetch_message(msg.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        for _ in range(10):
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda r, u: str(u.emoji) == '✋', timeout=120)
                users.append(user)
            except asyncio.TimeoutError:
                return await ctx.send("no one reacted in time")

def setup(bot: SquidGame):
    bot.add_cog(Game(bot))
