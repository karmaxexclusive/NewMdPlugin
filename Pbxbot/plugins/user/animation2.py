import asyncio
import random

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
