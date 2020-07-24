# Banhammer.py

[![PyPi version](https://img.shields.io/pypi/v/Banhammer.py?style=flat-square)](https://pypi.org/project/Banhammer.py/)
![PyPi License](https://img.shields.io/pypi/l/Banhammer.py?style=flat-square)
![PyPi Python Versions](https://img.shields.io/pypi/pyversions/banhammer.py?style=flat-square)
[![Banhammer Discord](https://img.shields.io/discord/721693929195569172?color=7289da&label=Discord&logo=discord&style=flat-square)](https://discord.gg/9JrGC8f)
![GitHub Issues](https://img.shields.io/github/issues/Dan6erbond/Banhammer.py?style=flat-square)
![GitHub Stars](https://img.shields.io/github/stars/Dan6erbond/Banhammer.py?style=flat-square)
![GitHub Contributors](https://img.shields.io/github/contributors/Dan6erbond/Banhammer.py?style=flat-square)
[![Subreddit Subscribers](https://img.shields.io/reddit/subreddit-subscribers/BanhammerBot?style=flat-square)](https://reddit.com/r/BanhammerBot)

**Banhammer.py** is a framework that allows you to build your very own Banhammer! *Banhammer* pursues the goal of bringing subreddit moderation to your very own Discord server, by streaming any and all moderatable items to Discord channels and allowing users to then moderate the subreddit through a joint bot account using **Reactions**, there's no need to use Reddit's moderation interface anymore!

**Table of Contents**

 - [Features](#features)
 - [Installation](#installation)
 - [Quick Example](#quick-example)
 - [Contributing](#contributing)
 - [Roadmap](#roadmap)
 - [Links](#links)
 - [License](#license)

## Features
 - Streaming new and reported posts to your Discord bot.
 - Adding and handling reactions.
 - Fetching reactions from subreddit wiki.
 - Changing bot presence on Discord.
 - Generating embeds and messages for items and actions.

## Installation

Banhammer.py requires a release of Python 3.6 or newer. You can install Banhammer.py via pip:

```pip install banhammer.py```

## Quick Example
Once the dependencies have been installed, the bot can be created. For that the general structure of a Discord `Client` or `Bot` (if commands are of importance use `Bot`) needs to be created and then Banhammer initialized as well as ran.

```python
import apraw
import discord
import banhammer
from banhammer.models import Subreddit
from discord.ext import commands

bot = commands.Bot(command_prefix='>')
reddit = apraw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                     password=PASSWORD, username=USERNAME, user_agent=USER_AGENT)
bh = banhammer.Banhammer(reddit, bot=bot)

@bot.event
async def on_command_error(ctx, error):
    print(error)

@bot.event
async def on_ready():
    print(str(bot.user) + ' is running.')
    sub = Subreddit(bh, SUBNAME)
    await sub.load_reactions()
    await bh.add_subreddits(sub)
    bh.run()

@bh.new()
async def handle_new(p):
    msg = await bot.get_channel(CHANNEL_ID).send(embed=await p.get_embed())
    await p.add_reactions(m)

bot.run(TOKEN)
```

`bh.run()` must be called so that Banhammer can start the internal event loop. More examples can be found in the (examples)[examples] folder or in the [Banhacker](https://github.com/Dan6erbond/Banhacker) as well as the [D6B](https://github.com/Dan6erbond/D6B) GitHub repositories that both show different (and more complex) implementations of the framework.

## Contributing

Banhammer.py is open-source! That means we'd love to see your contributions and hopefully be able to accept them in the next release. If you want to become a contributor, try to follow these rules to keep the code clean:

 - Follow Python naming conventions. (eg. `variable_name` and `ClassName`)
 - Only use `async` where necessary.
 - Use the OOP approach; create classes when it makes sense.
 - Document as much as you can, preferably with inline comments.
 - Use the NumPyDoc docstring format.
 - Store data in JSON, INI or YAML format to eliminate dependencies for other formats.

## Roadmap

 - [x] Returning actions performed.
 - [x] Improved support for modmail.
 - [x] `MessageBuilder` object to create custom messages/embeds.
 - [ ] `save()` function for `Subreddit` object.
 - [x] Support for newer PRAW features (such as locking comments).
 - [ ] Validation of inputs.
 - [x] Better exception handling and outputs.
 - [ ] Support for variable function arguments.

## Links

 - [Official Discord server](https://discordapp.com/invite/9JrGC8f)
 - [PyPi Release](https://pypi.org/project/Banhammer.py/)
 - [Discord.py](https://discordpy.readthedocs.io/en/latest)
 - [aPRAW](https://apraw.readthedocs.io/en/latest)

## License

Banhammer.py's source is provided under GPLv3.
> Copyright ©, RaviAnand Mohabir
