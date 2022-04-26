import os
import requests

from discord import FFmpegOpusAudio, FFmpegPCMAudio
from discord.ext.commands import Bot
from discord.ext.commands.errors import CommandInvokeError
from discord.errors import ClientException
from discord.ext.commands.errors import MissingRequiredArgument

from collections import deque

import logging


log = logging.getLogger()
logging.basicConfig(level=logging.INFO, filename="../log/radiobot_mobradio_mark.log")

TOKEN = os.getenv("DISCORD_RADIBOT_TOKEN", "")            # collected from Discord Bot setup process.
PREFIX = os.getenv("DISCORD_ANYPLAYER_PREFIX", "!")       # recommended: "!"

# Note: mp3 costs more in CPU cycles and doesn't sound any better than ogg.
ENCODING = "ogg"                                     # options: ogg, mp3  (default: ogg)
BITRATE = "160k"                                     # examples: 128k, 160k, 320k


# TODO: These should be overridden by the user; here are defaults that will work.
SERVER = "icecast.rocks"
PROTOCOL = "http"
PORT = 8000


### GLOBALS (do not edit) ###
client = Bot(command_prefix=list(PREFIX))
player = None
LISTENURL = ""
### end GLOBALS


def get_icecast_status():
    res = requests.get(f"{PROTOCOL}://{SERVER}:{PORT}/status-json.xsl")
    return res.json()


def get_listenurl(mountpoint):
    return f"{PROTOCOL}://{SERVER}:{PORT}/{mountpoint}"


def get_now_playing():
    status = get_icecast_status()

    # loop through until we find the matching mountpoint
    for source in status["icestats"].get("source", None):
        if source["listenurl"] == LISTENURL:
            out = "Now playing on %s:\n\n" % source["server_name"]
            out += "%s" % source["title"]
            return out

    return "Nothing currently playing."


@client.event
async def on_ready():
    log.info("MobileCoin Radio Ready")


async def do_stop(ctx):
    player.stop()
    await ctx.send(f"OK, stopping.")
    return


@client.event
async def on_command_error(ctx, error):
    log.error("User generated error: %r" % error)
    await ctx.send("Whoops!   %s" % error)

async def do_play(ctx, src):
    global player
    try:
        channel = ctx.message.author.voice.channel
    except AttributeError:
        # user is not in a Voice Channel
        await ctx.send(f"You need to join a Voice Channel first!")
        return

    try:
        player = await channel.connect()
    except CommandInvokeError:
        log.info("Attempt to play without user in channel")
    except Exception as err:
        log.error(err)
        pass
    if player:
        if ENCODING == "mp3":
            player.play(FFmpegPCMAudio(src, options="-b:a %s" % BITRATE))
        else:
            player.play(FFmpegOpusAudio(src, options="-b:a %s" % BITRATE))
    else:
        log.error("Could not initialize player.")


@client.command(aliases=['l', 'ls'])
async def list(ctx):
    "List available stations on the server."
    status = get_icecast_status()
    out = f"Available stations:\n"

    for source in status["icestats"].get("source", []):
        if source["listenurl"].endswith(".ogg"):
            out += "\n"
            out += source["listenurl"].split("/")[3].split(".ogg")[0]
            out += "\t\t\t"
            out += source["server_name"]

    out += "\n"
    await ctx.send(out)


@client.command(aliases=['p', 'pl'])
async def play(ctx, mountpoint):
    "Play a liquidsoap station (use !list to see station names)."
    global LISTENURL
    LISTENURL = get_listenurl(mountpoint)

    try:
        log.info(f"Playing {LISTENURL} per user command")
        await do_play(ctx, LISTENURL)
    except ClientException:
        #already playing
        log.info("Stopping current stream first.")
        do_stop(ctx)
        await do_play(ctx, LISTENURL)
    except Exception as err:
        print(err)
        log.error(err)
        await ctx.send("%r" % err)


@client.command(aliases=['s'])
async def stop(ctx):
    "Stop playing."
    log.info(f"Stopping {LISTENURL} per user command")
    do_stop(ctx)
    # to make bot leave the channel entirely:
    # await ctx.voice_client.disconnect()


@client.command(aliases=['np'])
async def wtf(ctx):
    "Find out what's currently playing (alias: !np)."
    await ctx.send(get_now_playing())


# Remove bot from channel if it's sitting unused.
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    # Checking if the bot is connected to a channel and if there is only 1 member connected to it (the bot itself)
    if voice_state is not None and len(voice_state.channel.members) == 1:
        # You should also check if the song is still playing
        await voice_state.disconnect()


if TOKEN:
    client.run(TOKEN)
else:
    print("Discord bot token not set; cannot run.")
    print()
    print("Please set DISCORD_RADIOBOT_TOKEN environment variable (or edit this script.)"

