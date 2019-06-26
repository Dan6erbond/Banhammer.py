import asyncio
import os

from .subreddit import Subreddit
from .reddithelper import *
from .item import RedditItem

class Banhammer:

    def __init__(self, reddit, loop_time=5 * 60):
        self.reddit = reddit
        self.subreddits = list()
        self.loop = asyncio.get_event_loop()
        self._new = list()
        self.loop_time = loop_time
        if not os.path.exists("files"):
            os.mkdir("files")

    def add_subreddits(self, *subs):
        for sub in subs:
            if type(sub) != Subreddit:
                sub = Subreddit(self.reddit, subreddit=str(sub))
                sub.setup()
            self.subreddits.append(sub)

    def new(self, **kwargs):
        def assign(func):
            data = {
                "func": func,
                "sub": kwargs["subreddit"] if "subreddit" in kwargs else None
            }
            self._new.append(data)
            return data

        return assign

    async def send_new(self):
        while True:
            for func in self._new:
                subs = list()
                if func["sub"] is not None:
                    for sub in self.subreddits:
                        if str(sub.subreddit).lower() == func["sub"].lower():
                            subs.append(sub)
                            break
                else:
                    subs.extend(self.subreddits)
                for sub in subs:
                    for post in sub.get_new():
                        await func["func"](post)
            await asyncio.sleep(self.loop_time)

    def get_item(self, str):
        item = get_item(self, str)
        return RedditItem(item["item"], item["subreddit"], "message")

    def run(self):
        if len(self._new) > 0: self.loop.create_task(self.send_new())
        # self.loop.run_forever()
