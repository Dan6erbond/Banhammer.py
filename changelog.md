2019-07-06 v1.15.0

**Changelog:**
 - Default reactions are indented for Reddit's formatting.
 - `Banhammer.remove_subreddit()` takes `str` and `banhammer.Subreddit`.
 - Support for indents in YAML added to `banhammer.YAMLParser`.
 - Code clean-up, `__init__.py` pre-imports classes and scripts.
 - Improved efficiency by limiting repeitions of calling `Payload.feed()`.
 - Added `Subreddit.ignore_old()`.