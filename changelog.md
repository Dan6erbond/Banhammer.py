2019-07-06 v1.15.0

**Changelog:**
 - Default reactions are indented for Reddit's formatting.
 - `Banhammer.remove_subreddit()` takes `str` and `banhammer.Subreddit`.
 - Support for indents in YAML added to `banhammer.YAMLParser`.
 - Code clean-up, `__init__.py` pre-imports classes and scripts.
 - Improved efficiency by limiting repeitions of calling `Payload.feed()`.
 - Added `Subreddit.ignore_old()`.
 
2019-07-10 v1.16.0

**Changelog:**
 - Improved support for modmail.
 - "dismissed" automatically added to `ReactionPayload.actions` if empty.
 - ✉ Default modmail reaction to dismiss.
 - Fixed `RedditHelper.get_item_from_url()`.
 
2019-07-10 v1.17.0

**Changelog:**
 - Moved package information to `config.py`.
 - Added `Config.BOT_VERSION_TEXT`, `BOT_FOOTER` and `BOT_DISCLAIMER`.
 - Added `MessageBuilder.get_ban_message()`.
 - Fixed banning users in `banhammer.ReactionHandler`.
 - Added `Subreddit.get_contact_url()`.