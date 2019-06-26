import json
import praw
import os
from .yaml import *
from .reaction import *
from .item import *

class Subreddit:

    def __init__(self, reddit, dict={}, subreddit="", stream_new=True, stream_comments=False, stream_reports=True, stream_mail=True, stream_queue=True):
        self.reddit = reddit

        self.subreddit = dict["subreddit"] if "subreddit" in dict else subreddit
        if type(self.subreddit) == str: self.subreddit = reddit.subreddit(self.subreddit)

        self.name = self.subreddit.display_name.replace("r/", "").replace("/", "")

        self.stream_new = dict["stream_new"] if "stream_new" in dict else stream_new
        self.stream_comments = dict["stream_comments"] if "stream_comments" in dict else stream_comments
        self.stream_reports = dict["stream_reports"] if "stream_reports" in dict else stream_reports
        self.stream_mail = dict["stream_mail"] if "stream_mail" in dict else stream_mail
        self.stream_queue = dict["stream_queue"] if "stream_queue" in dict else stream_queue

        self.reactions = list()
        self.load_reactions()

    def __str__(self):
        str = "/r/" + self.name
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
        if self.subreddit.quarantine:
            self.subreddit.quaran.opt_in()

        settings = self.subreddit.mod.settings()
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
            "subreddit": self.name,
            "stream_new": self.stream_new,
            "stream_comments": self.stream_comments,
            "stream_reports": self.stream_reports,
            "stream_mail": self.stream_mail,
            "stream_queue": self.stream_queue,
            # "reactions": reactions
        }

        return dict

    def load_reactions(self, custom=True):
        if custom:
            try:
                reaction_page = self.subreddit.wiki['banhammer-reactions']
                result = get_reactions(self.reddit, reaction_page.content_md)["reactions"]
            except Exception as e:
                print(e)

        if not len(self.reactions) > 0:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            with open(dir_path + "/reactions.yaml", encoding="utf8") as f:
                self.reactions = get_reactions(self.reddit, f.read())["reactions"]

    def get_reactions(self, item):
        _r = list()
        for reaction in self.reactions:
            if reaction.eligible(item):
                _r.append(reaction)
        return _r

    def get_reaction(self, emoji, item):
        for reaction in self.get_reactions(item):
            if reaction.emoji == emoji:
                return reaction

    def get_new(self):
        path = "files/{}_new.txt".format(self.subreddit.id)
        ids = list()
        if os.path.exists(path):
            with open(path) as f:
                ids = f.read().splitlines()
        for submission in self.subreddit.new():
            if submission.id in ids:
                break
            item = RedditItem(submission, self, "new")
            item.save(path)
            yield item

    def get_comments(self):
        path = "files/{}_comments.txt".format(self.subreddit.id)
        ids = list()
        if os.path.exists(path):
            with open(path) as f:
                ids = f.read().splitlines()
        for comment in self.subreddit.comments(limit=250):
            if submission.id in ids:
                break
            item = RedditItem(comment, self, "new")
            item.save(path)
            yield item

    def get_reports(self):
        path = "files/{}_reports.txt".format(self.subreddit.id)
        ids = list()
        if os.path.exists(path):
            with open(path) as f:
                ids = f.read().splitlines()
        for item in self.subreddit.mod.reports():
            if item.id in ids:
                break
            item = RedditItem(item, self, "reports")
            item.save(path)
            yield item

    def get_mail(self):
        path = "files/{}_mail.txt".format(self.subreddit.id)
        ids = list()
        if os.path.exists(path):
            with open(path) as f:
                ids = f.read().splitlines()
        for mail in self.subreddit.modmail.conversations():
            if mail.id in ids:
                break
            item = RedditItem(mail, self, "modmail")
            item.save(path)
            yield item

    def get_queue(self):
        path = "files/{}_queue.txt".format(self.subreddit.id)
        ids = list()
        if os.path.exists(path):
            with open(path) as f:
                ids = f.read().splitlines()
        for item in self.subreddit.mod.modqueue():
            if item.id in ids:
                break
            item = RedditItem(item, self, "queue")
            item.save(path)
            yield item

    def get_mod_actions(self, mods):
        path = "files/{}_actions.txt".format(self.subreddit.id)
        ids = list()
        if os.path.exists(path):
            with open(path) as f:
                ids = f.read().splitlines()
        for action in self.subreddit.mod.log(limit=None):
            if action.id in ids:
                break
            if str(action.mod).lower() in mods:
                item = RedditItem(action, self, "log")
                item.save(path)
                yield item
