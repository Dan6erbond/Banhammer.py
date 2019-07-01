import discord

from banhammer import reaction

class CustomReactionPayload(reaction.ReactionPayload):
    def get_embed(self, embed_color=None):
        embed = discord.Embed(
            colour=item.subreddit.banhammer.embed_color if embed_color is None else embed_color
        )

        embed.set_author(name="**{} {} by {}!**".format(self.item.type.title(), " and ".join(self.actions), self.user))

        embed.add_field(name="{} by /u/{}".format(self.item.type.title(), self.item.get_author_name()),
                        value=self.item.get_url(), inline=False)

        return embed