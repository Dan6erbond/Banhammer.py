import discord
from discord.ext import commands

from banhammer import banhammer
from banhammer import subreddit

bot = commands.Bot(command_prefix='>')
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                     password=PASSWORD, username=USERNAME, user_agent=USER_AGENT)
bh = banhammer.Banhammer(reddit, bot=bot)
bh.add_subreddits(subreddit.Subreddit(bh, SUBNAME))


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