import yt_dlp
import asyncio
import random

import requests
from pyrogram import *
from pyrogram import Client, filters
from . import *



async def play_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['formats'][0]['url']
        await group_call.input_stream(audio_url)

@on_message("play", allow_stan=True)
async def play(event):
    url = event.pattern_match.group(1)
    await play_youtube_audio(url)
    await event.respond('Playing YouTube audio...')
