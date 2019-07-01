import praw

from . import exceptions
from . import yaml
from . import item as reddititem


class ReactionPayload:
    def __init__(self):
        self.item = None
        self.user = "Banhammer"
        self.actions = list()
        self.approved = False
        self.reply = ""

    def __str__(self):
        return self.get_message()

    def feed(self, user, item, approved, reply=""):
        self.item = item
        self.approved = approved
        self.reply = reply

    def get_message(self):
        return "**{} {} by {}!**\n\n" \
               "{} by /u/{}:\n\n" \
               "{}".format(self.item.type.title(), " and ".join(self.actions), self.user,
                           self.item.type.title(), self.item.get_author_name(), self.item.get_url())


class Reaction:

    def __init__(self, reddit, dict={}, emoji="", type="", flair="", approve=False, mark_nsfw=False, lock=False,
                 reply="", distinguish_reply=True, sticky_reply=True, ban=None, archive=False, mute=False, min_votes=1):
        self.reddit = reddit

        self.emoji = dict["emoji"] if "emoji" in dict else emoji
        self.emoji = self.emoji.strip()

        self.type = dict["type"] if "type" in dict else type
        self.flair = dict["flair"] if "flair" in dict else flair
        self.approve = dict["approve"] if "approve" in dict else approve
        self.mark_nsfw = dict["mark_nsfw"] if "mark_nsfw" in dict else mark_nsfw
        self.lock = dict["lock"] if "lock" in dict else lock
        self.reply = dict["reply"] if "reply" in dict else reply

        self.distinguish_reply = dict["distinguish_reply"] if "distinguish_reply" in dict else distinguish_reply
        self.sticky_reply = dict["sticky_reply"] if "sticky_reply" in dict else sticky_reply
        if self.sticky_reply: self.distinguish_reply = True

        self.ban = dict["ban"] if "ban" in dict else ban
        self.archive = dict["archive"] if "archive" in dict else archive
        self.mute = dict["mute"] if "mute" in dict else mute
        self.min_votes = dict["min_votes"] if "min_votes" in dict else min_votes

        self.item = None

    def __str__(self):
        str = self.emoji

        if self.type in ["submission", "comment", ""]:
            if self.type != "":
                str += " | " + self.type
            else:
                str += " | submissions + comments"
            if self.flair != "": str += " | flair: " + self.flair
            str += " | " + ("approve" if self.approve else "remove")
            if self.mark_nsfw: str += " | mark NSFW"
            if self.lock or not self.approve: str += " | lock"
            if self.ban is not None:
                str += " | " + ("permanent ban" if self.ban == 0 else "{} day ban".format(self.ban))
        if self.reply != "": str += " | reply"
        if self.min_votes: str += " | min votes: {}".format(self.min_votes)

        return str

    def get_dict(self):
        dict = {
            "emoji": self.emoji,
            "type": self.type,
            "flair": self.flair,
            "approve": self.approve,
            "mark_nsfw": self.mark_nsfw,
            "lock": self.lock,
            "reply": self.reply,
            "ban": self.ban,
            "archive": self.archive,
            "mute": self.mute,
            "min_votes": self.min_votes
        }

        return dict

    def handle(self, user, payload=ReactionPayload(), item=None):
        if item is None and self.item is not None:
            item = self.item

        if type(item) != reddititem.RedditItem or item is None:
            raise exceptions.NoItemGiven()

        if not self.eligible(item.item):
            raise exceptions.NotEligibleItem()

        payload.feed(user, item, self.approve, self.reply)

        if isinstance(item.item, praw.models.ModmailMessage):
            if self.archive:
                item.item.conversation.archive()
                payload.actions.append("archived")
            if self.mute:
                item.item.conversation.mute()
                payload.actions.append("muted")
            if self.reply != "":
                item.item.conversation.reply(self.reply)
                payload.actions.append("replied to")
            return payload

        # is_submission = isinstance(item.item, praw.models.Submission)
        # is_comment = isinstance(item.item, praw.models.Comment)

        if item.is_removed() or item.is_author_removed():
            item.item.mod.remove()
            payload.actions.append("removed")
            item.item.mod.lock()
            payload.actions.append("locked")

            payload.feed("Banhammer", item, False)
            return payload

        if self.approve:
            item.item.mod.approve()
            payload.actions.append("approved")
        else:
            item.item.mod.remove()
            payload.actions.append("removed")

        if self.lock or not self.approve:
            item.item.mod.lock()
            payload.actions.append("locked")
        else:
            item.item.mod.unlock()

        if is_submission:
            if self.flair != "":
                item.item.mod.flair(text=self.flair)
                payload.actions.append("flaired")

            if self.mark_nsfw:
                item.item.mod.nsfw()
                payload.actions.append("marked NSFW")

        if self.reply != "":
            reply = item.item.reply(self.reply)
            if self.distinguish_reply: reply.mod.distinguish(sticky=self.sticky_reply)
            payload.actions.append("replied to")

        if isinstance(self.ban, int):
            if self.ban == 0:
                item.item.subreddit.banned.add(item.item.author.name, ban_reason="Breaking Rules",
                                               ban_message=formatter.format_ban_message(item.item, self.ban),
                                               note="Bot Ban")
                payload.actions.append("/u/" + item.item.author.name + " permanently banned")
            else:
                item.item.subreddit.banned.add(item.item.author.name, ban_reason="Breaking Rules", duration=self.ban,
                                               ban_message=formatter.format_ban_message(item.item, self.ban),
                                               note="Bot Ban")
                payload.actions.append("/u/{} banned for {} day(s)".format(item.item.author.name, self.ban))

        item.remove("files/{}_reports.txt".format(item.subreddit.subreddit.id))
        item.remove("files/{}_queue.txt".format(item.subreddit.subreddit.id))

        return payload

    def eligible(self, item):
        if isinstance(item, praw.models.Submission):
            if self.type == "" or self.type == "submission":
                return True
        elif isinstance(item, praw.models.Comment):
            if self.type == "" or self.type == "comment":
                return True
        elif isinstance(item, praw.models.ModmailMessage):
            if self.type == "mail":
                return True
        return False


def get_reactions(reddit, yml):
    result = yaml.get_list(yml)
    ignore = list()
    emojis = set()
    for item in result:
        if "ignore" in item:
            ignore = [i.strip() for i in item["ignore"].split(",")]
            result.remove(item)
            break
    reactions = result
    reactions = [Reaction(reddit, r) for r in result if "emoji" in r]
    return {
        "ignore": ignore,
        "reactions": reactions
    }


def ignore_reactions(reactions, remove):
    emojis = set()

    for item in remove:
        if isinstance(item, Reaction):
            emojis.add(item.emoji)
        elif isinstance(item, str):
            emojis.add(item)

    for react in reactions:
        if react.emoji in emojis:
            reactions.remove(react)

    return reactions
