#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import logging

from motor.motor_asyncio import AsyncIOMotorClient
from bot import Config

logger = logging.getLogger(__name__)


client = AsyncIOMotorClient(Config.DATABASE_URI)
db = client["MsgPurger"]
col = db["ConfigsData"]

async def get_configs():
    data = await ((col.find()).to_list(length=None))
    return data

async def get_config(key, default):
    data = await col.find_one({"_id": key})
    if data:
        return data["value"]
    else:
        await add_config(key, default)
        return default

async def add_config(key, value):
    await col.insert_one({"_id": key, "value": value})

async def update_config(data):
    await col.update_one({}, {"$set": data}, upsert=True)

async def delete_config(key):
    await col.delete_many({"_id": key})

async def delete_all_config():
    await col.delete_many({})

