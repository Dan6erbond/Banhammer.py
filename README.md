# Banhammer.py
By [Mariavi](https://dan6erbond.github.io/mariavi)

**Banhammer.py** is a framework that allows you to build your very own Banhammer! *Banhammer* is the concept that got Mariavi started and pursues the goal of bringing subreddit moderation to your very own Discord server. By streaming any and all moderatable items to Discord channels and allowing users to then moderate the subreddit through a joint bot account using **Reactions**, there's no need to use Reddit's moderation interface anymore!

## Features
 - Streaming new posts to Discord.
 - Adding and handling reactions.
 - Grabbing reactions from subreddit wiki.
 - Changing bot's presence on Discord.
 - Generating embeds and messages for items and actions.

## Usage
### Installation
Currently the PyPi release of Banhammer.py has not been tested which is why we recommend just cloning the repository to your local machine after which you can `cd` into the directory with the files to install the requirements which are notated in the [requirements.txt](requirements.txt) file:
 - `pip install -r requirements.txt`
 
### Quick Example
Now that the dependancies have been installed, it's time to create your bot! For that you'll need the general structure of a Discord `Client` or `Bot` (if you want to make use of the commands extension) and then add the bits for Banhammer.py to know what to do.

```python
import discord
from discord.ext import commands

from banhammer import banhammer
from banhammer import subreddit

bot = commands.Bot(command_prefix='>')
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                     password=PASSWORD, username=USERNAME, user_agent=USER_AGENT)
bh = banhammer.Banhammer(reddit, bot=bot)

@bot.event
async def on_command_error(ctx, error):
    print(error)
    
@bot.event
async def on_ready():
    print(str(bot.user) + ' is running.')
    bh.run()
    
@bh.new()
async def handle_new(p):
    msg = await bot.get_channel(CHANNEL_ID).send(embed=p.get_embed())
    await p.add_reactions(m)

bot.run(TOKEN)
```

Make sure you don't forget to call `bh.run()` so that Banhammer can start the internal event loop. For more examples check out [Banhacker](https://github.com/Dan6erbond/Banhacker) as well as the [D6B](https://github.com/Dan6erbond/D6B) bot that both show different (and more complex) implementations of the framework.

## Contributing
🚧👷‍♂️Work in progress!

## Roadmap
 - [x] Returning actions performed.
 - [ ] Better support for modmail.
 - [ ] `MessageBuilder` object to create custom messages/embeds.
 - [ ] `save()` function for `Subreddit` object.
 - [ ] Support for newer PRAW features (such as locking comments).
 - [ ] Validation of inputs.
 - [ ] Better exception handling and outputs.

## Links
 - [Documentation](https://dan6erbond.github.io/mariavi/banhammer.py.html)
 - [Official Discord server](https://discordapp.com/invite/9JrGC8f)
 - [PyPi Release](https://pypi.org/project/banhammer.py/)
 - [Discord.py](https://discordpy.readthedocs.io/en/latest)
 - [PRAW](https://praw.readthedocs.io/en/latest)
 - [Mariavi](https://dan6erbond.github.io/mariavi)
 
### Contributors
The awesome people that worked on this framework and its idea to make it a reality!
 - [Dan6erbond](https://dan6erbond.github.io) (Dan6erbond#2259)
 - [lydocia](https://www.lydocia.com) (lydocia#2301)

### Users
Some bots that makes use of this framework.
 - [Banhammer](https://dan6erbond.github.io/mariavi/banhammer.html)
 - [Banhacker](https://github.com/Dan6erbond/Banhacker)
 - [D6B](https://github.com/Dan6erbond/D6B)
