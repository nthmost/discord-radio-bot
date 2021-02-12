import os

from discord import FFmpegOpusAudio, FFmpegPCMAudio
from discord.ext.commands import Bot
from discord.ext.commands.errors import CommandInvokeError


# A spot to keep these details handy while you're collecting them...
# 
# client id: 
# public key: 
# client secret: 
# bot permissions: 66583360
# TOKEN:
 


TOKEN = os.getenv("DISCORD_RADIOBOT_TOKEN")         # collected from Discord Bot setup process.
PREFIX = os.getenv("DISCORD_RADIOBOT_PREFIX")       # e.g. "!"
SOURCE = os.getenv("DISCORD_RADIOBOT_SOURCE")       # e.g. "http://nthmost.net:8000/mutiny-studio"
ENCODING = "ogg"                                    # options: ogg, mp3  (default: ogg)

client = Bot(command_prefix=list(PREFIX))

player = None


@client.event
async def on_ready():
    print('KSTK Player Ready')


@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")


@client.command(name="web_listeners")
async def web_listeners(ctx):
    listeners = 5
    await ctx.send(f"Listeners connected directly to {SOURCE}: {listeners}")


@client.command(aliases=['p', 'pla'])
async def play(ctx):
    global player
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        # user is not in a Voice Channel
        await ctx.send(f"You need to join a Voice Channel for me to know where to play the stream!")
        return

    try:
        player = await channel.connect()
    except CommandInvokeError:
        print("Attempt to play without user in channel")
    except Exception as err:
        print(err)
        pass
    if player:
        if ENCODING == "mp3":
            player.play(FFmpegPCMAudio(SOURCE))
        else:
            player.play(FFmpegOpusAudio(SOURCE))
    else:
        print("Could not initialize player.")


@client.command(aliases=['s', 'sto'])
async def stop(ctx):
    player.stop()


client.run(TOKEN)

