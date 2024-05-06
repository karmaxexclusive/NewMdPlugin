import asyncio
import random
from collections import deque
import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.types import *
from pyrogram.types import Message

from Pbxbot.bad.bad import edit_or_reply, get_text
from Pbxbot.bad.constants import MEMES
from . import *

DEFAULTUSER = "Man"

@on_message("plain", allow_stan=True)
async def hello_world(client: Client, message: Message):
    mg = await edit_or_reply(message, "Wait for plane...")
    await asyncio.sleep(0.2)
    await mg.edit("✈-------------")
    await asyncio.sleep(0.2)
    await mg.edit("-✈------------")
    await asyncio.sleep(0.2)
    await mg.edit("--✈-----------")
    await asyncio.sleep(0.2)
    await mg.edit("---✈----------")
    await asyncio.sleep(0.2)
    await mg.edit("----✈---------")
    await asyncio.sleep(0.2)
    await mg.edit("-----✈--------")
    await asyncio.sleep(0.2)
    await mg.edit("------✈-------")
    await asyncio.sleep(0.2)
    await mg.edit("-------✈------")
    await asyncio.sleep(0.2)
    await mg.edit("--------✈-----")
    await asyncio.sleep(0.2)
    await mg.edit("---------✈----")
    await asyncio.sleep(0.2)
    await mg.edit("----------✈---")
    await asyncio.sleep(0.2)
    await mg.edit("-----------✈--")
    await asyncio.sleep(0.2)
    await mg.edit("------------✈-")
    await asyncio.sleep(0.2)
    await mg.edit("------------✈")
    

@on_message("addsudo", allow_stan=True)
async def hajqag(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 3
    animation_ttl = range(0, 18)
    await message.edit("Deploying........")
    animation_chars = [
"**Heroku Connecting To Latest [Github Build](Badhacker98/PBX_2.0)**",
            f"**Build started by user** {DEFAULTUSER}",
            f"**Deploy** `535a74f0` **by user** **{DEFAULTUSER}**",
            "**Restarting Heroku Server...**",
            "**State changed from up to starting**",    
            "**Stopping all processes with SIGTERM**",
            "**Process exited with** `status 143`",
            "**Starting process with command** `python3 -m stdborg`",
            "**State changed from starting to up**",
            "__INFO:Pbxẞø†:Logged in as 557667062__",
            "__INFO:Pbxẞø†:Successfully loaded all plugins__",
            "**Build Succeeded**",
    ]
    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 18])
