import discord
import motor.motor_asyncio as motor
from utils.exceptions import NotSetup, UserAlreadyInAModmailThread
from typing import Optional, List


class Database:
    def __init__(self, url: str):
        self.cluster = motor.AsyncIOMotorClient(url)
        self.db = self.cluster['brah']
        self.guild_data = self.db['guild_data']
        self.blacklist_data = self.db['blacklists']
        self.blacklist_cache = []

    async def get_guild_data(self, guild_id: int, raise_error: bool = True) -> Optional[dict]:
        data = await self.guild_data.find_one({"_id": guild_id})
        if data is None and raise_error:
            raise NotSetup()
        return data

    async def set_guild_data(self, guild_id: int, **kwargs):
        return await self.guild_data.update_one(
            filter={"_id": guild_id},
            update={"$set": kwargs},
            upsert=True
        )

    async def blacklist(self, user_id: int, reason: str):
        return await self.blacklist_data.update_one(
            filter={"_id": user_id},
            update={"$set": {"reason": reason}},
            upsert=True
        )

    async def unblacklist(self, user_id: int):
        return await self.blacklist_data.delete_one({"_id": user_id})

    async def get_blacklist_cache(self):
        cursor = self.blacklist_data.find({})
        list_of_docs = await cursor.to_list(length=None)
        self.blacklist_cache = [e['_id'] for e in list_of_docs]
