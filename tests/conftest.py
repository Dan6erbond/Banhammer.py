import os

import apraw
import pytest

import banhammer as bh
from banhammer.models import Subreddit

username = os.getenv("USERNAME")
if username is None:
    raise EnvironmentError("USERNAME environment is not set.")

password = os.getenv("PASSWORD")
if password is None:
    raise EnvironmentError("PASSWORD environment is not set.")

client_id = os.getenv("CLIENT_ID")
if client_id is None:
    raise EnvironmentError("CLIENT_ID environment is not set.")

client_secret = os.getenv("CLIENT_SECRET")
if client_secret is None:
    raise EnvironmentError("CLIENT_SECRET environment is not set.")


@pytest.fixture
def reddit():
    reddit = apraw.Reddit(client_id=client_id, client_secret=client_secret,
                          password=password, username=username)
    return reddit


@pytest.fixture
def banhammer(reddit):
    b = bh.Banhammer(reddit)
    return b


@pytest.fixture
def subreddit(banhammer):
    sub = Subreddit(banhammer, subreddit="banhammerdemo")
    return sub
