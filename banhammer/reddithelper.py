import praw
from .item import RedditItem
from urllib.parse import urlparse

def get_item(bh, str):
    url = ""
    for line in str.splitlines():
        for segment in line.split(" "):
            if is_url(segment.strip()):
                url = segment.strip()

    if url == "" or url is None:
        return None

    if url.startswith("https://mod.reddit.com/mail/all/"):
        id = url.strip()[-5:]

        for subreddit in bh.subreddits:
            try:
                modmail = subreddit.subreddit.modmail(id)
                if hasattr(modmail, "subject"):
                    return RedditItem(modmail, subreddit, "message")
            except Exception as e:
                print("{}: {}".format(type(e), e))

        return None

    item = None
    try:
        item = bh.reddit.comment(url=url)
    except:
        try:
            item = bh.reddit.submission(url=url)
        except:
            print("Invalid URL!")
            return None

    try:
        if not hasattr(item, "subreddit"):  # truly verify if it's a reddit comment or submission
            return None
    except:
        return None

    sub = None
    for sub in bh.subreddits:
        if sub.subreddit.id == item.subreddit.id:
            subreddit = sub
            break

    if subreddit is None:
        return None

    return RedditItem(item, subreddit, "message")

def get_item_url(item):
    if isinstance(item, praw.models.Submission):
        return "https://www.reddit.com/r/{}/comments/{}".format(item.subreddit, item)
    elif isinstance(item, praw.models.Comment):
        return "https://www.reddit.com/r/{}/comments/{}/_/{}".format(item.subreddit, item.submission, item)
    elif isinstance(item, praw.models.ModmailConversation):
        return "https://mod.reddit.com/mail/all/" + item.id
    elif isinstance(item, praw.models.Message):
        if item.was_comment:
            return "https://www.reddit.com/r/{}/comments/{}/_/{}".format(item.subreddit, item.submission, item)
        else:
            return "https://www.reddit.com/message/messages/{}".format(item)
    elif isinstance(item, praw.models.Subreddit):
        return "https://www.reddit.com/r/" + item.display_name

def is_url(url):
    check = urlparse(url)
    if check.scheme != "" and check.netloc != "":
        return True
    else:
        return False