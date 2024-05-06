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
async def gahah(client: Client, message: Message):
    if message.forward_from:
        return
    animation_interval = 0.7
    animation_ttl = range(0, 12)
    await message.edit("ready to die dude.....")
    animation_chars = [
    "-✈------------",
"--✈-----------",
"---✈----------",
"----✈---------",
"-----✈--------",
"------✈-------",
"-------✈------",
"--------✈-----",
"---------✈----",
"----------✈---",
"-----------✈--",
"------------✈-",
"-------------✈",
]

    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await message.edit(animation_chars[i % 12])
