# discord-radio-bot
Basic music-stream-playing Discord bot in python.

## Discord Radio Bot Basics

### What is this for? 

I made `discord-radio-bot` to play Internet Radio Streams in a Discord Voice Channel.

Using the "play" command with this Bot will summon it into the channel where you are currently connected and immediately start playing from the SOURCE it knows about.

You can have multiple bots playing different streams in different channels. Note that you will need to register each bot as a separate, novel Application through your Discord account.  See https://discordpy.readthedocs.io/en/latest/discord.html

You could probably also use `discord-radio-bot` to play static files if you wanted, but it would just play them once and then drop off until you told it to play again. It would be pretty trivial to give this bot a "loop" command.


### What tricks does it know?

Oh, very few.  It knows how to:

  * play -- play the SOURCE stream or file it was loaded with.
  * whoami -- tell you in chat what your username is (so useful!).
  * source -- tell you in chat the URL of its source audio.


### What Do I Need to Set up a Discord Radio Bot?

1. a Discord account.
2. a Discord server that allows you to invite and control Bots.
3. a computer connected to the internet (let's call it a "server") where you can run this python script.
4. this "server" will need to have `ffmpeg` installed (see below) and Python 3.6 at minimum.


## Bot Setup

First, there are some hurdles you'll have to jump through to get a Discord Bot TOKEN, so I'm going to send you to the Discord Python library page for how to do that: https://discordpy.readthedocs.io/en/latest/discord.html

Good luck.  Come back here when you've:

1. Created a novel Application.
2. Copied its Client ID.
3. Made it into a Bot
4. Invited your Bot into your server.

### Step 1: Make a Python virtualenv.

Clone this repo, then `cd discord-radio-bot`.  In this directory, use the Python virtualenv maker of your choice, e.g. `pipenv`, then activate it.  Then `pip -r requirements.txt` to install what you need.

### Step 2: Set environment variables.

Before running your bot, you'll need to set three env variables:

* `DISCORD_RADIOBOT_TOKEN` -- the Discord TOKEN you generated when you completed the "Build a Bot" step.
* `DISCORD_RADIOBOT_PREFIX` -- the prefix for commands so that the bot knows you're addressing it.
* `DISCORD_RADIOBOT_SOURCE` -- the streaming radio station or static file's URL. Must be mp3 or ogg.

### Step 3: Run the bot.

Now simply type `python radiobot.py` and see what happens.

Chances are pretty high you'll need to install `ffmpeg` first.  On OS X you can do `brew install ffmpeg` (assuming you're using Brew).  On Linux, do `sudo apt install ffmpeg`.

After installing FFMpeg try running the bot again. 

### Step 4: Get on Discord and Invite Your Bot into a Voice Channel.

You should now see your Bot listed on your Discord server as a logged-in user.  You can send it commands from any public text channel (or channel you have given it permissions to read).  If you selected a prefix of "!", try doing `!whoami`.  If it doesn't respond, try a different channel.

If your bot seems responsive, put yourself into a Voice Channel.  Now type into any text channel the bot can read, `!play` (again assuming you set `DISCORD_RADIOBOT_PREFIX` to "!"). The bot should now be playing!

If you can't hear anything, look at the server where the bot is running and check the messages.  Can it read the SOURCE file?  Does it look like it didn't actually hear the "play" command?  Look for error messages.


## Known Weaknesses

This bot has NO KNOWN WEAKNESSES!!!!1one


## Improvements That Could Be Made

This bot needs:

* a more user-friendly way to turn it into a standalone daemon
* a "loop" command
* more robust error-handling
* some control over the quality of re-encoding
* the ability to configure at run-time whether it uses the MP3 or OPUS encoder (currently just uses the latter since it's way more efficient... this bot is a gas-guzzler...)
* a "stop" command
* a "chicken" command


## Contact

This bot was made hastily for an online nonsense party where it played 3 different "rooms" from 3 different radio streams.  It worked pretty decently well, all told.  Feel free to fork and improve.  I will probably accept pull requests without testing them, so make them good.  --Naomi Most, 2021







