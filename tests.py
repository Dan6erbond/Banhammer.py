import praw

import banhammer


class CustomPayload(banhammer.ReactionPayload):
    def get_message(self):
        return "I handled the submission '{0.title}' from /r/{0.subreddit}.".format(self.item.item)


class CustomHandler(banhammer.ReactionHandler):
    def handle(self, reaction, item, payload):
        payload.actions.append("test action")
        return payload


class CustomBuilder(banhammer.MessageBuilder):
    def get_item_message(self, item):
        return "Item title: {}".format(item.item.title)


def run():
    reddit = praw.Reddit("TBHB")

    bh = banhammer.Banhammer(reddit, message_builder=CustomBuilder(), reaction_handler=CustomHandler())
    bh.add_subreddits(banhammer.Subreddit(bh, subreddit="banhammerdemo"))
    bh.run()

    url = "https://www.reddit.com/r/banhammerdemo/comments/c66rdl"
    item = bh.get_item(url)

    print(item)
    # print(json.dumps(item.get_embed().to_dict(), indent=4))
    print(item.is_removed())
    print(item.is_author_removed())

    payload = item.get_reaction("✔").handle()
    print(payload)
    payload = item.get_reaction("✔").handle(CustomPayload("Ravi"))
    print(payload)


run()
