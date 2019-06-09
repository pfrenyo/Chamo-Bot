import discord
from discord.ext import commands
import json
import time
import asyncio

LOOP_CHECK_TIME = 60  # Check the loop every minute
ALSO_MARGIN = (2 * LOOP_CHECK_TIME) + 1
WHITEMAGE_DATA_FILE = 'data/info/whitemage.json'
WRIST_100 = 'https://imgur.com/Slnwo1y'
WRIST_130 = 'https://imgur.com/8bdFs07'
WRIST_230 = 'https://imgur.com/UbYhjhm'
WRIST_330 = 'https://imgur.com/PgrSu3b'
HOUR100 = 3600
HOUR130 = 5400
HOUR230 = 9000
HOUR330 = 12600  # 3h30 in seconds
ALSO = '**Also (but do not forget to do the above exercise(s) as well)**, '
DONTFORGET = "If you have time, don't forget to "
PASSED_330 = "3 hours and a half have passed. It's time to "
EXO_330 = "stretch your forearms.\n" \
          "You will need to *gently* pull on your fingers, hands and wrists " \
          "and feel your forearm muscles stretching.\n" \
          "Keep each stretch going for about 30 seconds (totalizing to 3 minutes, 3 stretches per arm).\n" \
          "Follow the indications on the image below, or check out the video with *?wristvideo*.\n" \
          "{}".format(WRIST_330)
PASSED_230 = "2 hours and a half have passed. It's time to "
EXO_230 = "shake your wrists and fingers.\n" \
          "*Gently* shake out your fingers and your wrists for about 1 minute.\n" \
          "Follow the indications on the image below, or check out the video with *?wristvideo*.\n" \
          "{}".format(WRIST_230)
PASSED_130 = "an hour and a half have passed. It's time to "
EXO_130 = "stretch your fingers and thumb, " \
          "and open and close your hands a few times.\n" \
          "You can check out the specific instructions for this part with the *?thumb* function.\n" \
          "It will start the video at the correct timestamp. I recommend you to check it out " \
          "if this is your first time.\n" \
          "Follow the indications on the image below, or check out the video with *?thumb*.\n" \
          "{}".format(WRIST_130)
PASSED_100 = "an hour has passed. It's time for "
EXO_100 = "some hand exercises.\n" \
          "Two things are recommended every hour:\n" \
          "1) Alternate between full fist, open fist, table top, claw fist and half fist a few times.\n" \
          "2) Massage your hands with your opposite thumb.\n" \
          "Follow the indications on the image below, or check out the video with *?wristvideo*.\n" \
          "{}".format(WRIST_100)
WHITEMAGE_BRIEF = "\n:flag_us: Hi, I'm WhiteMage, a gentle nurse bot designed to help you with " \
                  "your general health needs. I reply to commands starting with '?'.\n"\
                  "You can get all of my commands by using *?help*, which I advise you to do."\
                  "\n:flag_fr: Bonjour, je suis WhiteMage, le gentil bot infirmier conçu pour vous"\
                  " aider quant à vos besoins de santé. Je réponds aux commandes commençant "\
                  "par '?'.\n"\
                  "Vous pouvez utiliser *?help* pour connaitre l'entiereté de mes commandes, "\
                  "ce que je vous recommande de faire."


