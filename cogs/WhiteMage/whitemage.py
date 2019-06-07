import discord
from discord.ext import commands
import feedparser
import json
import time

WHITEMAGE_DATA_FILE = 'data/info/whitemage.json'


class WhiteMage(commands.Cog):
    def __init__(self, client):
        self.client = client

        try:
            with open(WHITEMAGE_DATA_FILE, 'r') as f:
                self.info = json.load(f)
        except IOError:
            print("/!\\ WHITEMAGE DATA (INFO) NOT FOUND AT {}, DEFAULTING TO BLANK VALUES!".format(WHITEMAGE_DATA_FILE))
            self.info = {
                'known_guilds': [],
                'latest_update_time': time.time()
            }

    async def save_whitemage_data(self):
        with open(WHITEMAGE_DATA_FILE, 'w') as f:
            json.dump(self.info, f)

    async def load_whitemage_data(self):
        with open(WHITEMAGE_DATA_FILE, 'r') as f:
            self.info = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(name="Hello Nurse!", type=discord.ActivityType['listening']))
        whitemage_intro_msg = ":flag_us: Allow me to introduce myself.\nI am WhiteMage, " \
                              "a gentle bot designed to help you with your general health needs.\n" \
                              'I reply to commands starting with the \'?\' sign. ' \
                              'To get all of my possible commands, just type \'?help\' ' \
                              "in any chatroom or via PM.\n" \
                              'I generally work by pinging you via Personal Messages (PMs). ' \
                              "Please treat me kindly.\n" \
                              'PS : If you have any ideas about some improvements for this bot, ' \
                              'please send them ' \
                              'to my maker, {0.mention}.' \
                              "\n\n" \
                              ":flag_fr: Permettez-moi de me présenter.\n Je suis WhiteMage, " \
                              'un gentil bot infirmier conçu pour vous aider quant à vos ' \
                              "besoins de santé.\n" \
                              'Je réponds aux commandes commençant par le caractère \'?\'. ' \
                              'Pour connaitre l\'entièreté de mes commandes, tapez \'?help\' dans ' \
                              "n\'importe quel salon de chat ou via MP.\n" \
                              'En général, je compte vous ping via Message Personnel (MP). ' \
                              "Soyez gentil avec moi.\n" \
                              'PS : Si vous avez des idées d\'améliorations pour ce bot, ' \
                              'veuillez les envoyer à mon' \
                              'créateur, {0.mention}.'.format(await self.client.fetch_user(self.client.ADMIN_ID))
        for guild in self.client.guilds:
            # Note : a 'discord guild' is a synonym for a 'discord server'.
            # We chose to keep 'guild' for consistency with the API.
            if guild.id not in self.info.setdefault('known_guilds', []):
                self.info['known_guilds'].append(guild.id)
                await guild.system_channel.send(whitemage_intro_msg)
            else:
                if time.time() - self.info.setdefault('latest_update_time', time.time()) > 86401:
                    # 86400 is the number of seconds in a day.
                    # This is so the update message only appears once per day at best.
                    self.info['latest_update_time'] = time.time()
                    await guild.system_channel.send(":flag_us: I seem to have been updated / "
                                                    ":flag_fr: On dirait bien que j'ai été mis à jour.")
        await self.save_whitemage_data()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None \
                and message.author != self.client.user\
                and message.content[0] not in self.client.BOT_PREFIX:  # On PM (sometimes called DM) only
            await message.channel.send("\n:flag_us: Hi, I'm WhiteMage, a gentle nurse bot designed to help you with "
                                       "your general health needs. I reply to commands starting with '?'.\n"
                                       "You can get all of my commands by using *?help*, which I advise you to do."
                                       "\n:flag_fr: Bonjour, je suis WhiteMage, le gentil bot infirmier conçu pour vous"
                                       " aider quant à vos besoins de santé. Je réponds aux commandes commençant "
                                       "par '?'.\n"
                                       "Vous pouvez utiliser *?help* pour connaitre l'entiereté de mes commandes, "
                                       "ce que je vous recommande de faire.")



    @commands.command(name='wrist',
                      aliases=['wrists'],
                      brief='Info on commands related to wrists',
                      description='Provides information relative to WhiteMage\'s commands related to wrist exercises')
    async def wrist(self, context):
        await context.send("I can provide you with either a video or summary image of wrist exercises for Gamers.\n"
                           "The commands *?wristimage* and *?wristvideo* (and their respective variants) "
                           "provide you with the respective media.\n"
                           "To get all my commands, use *?help*.\n"
                           "I can also ping you for these very same wrist exercises via *?start* (temporary name), "
                           "which you need to use when you start playing a game.\n"
                           "**Please take care of your wrists!**")

    @commands.command(name='wristimage',
                      aliases=['wrist_image', 'wrist-image'],
                      brief="Summary image of Dr. Levi's wrist exercises.",
                      description="Provides an image summarizing the exercises recommended by Dr. Levi in his video "
                                  "(available with the '?wristvideo' commands and its variants)")
    async def wrist_image(self, context):
        await context.send("Here's a summary of wrist exercises recommended by Dr. Levi in his Youtube video "
                           "(provided below).\n"
                           "When you start playing a game, use *?start* to have me ping you with a PM at specific "
                           "time intervals to remind you to do the different wrist exercises on the image,\nusing the "
                           "recommended time intervals for each different exercise.\n"
                           "https://imgur.com/5vktp17\n")

    @commands.command(name='wristvideo',
                      aliases=['wrist_video', 'wrist-video'],
                      brief="Video of Dr. Levi's hand and wrist exercises.",
                      description="Provides you with the link to the video of the hand and wrist exercises recommended "
                                  "by Dr. Levi.")
    async def wrist_video(self, context):
        await context.send("Here's the video of hand and wrist exercises recommended by Dr. Levi (provided below).\n"
                           "When you start playing a game, use *?start* to have me ping you with a PM at specific "
                           "time intervals to remind you to do the different wrist exercises in this video,\nusing the "
                           "recommended time intervals for each different exercise.\n"
                           "https://www.youtube.com/watch?v=EiRC80FJbHU\n")


def setup(client):
    client.add_cog(WhiteMage(client))