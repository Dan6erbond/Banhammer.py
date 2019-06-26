import json
import praw
from .yaml import *
from .reaction import *

class Subreddit:

    def __init__(self, reddit, dict={}, subreddit="", stream_new=True, stream_comments=False, stream_reports=True, stream_mail=True, stream_queue=True):
        self.reddit = reddit
        self.subreddit = dict["subreddit"] if "subreddit" in dict else subreddit
        self.stream_new = dict["stream_new"] if "stream_new" in dict else stream_new
        self.stream_comments = dict["stream_comments"] if "stream_comments" in dict else stream_comments
        self.stream_reports = dict["stream_reports"] if "stream_reports" in dict else stream_reports
        self.stream_mail = dict["stream_mail"] if "stream_mail" in dict else stream_mail
        self.stream_queue = dict["stream_queue"] if "stream_queue" in dict else stream_queue

    def __str__(self):
        str = self.subreddit
        if self.stream_new:
            str += " | New Posts"
        if self.stream_comments:
            str += " | Comments"
        if self.stream_reports:
            str += " | Reports"
        if self.stream_mail:
            str += " | Mod-Mail"
        if self.stream_queue:
            str += " | Mod-Queue"
        return str

    def setup(self):
        sub = self.reddit.subreddit(self.subreddit)

        if sub.quarantine:
            sub.quaran.opt_in()

        settings = sub.mod.settings()
        self.stream_new = False if settings["spam_links"] == "all" or settings["spam_selfposts"] == "all" else True
        self.stream_comments = True if settings["spam_comments"] == "all" else False
        self.stream_queue = True if settings["spam_links"] == "all" or settings["spam_selfposts"] == "all" else False

    def get_dict(self):
        '''
        reactions = list()
        for reaction in self.reactions:
            reactions.append(reaction.get_dict())
        '''

        dict = {
            "subreddit": self.subreddit,
            "stream_new": self.stream_new,
            "stream_comments": self.stream_comments,
            "stream_reports": self.stream_reports,
            "stream_mail": self.stream_mail,
            "stream_queue": self.stream_queue,
            # "reactions": reactions
        }

        return dict

    def get_reactions(self, item, reactions=list(), ce=True):
        if ce:
            try:
                sub = self.reddit.subreddit(self.subreddit)
                reaction_page = sub.wiki['banhammer-reactions']
                result = get_list(reaction_page.content_md)

                ignore = list()
                for item in result:
                    if "ignore" in item:
                        ignore = [i.strip() for i in ignore.split(",")]
                        result.remove(item)

                rs = [Reaction(self.reddit, d) for d in result]
                ignore.extend(rs)
                self.remove_reactions(reactions, ignore) # removes duplicate reactions
                reactions.extend(rs)
            except Exception as e:
                print(e)

        _r = list()
        for reaction in reactions:
            if reaction.eligible(item):
                _r.append(reaction)
        if len(_r) < 1:
            with open(self.dir_path + "/reactions.yaml", encoding="utf8") as f:
                return get_reactions(self.reddit, f.read())

    def remove_reactions(self, reactions, remove):
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

    def get_reaction(self, emoji, item):
        for reaction in self.get_reactions(item):
            if reaction.emoji == emoji:
                return reaction

    def get_new(self):
        sub = self.reddit.subreddit(self.subreddit)

        for submission in sub.new():
            if submission.author is None:
                # item.mod.remove(True)
                continue
            yield submission

    def get_comments(self):
        sub = self.reddit.subreddit(self.subreddit)

        for comment in sub.comments(limit=250):
            if comment.author is None:
                # item.mod.remove(True)
                continue
            yield comment

    def get_reports(self):
        sub = self.reddit.subreddit(self.subreddit)

        for item in sub.mod.reports():
            if item.author is None:
                # item.mod.remove(True)
                continue
            yield item

    def get_mail(self):
        sub = self.reddit.subreddit(self.subreddit)

        for mail in sub.modmail.conversations():
            yield mail

    def get_queue(self):
        sub = self.reddit.subreddit(self.subreddit)

        for item in sub.mod.modqueue():
            if item.author is None:
                # item.mod.remove(True)
                continue
            yield item

    def get_mod_actions(self, mods):
        sub = self.reddit.subreddit(self.subreddit)

        for mod in mods:
            for action in sub.mod.log(limit=None, mod=mod):
                yield action
