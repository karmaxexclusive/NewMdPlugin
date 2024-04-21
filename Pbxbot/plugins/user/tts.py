from pyrogram import Client, filters
from gtts import gTTS
import os
import random
import time
from . import *

@on_message("ttts", allow_stan=True)
def text_to_speech(client, message):
    text = message.text.split(' ', 1)[2]
    tts = gTTS(text=text, lang='hi')
    tts.save('ᴬᵁᴰᴵᴼ.mp3')
    client.send_audio(message.chat.id, 'ᴬᵁᴰᴵᴼ.mp3')
