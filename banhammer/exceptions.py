class BanhammerException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class NotModerator(BanhammerException):
    def __init__(self, user, sub):
        super(NotModerator, self).__init__("/u/{} doesn't moderate /r/{}.".format(user, sub))


class NoRedditInstance(BanhammerException):
    def __init__(self, sub):
        super(NotModerator, self).__init__(
            "No <praw.Reddit> instance was given to the Subreddit <banhammer.Subreddit({})>".format(sub))


class NoItemGiven(BanhammerException):
    def __init__(self):
        super(NotModerator, self).__init__("No <banhammer.RedditItem> was given to the <banhammer.Reaction> instance.")


class NotEligibleItem(BanhammerException):
    def __init__(self):
        super(NotModerator, self).__init__(
            "The <banhammer.RedditItem> given to the <banhammer.Reaction> object cannot be handled.")
