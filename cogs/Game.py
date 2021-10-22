import discord
from handler import InteractionContext, slash_command
from typing import Union
from utils.bot import SquidGame
from discord.ext import commands
import asyncio
import random


class Game(commands.Cog, name="Game"):
    def __init__(self, bot: SquidGame):
        self.bot = bot
        self.react_emoji = "✋"

    @commands.command(aliases=["start_game"], help="Start a new Game")
    @slash_command(name="startgame", help="Start a New Game")
    async def startgame(self, ctx: Union[commands.Context, InteractionContext]):
        msg = await ctx.send(embed=discord.Embed(title="Starting A New Game", description="Welcome To Squid Game. Creating a New Game...", color=discord.Color.red()).set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeXK3jXSdWsAMjTGuczb7dUhAsMnnnmXYnLw&usqp=CAU"))
        await asyncio.sleep(5)
        sus = await msg.edit(embed = discord.Embed(title="Room Created", description=f"The Room for Squid Game has been Created! Now, Click on `{self.react_emoji}` to Join The Room."))
        await sus.add_reaction(self.react_emoji)
        new_msg = await ctx.channel.fetch_message(sus.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        for _ in range(1):
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check = lambda r, u: str(r.emoji) == '✋', timeout=120)
                users.append(user)
            except asyncio.TimeoutError:
                return await ctx.send("no one reacted in time")
        overwrites = {user: discord.PermissionOverwrite(read_messages=True, send_messages=True) for user in users}
        overwrites[ctx.guild.default_role] = discord.PermissionOverwrite(read_messages=False, send_messages=False)
        chnl = await ctx.guild.create_text_channel(f"Squid-Game", overwrites=overwrites)
        await ctx.send(f"**10/10** has joined. Room has been created! Move to <#{chnl.id}>.")
        introduction_embed = discord.Embed(description="Welcome to Squid Game.", color=0xff2f00)
        introduction_embed.set_author(name="Squid Game")
        introduction_embed.add_field(name="Info:", value="1) this is the game of death. The one who lose he/she will die and the won who wins gets all the prize money.", inline=False)
        introduction_embed.add_field(name="-", value="2) if any cheating was seen then the player get instantaneous elimination.", inline=True)
        introduction_embed.add_field(name="-", value="any player who don't want to play can click on "🔚" to exit the game. ", inline=True)
        introduction_embed.add_field(name="-", value="The winner get **1000 coins** as a prize money", inline=True)
        introduction_embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGzJjuDzamSLOP9KVcBSfLf-gQ0dHm8iGdgg&usqp=CAU")
        await ctx.chnl.send(embed=introduction_embed)



def setup(bot: SquidGame):
    bot.add_cog(Game(bot))
