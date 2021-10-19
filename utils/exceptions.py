import discord
from typing import Optional, Union
from discord.ext.commands import CommandError


class DMsDisabled(CommandError):
    def __init__(self, user: discord.Member):
        self.user = user


class NotStaff(CommandError):
    pass


class NotAdmin(CommandError):
    pass


class NoBots(CommandError):
    pass


class GuildOnlyPls(CommandError):
    pass
