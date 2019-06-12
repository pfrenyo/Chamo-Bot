from discord.ext import commands
import asyncio
import feedparser
from difflib import get_close_matches
HORRIBLESUBS_720p_URL = "http://www.horriblesubs.info/rss.php?res=720"
RSSMANAGER_DATA_FILE = 'data/info/horriblesubs_720p.json'


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                           Cog handling RSS subs from HorribleSubs (for anime updates)                               #
#######################################################################################################################
class RSSManager(commands.Cog):
    # Big thanks to Baawaah, AKA S.TRAN, for teaching me how to make a discord bot and use RSS feeds.
    # This class is my own take on Baawaah's Anime RSS manager:
    # https://github.com/Baawaah/DiscordBot-2N/blob/master/extensions/Anime.py
    # Many thanks!
    def __init__(self, client):
        self.client = client
        self.valid_channels = []  # For all channels you can spam with anime rss updates

    async def horriblesubs_720p_loop(self):

        # Getting the RSS feed from Horriblesubs
        feed = feedparser.parse(HORRIBLESUBS_720p_URL)

        # Getting the names of the anime to watch out for
        # anime_names = list(HSDATAFILE LOL)

        # feed keys look like :
        # ['feed', 'entries', 'bozo', 'headers', 'href', 'status', 'encoding', 'version', 'namespaces']

        return

    @commands.command(name='addanime')
    async def addanime(self, context, anime_name, attribute=None):

        # Getting the RSS feed from Horriblesubs
        feed = feedparser.parse(HORRIBLESUBS_720p_URL)

        valid_names = set([entry['title'].lstrip('[HorribleSubs]')
                                         .lstrip(' ')
                                         .rstrip(' 0123456789[p].mkv')
                                         .rstrip('-')
                                         .rstrip(' ')
                          for entry in feed['entries']])
        # The argument is not a prefix; rather, all combinations of its values are stripped.
        # We could use .rstrip(' -0123456789[]p.mkv'), but it would be dangerous for anime with numbers in their name.

        if anime_name in valid_names:
            # do stuff
            return
        else:
            similar_names = get_close_matches(anime_name, valid_names, n=7)  # Will give the 7 closest names, if any
            if not similar_names:
                await context.send("The anime you're trying to add to the watch list doesn't seem to exist, "
                                   "and no similar matches have been found between the names of the anime among"
                                   "the last entries on HorribleSubs' 720p RSS feed.\n"
                                   "If you want to force an anime that's not yet out onto the watch list,\n"
                                   "you can add it with '!addanime anime_name --force', but you have to be sure of\n"
                                   "the name you're using (for instance, Attack on Titan's 3rd season is called \n"
                                   "'Shingeki no Kyojin S3' on HorribleSubs, and there may be no way to know which name"
                                   "is going to be used for a future anime.")
            else:
                await context.send("The anime you're trying to add on the watch list doesn't seem to exist.\n"
                                   "However, we found anime(s) with similar names among the last 50 entries on "
                                   "HorribleSubs' 720p RSS feed.\n\n"
                                   "**Did you mean to add any of the following?**\n"
                                   "*>> {}*".format(', '.join(similar_names)))


def setup(client):
    client.add_cog(RSSManager(client))
