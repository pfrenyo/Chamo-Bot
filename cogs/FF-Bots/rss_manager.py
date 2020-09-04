import json
import discord
import asyncio
import datetime
import feedparser
from os.path import join
from pprint import pprint
from urllib.parse import urlparse
from difflib import get_close_matches
from discord.ext.commands import Cog, command, check_any, is_owner, has_permissions

HORRIBLE720 = 'horriblesubs_720p'
HORRIBLESUBS_720p_URL = "http://www.horriblesubs.info/rss.php?res=720"
RSSMANAGER_DATA_FILE = join("data", "info", "rssmanager.json")
HOTPINK = 0xFF69B4
MISSING_THUMBNAIL = 'https://i.imgur.com/h7AYd0H.png'
HORRIBLESUBS_BASE_URL = 'https://horriblesubs.info/shows/'
RSS_SLEEPTIME = 60
HS_ANIME_NOT_EXIST = "The anime you're trying to add to the watch list doesn't seem to exist, "\
                     "and no similar match has been found among the names of "\
                     "the last entries on HorribleSubs' 720p RSS feed.\n\n"\
                     "If you want to force an anime that's not out yet onto the watch list, "\
                     "you can add it with \n"\
                     "*!addanime anime_name --force*, "\
                     "but you have to be sure of the name you're using.\n\n"\
                     "(for instance, Attack on Titan's 3rd season is called 'Shingeki no Kyojin S3' "\
                     "on HorribleSubs,\n and there may be no way to know which name "\
                     "is going to be used for a future anime)"
HS_ANIME_SIMILAR_FOUND = "The anime you're trying to add on the watch list doesn't seem to exist.\n"\
                         "However, we found anime(s) with similar names among the last 50 entries on "\
                         "HorribleSubs' 720p RSS feed.\n\n"\
                         "**Did you mean to add any of the following?**\n"\
                         "*>> {}*"
SHADOWVERSE_CHANNEL = 559401293928464417


#######################################################################################################################
#                                             Helper functions                                                        #
######################################################################################################################

# Function to help us create pretty embeds for updates about new anime episodes on HorribleSubs.
#
# @pre: the name of the anime, the rssinfo of the anime.
# @post: a pretty embed to be sent by the bot
def create_embed_horriblesubs(anime_name, episode_number, rssinfo):
    base_url = rssinfo[HORRIBLE720][anime_name].setdefault('base_url', '') or \
               HORRIBLESUBS_BASE_URL + anime_name.lower().replace(' ', '-')
    episode_url = base_url + '/#' + episode_number
    episode_date = datetime.datetime.fromtimestamp(rssinfo[HORRIBLE720][anime_name]['last_update'])

    embed = discord.Embed(title=anime_name, description='New episode out on HorribleSubs!', color=HOTPINK)
    embed.set_author(name='HorribleSubs')
    embed.set_thumbnail(url=rssinfo[HORRIBLE720][anime_name]['thumbnail'] or MISSING_THUMBNAIL)
    embed.add_field(name="Name", value=anime_name, inline=True)
    embed.add_field(name="Episode", value=episode_number, inline=True)
    embed.add_field(name="URL", value=episode_url, inline=False)
    embed.set_footer(text='Uploaded on {}'.format(str(episode_date)))
    return embed


# Function to help us get the episode number from an entry title coming from a HorribleSubs RSS feed.
#
# @pre: from a HS RSS feed, feed['entry'][i]['title'] (which is a string)
# @post: an episode number, as a string
def get_episode_number(title):
    return title.lstrip('[HorribleSubs]').lstrip(' ')\
                .rstrip('[720p].mkv').rstrip(' ')\
                .split(' - ')[1]


# Function to create an empty anime RSS entry.
#
# @pre: /
# @post: an empty RSS entry for an anime (for HorribleSubs' 720p feed)
def create_empty_anime():
    return {'channels': [],
            'last_update': 0,
            'thumbnail': '',
            'base_url': ''}


