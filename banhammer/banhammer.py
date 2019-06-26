import asyncio
import os
from datetime import datetime
from .subreddit import Subreddit
from .reaction import *
from .item import RedditItem
from .yaml import *

class Banhammer():

    def __init__(self, reddit, loop_time=5*60):
        self.reddit = reddit
        self.subreddits = list()
        self.loop = asyncio.get_event_loop()
        self._new = list()
        self.loop_time = loop_time
        if not os.path.exists("files"):
            os.mkdir("files")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def add_subreddits(self, *subs):
        for sub in subs:
            s = Subreddit(self.reddit, subreddit=str(sub))
            s.setup()
            self.subreddits.append(s)

    def new(self, *args, **kwargs):
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
                        if sub.subreddit.lower() == func["sub"].lower():
                            subs.append(sub)
                            break
                else:
                    subs.extend(self.subreddits)
                for sub in subs:
                    path = "files/{}_new.txt".format(self.reddit.subreddit(sub.subreddit).id)
                    ids = list()
                    if os.path.exists(path):
                        with open(path) as f:
                            ids = f.read().splitlines()
                    for post in sub.get_new():
                        item = RedditItem(post)
                        if item.id in ids:
                            break
                        item.save(path)
                        await func["func"](item)
            await asyncio.sleep(self.loop_time)

    def run(self):
        if len(self._new) > 0: self.loop.create_task(self.send_new())
        # self.loop.run_forever()