import json

import praw

from banhammer import banhammer
from banhammer import reaction
from banhammer import subreddit


class CustomPayload(reaction.ReactionPayload):
    def get_message(self):
        return "I handled the submission '{}' from /r/{}.".format(self.item.item.name, self.item.item.subreddit)


def run():
    reddit = praw.Reddit("TBHB")

    bh = banhammer.Banhammer(reddit)
    bh.add_subreddits(subreddit.Subreddit(bh, subreddit="banhammerdemo"))

    url = "https://www.reddit.com/r/banhammerdemo/comments/c66rdl"
    item = bh.get_item(url)

    print(item)
    print(json.dumps(item.get_embed().to_dict(), indent=4))
    print(item.is_removed())
    print(item.is_author_removed())

    payload = item.get_reaction("✔").handle("Ravi", CustomPayload())
    print(payload)


run()