#######################################################################################################################
#                                        ---  'RSS Manager' cog  ---                                                  #
#                            Cog handling RSS feeds from HorribleSubs (for anime updates)                             #
#######################################################################################################################
class RSSManager(Cog):
    # Big thanks to Baawaah, AKA S.TRAN, for teaching me how to make a discord bot and use RSS feeds.
    # This class is my own take on Baawaah's Anime RSS manager:
    # https://github.com/Baawaah/DiscordBot-2N/blob/master/extensions/Anime.py
    # Many thanks!
    def __init__(self, client):
        self.client = client

        # Loading information on RSSManager from previous iterations
        try:
            with open(RSSMANAGER_DATA_FILE, 'r') as f:
                self.rssinfo = json.load(f)
                print("> Successfully loaded data from {}".format(RSSMANAGER_DATA_FILE))
        except IOError:
            print("/!\\ RSSMANAGER DATA (RSSINFO) NOT FOUND AT {}, DEFAULTING TO BLANK VALUES!"
                  .format(RSSMANAGER_DATA_FILE))
            self.rssinfo = {
                HORRIBLE720: {}
            }
            with open(RSSMANAGER_DATA_FILE, 'w') as f:
                json.dump(self.rssinfo, f)

    # Save function to keep information about RSSManager between instances
    async def save_rssmanager_data(self):
        with open(RSSMANAGER_DATA_FILE, 'w') as f:
            json.dump(self.rssinfo, f)

    # Load function loading up information about previous instances of RSSManager
    async def load_rssmanager_data(self):
        with open(RSSMANAGER_DATA_FILE, 'r') as f:
            self.rssinfo = json.load(f)

    @Cog.listener()
    async def on_ready(self):
        await self.horriblesubs_720p_loop()

    @Cog.listener()
    async def on_message(self, message):
        if message.channel.id == SHADOWVERSE_CHANNEL and message.content[0] in self.client.BOT_PREFIX:
            pass

    # Btw the reason we're working with last_update times instead of episode numbers is because sometimes,
    # episode '0' comes out after a few episodes are already out.

    async def horriblesubs_720p_loop(self):

        # Getting the RSS feed from Horriblesubs
        feed = feedparser.parse(HORRIBLESUBS_720p_URL)
        # feed keys look like :
        # ['feed', 'entries', 'bozo', 'headers', 'href', 'status', 'encoding', 'version', 'namespaces']

        # Getting the names of the anime to watch out for
        watchlist = self.rssinfo[HORRIBLE720].keys()

        for entry in reversed(feed['entries']):  # We go from oldest to newest in case our bot went offline or missed anything
            for anime_name in watchlist:
                if anime_name in entry['title']:
                    date = entry['published_parsed']
                    entry_update = datetime.datetime(year=date.tm_year, month=date.tm_mon, day=date.tm_mday,
                                                     hour=date.tm_hour, minute=date.tm_min, second=date.tm_sec).timestamp()
                    if entry_update > self.rssinfo[HORRIBLE720][anime_name]['last_update']:
                        self.rssinfo[HORRIBLE720][anime_name]['last_update'] = entry_update
                        episode_number = get_episode_number(entry['title'])
                        embed = create_embed_horriblesubs(anime_name, episode_number, self.rssinfo)
                        for channel_id in self.rssinfo[HORRIBLE720][anime_name]['channels']:
                            channel = self.client.get_channel(channel_id)
                            if channel:
                                await channel.send(embed=embed)
                            else:
                                user = self.client.get_user(channel_id)
                                if user:
                                    await user.send(embed=embed)

        await self.save_rssmanager_data()
        await asyncio.sleep(RSS_SLEEPTIME)
        await asyncio.ensure_future(self.horriblesubs_720p_loop())

    @command(name='addanime')
    async def addanime(self, context):

        cur_channel = context.channel.id

        # Parsing command content
        content = context.message.content.lstrip(''.join(self.client.BOT_PREFIX)+'addanime').strip()
        force = False
        if content.endswith('--force'):
            force = True
            content = content.rstrip('--force').rstrip(' ')
        if content.startswith('"') and content.endswith('"'):
            content = content.strip('" ')
        anime_name = content

        if context.guild is None:
            cur_channel = context.author.id

        if anime_name in self.rssinfo[HORRIBLE720].keys():
            if cur_channel in self.rssinfo[HORRIBLE720][anime_name]['channels']:
                await context.send("The anime *{}* is already on this channel's watch list.".format(anime_name))
                return

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
            if cur_channel not in self.rssinfo[HORRIBLE720].setdefault(anime_name,
                                                                       create_empty_anime())['channels']:
                self.rssinfo[HORRIBLE720][anime_name]['channels'].append(cur_channel)
                await context.send("Understood. The anime *{0}* has been added to this channel's watch list.\n"
                                   "The latest episode this bot has detected for this anime is the following:"
                                   .format(anime_name))

                feed = feedparser.parse(HORRIBLESUBS_720p_URL)

                for entry in feed['entries']:
                    if anime_name in entry['title']:
                        latest_ep = entry
                        break

                if self.rssinfo[HORRIBLE720][anime_name]['last_update'] == 0:
                    date = latest_ep['published_parsed']
                    self.rssinfo[HORRIBLE720][anime_name]['last_update'] = \
                        datetime.datetime(year=date.tm_year, month=date.tm_mon, day=date.tm_mday,
                                          hour=date.tm_hour, minute=date.tm_min, second=date.tm_sec).timestamp()

                episode_number = get_episode_number(latest_ep['title'])
                embed = create_embed_horriblesubs(anime_name, episode_number, self.rssinfo)
                await context.send(embed=embed)
                await self.save_rssmanager_data()

        else:
            if force:
                if cur_channel not in self.rssinfo[HORRIBLE720].setdefault(anime_name,create_empty_anime())['channels']:
                    self.rssinfo[HORRIBLE720][anime_name]['channels'].append(cur_channel)
                    await context.send("Very well. The anime *{0}* has been **forcefully** added to this channel's "
                                       "watch list.\n"
                                       "I hope that you know what you're doing."
                                       .format(anime_name))
                    await self.save_rssmanager_data()
            else:
                similar_names = get_close_matches(anime_name, valid_names, n=7)  # Will give the 7 closest names, if any
                if not similar_names:
                    await context.send(HS_ANIME_NOT_EXIST)
                else:
                    await context.send(HS_ANIME_SIMILAR_FOUND.format(', '.join(similar_names)))

    @command(name='delanime')
    async def delanime(self, context):
        # Note: currently throws an Exception if deleting from PM channel (which is None). Fix this!
        content = context.message.content.lstrip(''.join(self.client.BOT_PREFIX) + 'delanime').strip()
        if content.startswith('"') and content.endswith('"'):
            content = content.strip('" ')

        if content in self.rssinfo[HORRIBLE720].keys():
            self.rssinfo[HORRIBLE720][content]['channels'].remove(context.channel.id)
            await context.send("The anime *{}* has been successfully deleted from this channel's watch list.\n"
                               .format(content))
            await self.save_rssmanager_data()
            if not self.rssinfo[HORRIBLE720][content]['channels']:
                owner = self.client.owner
                await owner.send("Hello administrator {0.mention}, "
                                 "there seem to be no channels watching *{1}* left.\n".format(owner, content))
        else:
            await context.send("The anime *{}* doesn't seem to be on this channel watch list.\n"
                               "There is nothing to delete.".format(content))

    @command(name='lastupdate')
    async def lastupdate(self, context):
        content = context.message.content.lstrip(''.join(self.client.BOT_PREFIX)+'lastupdate').strip().lower()
        if content.startswith('"') and content.endswith('"'):
            content = content.strip('" ')

        if content in list(map(lambda x: x.lower(), self.rssinfo[HORRIBLE720].keys())):
            anime_name = get_close_matches(content, self.rssinfo[HORRIBLE720].keys(), n=1)[0]
            epoch = self.rssinfo[HORRIBLE720][anime_name]['last_update']

            if epoch == 0:
                await context.send("The anime *{}* has yet to receive an update pn HorribleSubs."
                                   .format(anime_name))
                return

            date = datetime.datetime.fromtimestamp(epoch)
            await context.send("The anime *{}* has last been updated on HorribleSubs on {} (epoch: {})"
                               .format(anime_name, str(date), str(epoch)))

        else:
            await context.send("The anime you mentionned (*{}*) doesn't seem to be in my HorribleSubs feed database.\n"
                               "Use *!addanime* to add an anime of your choice to my feed.".format(content))

    @command()
    async def addthumbnail(self, context, url, *, anime_name):
        if anime_name.startswith('"') and anime_name.endswith('"'):
            anime_name = anime_name.strip('" ')

        if anime_name in self.rssinfo[HORRIBLE720].keys():
            url_parsed = urlparse(url)
            if url_parsed.scheme and url_parsed.netloc:  # If these two exist, it is a valid URL according to urlparse
                self.rssinfo[HORRIBLE720][anime_name]['thumbnail'] = url
                await context.send("Successfully added thumbnail to *{}*.".format(anime_name))
                await self.save_rssmanager_data()
        else:
            await context.send("You cannot add a thumbnail to an anime that's not even in the database.\n"
                               "Use *!addanime* to add it first.")

    # Force-delete an entire anime entry, deleting all the channels, the thumbnail, last update time, etc. with it.
    @command(name='forcedelanime_iamsure', hidden=True)
    async def forcedelanime_iamsure(self, context):
        if is_bot_admin(context):
            content = context.message.content.lstrip(''.join(self.client.BOT_PREFIX) + 'forcedelanime_iamsure')\
                                             .strip()
            if content.startswith('"') and content.endswith('"'):
                content = content.strip('" ')

            if content in self.rssinfo[HORRIBLE720].keys():
                del self.rssinfo[HORRIBLE720][content]
                await context.send("Anime *{}* has been forcefully deleted from the database by the administrator."
                                   .format(content))
                await self.save_rssmanager_data()
            else:
                await context.send("Anime name *{}* seems to be invalid.".format(content))
        else:
            await context.send("Only the adminstrator can use the *force delete* function")

    # Modify the url basis of an anime.
    @check_any(has_permissions(administrator=True), is_owner())
    @command(name='addurl', hidden=True)
    async def addurl(self, context, url, *, anime_name):
        if anime_name.startswith('"') and anime_name.endswith('"'):
            anime_name = anime_name.strip('" ')

        if anime_name in self.rssinfo[HORRIBLE720].keys():
            url_parsed = urlparse(url)
            if url_parsed.scheme and url_parsed.netloc:  # If these two exist, it is a valid URL according to urlparse
                self.rssinfo[HORRIBLE720][anime_name]['base_url'] = url
                await context.send("Successfully added base_url to *{}*.".format(anime_name))
                await self.save_rssmanager_data()

    # Dumps self.rssinfo in a pretty print on stdout.
    @is_owner()
    @command(name='dumprssinfo', hidden=True)
    async def dumprssinfo(self, context):
        pprint(self.rssinfo)


def setup(client):
    client.add_cog(RSSManager(client))