def _is_admin(self, context):  # Can be done with a sexy decorator later: TO BE IMPLEMENTED!!!
    return int(context.author.id) == int(self.client.ADMIN_ID)


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

        self.wrist = {}  # Used for the wrist exercises when users require them. We do not want this to be saved.

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
        await self.wrist_loop()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None \
                and message.author != self.client.user\
                and message.content[0] not in self.client.BOT_PREFIX:  # On PM (sometimes called DM) only
            await message.channel.send(WHITEMAGE_BRIEF)
        elif message.author != self.client.user \
                and message.content[0] not in self.client.BOT_PREFIX \
                and self.client.user.mentioned_in(message):
            await message.channel.send(WHITEMAGE_BRIEF)

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
                      aliases=['wrist_image', 'wrist-image', 'wristsimage', 'wrists_image', 'wrists-image'],
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
                      aliases=['wrist_video', 'wrist-video', 'wristsvideo', 'wrists_video', 'wrists-video'],
                      brief="Video of Dr. Levi's hand and wrist exercises.",
                      description="Provides you with the link to the video of the hand and wrist exercises recommended "
                                  "by Dr. Levi.")
    async def wrist_video(self, context):
        await context.send("Here's the video of hand and wrist exercises recommended by Dr. Levi (provided below).\n"
                           "When you start playing a game, use *?start* to have me ping you with a PM at specific "
                           "time intervals to remind you to do the different wrist exercises in this video,\nusing the "
                           "recommended time intervals for each different exercise.\n"
                           "https://www.youtube.com/watch?v=EiRC80FJbHU\n")

    @commands.command(name='thumb',
                      aliases=['thumbs'])
    async def thumb(self, context):
        await context.send("Here's the timestamp for the finger exercises (especially thumb exercises) "
                           "in Dr. Levi's video.\n"
                           "Starts at 2:01, ends at 2:54 (the video should automatically start at 2:01).\n"
                           "https://youtu.be/EiRC80FJbHU?t=121")

    @commands.command(name='start')
    async def start(self, context):
        if context.author.id in self.wrist.keys():
            await context.send('You already have a running instance of wrist exercise pings.\n'
                               'Please use *?stop* to stop my pings before trying to use *?start* again.\n'
                               'Do note that this will, however, start over from the beginning.')
        if context.guild is not None:
            await context.send("Understood, {0.mention}.\n"
                               "You requested me to ping you with wrist exercises at recommended time intervals.\n"
                               "More information has been directly sent to you via Personal Message.\n"
                               "You can stop this anytime by using the *?stop* command. "
                               "Use it when you finish playing, or my pings will continue for as long as I'm up.\n"
                               "[Note : You can also use the *?start* command by directly messaging me with it. "
                               "The above message will then not be displayed]".format(context.author))
        await context.author.send("Hello, {0.mention}.\n"
                                  "It seems you have started gaming (or coding) and requested pings "
                                  "for wrist exercises.\n"
                                  "I will ping you every hour, as well as every 1h30, 2h30 and 3h30 with specific "
                                  "exercises.\n"
                                  "We're following the plan from the video available with the *?wristvideo* command. "
                                  "You can see a summary of said video with *?wristimage*.\n"
                                  "I recommend checking the video out if this is your first time using this "
                                  "function of mine.\n"
                                  "See you in an hour!".format(context.author))

        launch_time = time.time()
        self.wrist[context.author.id] = {
            'program_start':launch_time,
            'last_100': launch_time,
            'last_130': launch_time,
            'last_230': launch_time,
            'last_330': launch_time,    # last_330 also marks the start of a cycle
            'last_ping': launch_time
        }

    async def wrist_loop(self):
        for user_id in self.wrist:

            curtime = time.time()
            also = False if curtime - self.wrist[user_id]['last_ping'] >= ALSO_MARGIN else True

            if curtime - self.wrist[user_id]['last_330'] >= HOUR330:
                usr = await self.client.fetch_user(user_id)
                msg = usr.mention + ", " + PASSED_330 + EXO_330
                also = True
                self.wrist[user_id]['last_330'] = curtime
                self.wrist[user_id]['last_ping'] = curtime
                await usr.send(msg)

            if curtime - self.wrist[user_id]['last_230'] >= HOUR230:
                usr = await self.client.fetch_user(user_id)
                if not also:
                    msg = usr.mention + ", " + PASSED_230 + EXO_230
                    also = True
                else:
                    msg = ALSO + PASSED_230 + EXO_230
                self.wrist[user_id]['last_230'] = curtime
                self.wrist[user_id]['last_ping'] = curtime
                await usr.send(msg)

            if curtime - self.wrist[user_id]['last_130'] >= HOUR130:
                usr = await self.client.fetch_user(user_id)
                if not also:
                    msg = usr.mention + ", " + PASSED_130 + EXO_130
                    also = True
                else:
                    msg = ALSO + PASSED_130 + EXO_130
                self.wrist[user_id]['last_130'] = curtime
                self.wrist[user_id]['last_ping'] = curtime
                await usr.send(msg)

            if curtime - self.wrist[user_id]['last_100'] >= HOUR100:
                usr = await self.client.fetch_user(user_id)
                if not also:
                    msg = usr.mention + ", " + PASSED_100 + EXO_100
                    also = True
                else:
                    msg = ALSO + PASSED_100 + EXO_100
                self.wrist[user_id]['last_100'] = curtime
                self.wrist[user_id]['last_ping'] = curtime
                await usr.send(msg)

        await asyncio.sleep(LOOP_CHECK_TIME)
        await asyncio.ensure_future(self.wrist_loop())

    #Loop : curtimme = time.time().
    # for every user for every truc check et envoyer
    # check last 330->230->130->100

    @commands.command(name='stop')
    async def stop(self, context):
        if context.author.id in self.wrist:
            curtime = time.time()
            total_time_minutes = int((curtime - self.wrist[context.author.id]['program_start']) / 60)
            cycle_time = curtime - self.wrist[context.author.id]['last_330']  # last_330 is the beginning of a cycle
            await context.author.send("{0.mention}, you have decided to stop the wrist exercise pings "
                                      "after {1} minute(s).\n"
                                      "I will thus stop pinging you from now.\n"
                                      "Feel free to use the wrist exercise ping service again with *?start*.\n"
                                      "Have a great day!"
                                      .format(context.author, str(total_time_minutes)))
            if HOUR130 <= cycle_time < HOUR230:
                usr = await self.client.fetch_user(context.author.id)
                await usr.send("Sorry to bother you with this, but you have been playing more than an hour and a half "
                               "since the beginning of the last exercise cycle, "
                               "and have some exercises left in the queue which could be useful to you.\n"
                               "If you find the time, feel free to do these before starting other activities.\n"
                               "I will forward you the remaining exercises (normally sent to you after "
                               "2 and a half and 3 and a half hours, respectively).")
                await usr.send(DONTFORGET + EXO_230)
                await usr.send(DONTFORGET + EXO_330)
            elif HOUR230 <= cycle_time < HOUR330:
                usr = await self.client.fetch_user(context.author.id)
                await usr.send("Sorry to bother you with this, but you have been playing more than two and a half hours"
                               " since the beginning of the last exercise cycle, "
                               "and have an exercise left in the queue which could be useful to you.\n"
                               "If you find the time, feel free to do this one before starting other activities.\n"
                               "I will forward you the remaining exercise (normally sent to you after "
                               "3 and a half hours).")
                await usr.send(DONTFORGET + EXO_330)
            del self.wrist[context.author.id]
        else:
            await context.author.send("You are currently not registered for wrist exercise pings.\n"
                                      "There is no need to use *?stop*.")

    @commands.command(name='whowrist',
                      hidden=True)
    async def whowrist(self, context):
        if _is_admin(self, context):
            users = [await self.client.fetch_user(userid) for userid in self.wrist]
            admin = await self.client.fetch_user(self.client.ADMIN_ID)
            await admin.send("Currently requesting for wrist exercises:\n")
            usernames = [user.mention for user in users]
            if not usernames:
                await admin.send("No one")
            else:
                await admin.send(';'.join(usernames))

    @commands.command(nam='adminhelp',
                      hidden=True,
                      aliases=['admincommands'])
    async def adminhelp(self, context):
        if _is_admin(self, context):
            admin_cmds = ['whowrist']
            admin = await self.client.fetch_user(self.client.ADMIN_ID)
            await admin.send("Current admin commands on whitemage are:\n"+';'.join(admin_cmds))


def setup(client):
    client.add_cog(WhiteMage(client))
