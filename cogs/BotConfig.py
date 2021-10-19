import discord
from discord.ext import commands
from typing import Union, Optional, Dict
from handler import slash_command, user_command, InteractionContext
from handler import SlashCommandOption as Option
from handler import SlashCommandChoice as Choice
from utils.bot import SquidGame


dropdown_concurrency = []


class BotConfig(commands.Cog, name="Bot Configuration"):
    def __init__(self, bot: SquidGame):
        self.bot = bot


    @commands.Cog.listener('on_message')
    async def prefix_reply(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.lower() not in [f"<@{self.bot.user.id}>", f"<@!{self.bot.user.id}>"]:
            return
        prefixes = self.bot.config.prefixes.copy()
        if not message.guild:
            return await message.reply(f"My prefixes are: {', '.join(['`' + p + '`' for p in prefixes])}")
        data = await self.bot.mongo.get_guild_data(message.guild.id, raise_error=False)
        data = data or {}
        guild_prefixes = data.get('prefixes', [])
        if not guild_prefixes:
            return await message.reply(f"My prefixes are: {', '.join(['`' + p + '`' for p in prefixes])}")
        await message.reply(f"My prefixes are: {', '.join(['`' + p + '`' for p in guild_prefixes])}")

    @commands.group(name="prefix", help="Manage the prefixes for the bot.")
    async def prefix(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            g = await self.bot.mongo.get_guild_data(ctx.guild.id, raise_error=False)
            if g is None:
                g = {}
            prefixes = g.get("prefixes", self.bot.config.prefixes.copy())
            return await ctx.reply(f"Your current prefixes are: {', '.join(['`' + prefix + '`' for prefix in prefixes])}\nYou can use the following commands to manage them:\n\n- `{ctx.clean_prefix}prefix add <prefix>`\n- `{ctx.clean_prefix}prefix remove <prefix>`")

    @prefix.command(name="add", help="Add a prefix to the bot.")
    @commands.has_permissions(manage_guild=True)
    async def prefix_add(self, ctx: commands.Context, *, prefix: str = None):
        if prefix is None:
            return await ctx.reply(f"{self.bot.config.emojis.no} Please specify a prefix to add.")
        g = await self.bot.mongo.get_guild_data(ctx.guild.id, raise_error=False)
        if g is None:
            g = {}
        prefixes = g.get("prefixes", self.bot.config.prefixes.copy())
        if len(prefixes) >= 5:
            return await ctx.reply(f"{self.bot.config.emojis.no} You can only have 5 prefixes.")
        if prefix in prefixes:
            return await ctx.reply(f"{self.bot.config.emojis.no} This prefix is already added.")
        prefixes.append(prefix)
        await self.bot.mongo.set_guild_data(ctx.guild.id, prefixes=prefixes)
        await ctx.reply(f"{self.bot.config.emojis.yes} Added `{prefix}` to your prefixes.")

    @prefix.command(name="remove", help="Remove a prefix from the bot.")
    @commands.has_permissions(manage_guild=True)
    async def prefix_remove(self, ctx: commands.Context, *, prefix: str = None):
        if prefix is None:
            return await ctx.reply(f"{self.bot.config.emojis.no} Please specify a prefix to remove.")
        g = await self.bot.mongo.get_guild_data(ctx.guild.id, raise_error=False)
        if g is None:
            g = {}
        prefixes = g.get("prefixes", self.bot.config.prefixes.copy())
        if prefix not in prefixes:
            return await ctx.reply(f"{self.bot.config.emojis.no} This prefix is not added.")
        if len(prefixes) == 1:
            return await ctx.reply(f"{self.bot.config.emojis.no} You cannot remove the last prefix.\nPlease add another one and then remove this one.")
        prefixes.remove(prefix)
        await self.bot.mongo.set_guild_data(ctx.guild.id, prefixes=prefixes)
        await ctx.reply(f"{self.bot.config.emojis.yes} Removed `{prefix}` from your prefixes list.")


def setup(bot: SquidGame):
    bot.add_cog(BotConfig(bot))
