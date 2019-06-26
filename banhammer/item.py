import praw


class RedditItem:

    def __init__(self, item, subreddit, source):
        self.item = item
        self.id = item.id
        self.type = "submission" if type(item) == praw.models.Submission else "comment" if type(
            item) == praw.models.Comment else "modmail"
        self.subreddit = subreddit
        self.source = source

    def __str__(self):
        return "New {} in /r/{} by /u/{}!\n\n**Title:** {}\n**Body:**\n{}".format(self.type, self.item.subreddit,
                                                                                  self.item.author, self.item.title,
                                                                                  self.item.selftext)

    def save(self, path):
        with open(path, "a+") as f:
            f.write("\n" + self.item.id)

    def get_reactions(self):
        return self.subreddit.get_reactions(self.item)