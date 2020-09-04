import json
import asyncio
from time import time
from os.path import dirname
from discord import Activity, ActivityType
from discord.ext.commands import Cog, command, is_owner


#######################################################################################################################
#                                 Setting up our constants for whitemage                                              #
#######################################################################################################################

# > Whitemage's basic info
from utils import get_hidden_commands

WHITEMAGE_DATA_FILE = 'data/info/whitemage.json'
WHITEMAGE_BRIEF = "\n:flag_us: Hi, I'm WhiteMage, a gentle nurse bot designed to help you with " \
                  "your general health needs. I reply to commands starting with '?'.\n"\
                  "You can get all of my commands by using *?help*, which I advise you to do."\
                  "\n:flag_fr: Bonjour, je suis WhiteMage, le gentil bot infirmier conçu pour vous"\
                  " aider quant à vos besoins de santé. Je réponds aux commandes commençant "\
                  "par '?'.\n"\
                  "Vous pouvez utiliser *?help* pour connaitre l'entiereté de mes commandes, "\
                  "ce que je vous recommande de faire."
WHITEMAGE_UPDATE_MSG = ":flag_us: I seem to have learned a new spell! / "\
                       ":flag_fr: On dirait bien que j'ai appris un nouveau sort!"
# Thanks to Nathan (Kyouma) for this cool update message!

# >  Necessary constants for the wrist exercise pings
# Loop timers
LOOP_CHECK_TIME = 60                                # Timer to check the loop every minute
ALSO_MARGIN = (2 * LOOP_CHECK_TIME) + 1             # Error margin for small discrepancies in different exercise pings

# URLs for images
WRIST_100 = 'https://imgur.com/Slnwo1y'
WRIST_130 = 'https://imgur.com/8bdFs07'
WRIST_230 = 'https://imgur.com/UbYhjhm'
WRIST_330 = 'https://imgur.com/PgrSu3b'

# Time in seconds before exercise pings (respectively 1h, 1h30, 2h30 and 3h30)
HOUR100 = 3600
HOUR130 = 5400
HOUR230 = 9000
HOUR330 = 12600

# Exercise ping messages
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


#######################################################################################################################
#                                         ---  'Whitemage' cog  ---                                                   #
#                             Main (and only) cog for our Nurse bot, WhiteMage                                        #
#######################################################################################################################
class WhiteMage(Cog):
    def __init__(self, client):
        # Passing the bot's (AKA client's) information
        self.client = client

        # Loading information on Whitemage from previous iterations
        try:
            with open(WHITEMAGE_DATA_FILE, 'r') as f:
                self.info = json.load(f)
                print("> Successfully loaded data from {}".format(WHITEMAGE_DATA_FILE))
        except IOError:
            print("/!\\ WHITEMAGE DATA (INFO) NOT FOUND AT {}, DEFAULTING TO BLANK VALUES!".format(WHITEMAGE_DATA_FILE))
            self.info = {
                'known_guilds': [],
                'latest_update_time': time()
            }

        # Initializing the dictionary keeping information on users having requested exercise pings.
        # Since we do not want this to be saved between instances of the bot, we separate it from the data file.
        self.wrist = {}

    # Save function to keep information about Whitemage between instances
    async def save_whitemage_data(self):
        with open(WHITEMAGE_DATA_FILE, 'w') as f:
            json.dump(self.info, f)

    # Load function loading up information about previous instances of Whitemage
    async def load_whitemage_data(self):
        with open(WHITEMAGE_DATA_FILE, 'r') as f:
            self.info = json.load(f)

    ###################################################################################################################
    #                                              Event handlers                                                     #
    ###################################################################################################################

    # Event handler for initial boot up of the bot. This could be done in __init__ as well, but is way clearer this way.
    @Cog.listener()
    async def on_ready(self):
        # Changing the bot's activity feed
        await self.client.change_presence(activity=Activity(name="use ?help",
                                                            type=ActivityType['listening']))

        # Function removed entirely. May come back later on, but putting it in "on_ready" isn't optimal.

        # whitemage_intro_msg = ":flag_us: Allow me to introduce myself.\nI am WhiteMage, " \
        #                       "a gentle bot designed to help you with your general health needs.\n" \
        #                       'I reply to commands starting with the \'?\' sign. ' \
        #                       'To get all of my possible commands, just type \'?help\' ' \
        #                       "in any chatroom or via PM.\n" \
        #                       'I generally work by pinging you via Personal Messages (PMs). ' \
        #                       "Please treat me kindly.\n" \
        #                       'PS : If you have any ideas about some improvements for this bot, ' \
        #                       'please send them ' \
        #                       'to my maker, {0.mention}.' \
        #                       "\n\n" \
        #                       ":flag_fr: Permettez-moi de me présenter.\n Je suis WhiteMage, " \
        #                       'un gentil bot infirmier conçu pour vous aider quant à vos ' \
        #                       "besoins de santé.\n" \
        #                       'Je réponds aux commandes commençant par le caractère \'?\'. ' \
        #                       'Pour connaitre l\'entièreté de mes commandes, tapez \'?help\' dans ' \
        #                       "n\'importe quel salon de chat ou via MP.\n" \
        #                       'En général, je compte vous ping via Message Personnel (MP). ' \
        #                       "Soyez gentil avec moi.\n" \
        #                       'PS : Si vous avez des idées d\'améliorations pour ce bot, ' \
        #                       'veuillez les envoyer à mon' \
        #                       'créateur, {0.mention}.'.format(self.client.owner)

        # Function removed entirely. May come back later on, but putting it in "on_ready" isn't optimal.

        # # Greeting new guilds Whitemage has been introduced in, and informing already known guilds that an update
        # # has been done (the update message is limited to once every 24 hours to avoid spam when mass-updating).
        # # Note : 'Discord guild' is a synonym for a 'Discord server'.
        # #         We chose to keep 'guild' for consistency with the API.
        # for guild in self.client.guilds:
        #     # Introducing itself to a new guild
        #     if guild.id not in self.info.setdefault('known_guilds', []):
        #         self.info['known_guilds'].append(guild.id)
        #         await guild.system_channel.send(whitemage_intro_msg)
        #
        #     # The following code has been temporarily removed because of Heroku's dumb tendency
        #     # to reboot every script after 24 hours. This message spammed the server at 24h intervals, so
        #     # this function had to be removed.
        #     # Instead, only the admin will get a message (for debugging purposes)
        #
        #     # # Informing known guilds about an update
        #     # else:
        #     #     if time() - self.info.setdefault('latest_update_time', time()) > 86401:
        #     #         # 86400 is the number of seconds in a day.
        #     #         # This is so the update message only appears once per day at best.
        #     #         self.info['latest_update_time'] = time()
        #     #         await guild.system_channel.send(WHITEMAGE_UPDATE_MSG)

        # Saving new known guilds data
        await self.save_whitemage_data()

        # Initializing the loop checking for users requiring wrist exercise pings.
        # The loop will only really start doing things when a user uses the command ?start.
        # The definition of wrist_loop() is provided below, between the ?start and ?stop command.
        await self.wrist_loop()

    # Event listener for messages sent to Whitemage
    @Cog.listener()
    async def on_message(self, message):
        # IF we have a DM/PM (Personal Message) sent directly to Whitemage without being a command :
        # - we send information on how to use Whitemage to the user
        if message.guild is None \
                and message.author != self.client.user\
                and message.content[0] not in self.client.BOT_PREFIX:
            await message.channel.send(WHITEMAGE_BRIEF)

        # If we have a mention to @WhiteMage on any channel :
        # - we send information on how to use Whitemage to the user (on the context channel, not via PM/DM)
        elif message.author != self.client.user \
                and message.content[0] not in self.client.BOT_PREFIX \
                and self.client.user.mentioned_in(message):
            await message.channel.send(WHITEMAGE_BRIEF)

    ###################################################################################################################
    #                                                 Commands                                                        #
    ###################################################################################################################

    # The following commands' description are provided in the decorator and are pretty self-explanatory.
    # No comments will be written on simpler functions.

    @command(name='wrist',
             aliases=['wrists'],
             brief='Info on commands related to wrists',
             description='You can also use this command with the aliases below:',
             help='Provides information relative to WhiteMage\'s commands related to wrist exercises')
    async def wrist(self, context):
        await context.send("I can provide you with either a video or summary image of wrist exercises for Gamers.\n"
                           "The commands *?wristimage* and *?wristvideo* (and their respective variants) "
                           "provide you with the respective media.\n"
                           "To get all my commands, use *?help*.\n"
                           "I can also ping you for these very same wrist exercises via *?start* (temporary name), "
                           "which you need to use when you start playing a game.\n"
                           "**Please take care of your wrists!**")

    @command(name='wristimage',
             aliases=['wrist_image', 'wrist-image', 'wristsimage', 'wrists_image', 'wrists-image'],
             brief="Summary image of Dr. Levi's wrist exercises.",
             description='You can also use this command with the aliases below:',
             help="Provides an image summarizing the exercises recommended by Dr. Levi in his video "
                  "(available with the '?wristvideo' commands and its variants)")
    async def wrist_image(self, context):
        await context.send("Here's a summary of wrist exercises recommended by Dr. Levi in his Youtube video "
                           "(provided below).\n"
                           "When you start playing a game, use *?start* to have me ping you with a PM at specific "
                           "time intervals to remind you to do the different wrist exercises on the image,\nusing the "
                           "recommended time intervals for each different exercise.\n"
                           "https://imgur.com/5vktp17\n")

    @command(name='wristvideo',
             aliases=['wrist_video', 'wrist-video', 'wristsvideo', 'wrists_video', 'wrists-video'],
             brief="Video of Dr. Levi's hand and wrist exercises.",
             description='You can also use this command with the aliases below:',
             help="Provides you with the link to the video of the hand and wrist exercises recommended "
                   "by Dr. Levi.")
    async def wrist_video(self, context):
        await context.send("Here's the video of hand and wrist exercises recommended by Dr. Levi (provided below).\n"
                           "When you start playing a game, use *?start* to have me ping you with a PM at specific "
                           "time intervals to remind you to do the different wrist exercises in this video,\nusing the "
                           "recommended time intervals for each different exercise.\n"
                           "https://www.youtube.com/watch?v=EiRC80FJbHU\n")

    @command(name='thumb',
             aliases=['thumbs'],
             brief='Information and timestamp for thumb and finger exercises',
             description='You can also use this command with the aliases below:',
             help='Provides you with the link to the video about hand and wrist exercises with a timestamp, '
                  'starting at the part where the thumb/finger-related exercises start.')
    async def thumb(self, context):
        await context.send("Here's the timestamp for the finger exercises (especially thumb exercises) "
                           "in Dr. Levi's video.\n"
                           "Starts at 2:01, ends at 2:54 (the video should automatically start at 2:01).\n"
                           "https://youtu.be/EiRC80FJbHU?t=121")

    # This command is the main reason for the creation of the bot.
    # ?start is to be used when you start gaming and want Whitemage to ping you with wrist/hand exercises to keep
    # you healthy and avoid injuries and future carpal tunnel syndromes.
    @command(name='start',
             aliases=['wriststart', 'pingstart', 'gamestart'],
             brief='Use this when you start gaming and want wrist exercise pings',
             description='You can also use this command with the aliases below:',
             help='Registers you for wrist exercise pings sent by DM.\n'
                  'This command is to be used when you start a game of something that requires \n'
                  'effort from your hands and wrist, like League of Legends, Counter Strike, Warframe, etc.,\n'
                  ' and will send you pings for exercises every hour, hour and a half, two hours and a half '
                  'and three hours and a half.'
             )
    async def start(self, context):
        # If the user is already registered for wrist exercise pings
        if context.author.id in self.wrist.keys():
            await context.send('You already have a running instance of wrist exercise pings.\n'
                               'Please use *?stop* to stop my pings before trying to use *?start* again.\n'
                               'Do note that this will, however, start over from the beginning.')

        # If ?start isn't used in a DM to Whitemage
        if context.guild is not None:
            await context.send("Understood, {0.mention}.\n"
                               "You requested me to ping you with wrist exercises at recommended time intervals.\n"
                               "More information has been directly sent to you via Personal Message.\n"
                               "You can stop this anytime by using the *?stop* command. "
                               "Use it when you finish playing, or my pings will continue for as long as I'm up.\n"
                               "[Note : You can also use the *?start* command by directly messaging me with it. "
                               "The above message will then not be displayed]".format(context.author))

        # Send a DM to inform the user that pings will be sent to him.
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

        # Register info necessary for pings in self.wrist
        launch_time = time()
        self.wrist[context.author.id] = {
            'program_start': launch_time,                   # Time of the start of pings (when ?start was called)
            'last_ping': launch_time,                       # Time of the last ping done to user
            'last_100': launch_time,                        # Time of the last 1 hour ping sent to user
            'last_130': launch_time,                        # Time of the last 1h30 ping sent to user
            'last_230': launch_time,                        # Time of the last 2h30 ping sent to user
            'last_330': launch_time                         # Time of the last 3h30 ping sent to user
        }                                                   # Note : last_330 also marks the start of a cycle

    # Function managing the main loop, checking for users to ping and pinging them with the right exercises.
    # The message is constructed from the global constants defined at the start of this file.
    # The first ping will mention the user (with @name_of_the_user), using a discord mention ping.
    # If several pings are to be made in a row or in the same ALSO_MARGIN (see start of file) period of time,
    # subsequent pings will not mention the user, but use the message provided in ALSO to start their message.
    #
    # The time check for pings works by updating the last ping time for the adequate variable in self.wrist[user_id].
    async def wrist_loop(self):
        for user_id in self.wrist:

            curtime = time()
            also = False if curtime - self.wrist[user_id]['last_ping'] >= ALSO_MARGIN else True

            if curtime - self.wrist[user_id]['last_330'] >= HOUR330:
                # Note: fetching users and using them (like with usr.mention) must be done separately, or else it fails.
                usr = await self.client.fetch_user(user_id)
                # If a 3h30 ping happens, it'll always be the first one in priority order. No need to check for "Also".
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

        # Sleep for LOOP_CHECK_TIME seconds
        await asyncio.sleep(LOOP_CHECK_TIME)

        # Launch the next iteration of the loop, indefinitely
        await asyncio.ensure_future(self.wrist_loop())

    # This command removes you from the list of users to ping with exercises.
    # If a certain amount of time (over 1h30) has passed since you called ?start (i.e. since you started gaming),
    # the bot also dumps the remaining exercises and advises you to do them as well (without being pushy).
    @command(name='stop')
    async def stop(self, context):
        if context.author.id in self.wrist:

            curtime = time()
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

            # Delete user from the dictionary containing the users requesting pings
            del self.wrist[context.author.id]

        # If the user never even used ?start to begin with.
        else:
            await context.author.send("You are currently not registered for wrist exercise pings.\n"
                                      "There is no need to use *?stop*.")

    ###################################################################################################################
    #                                              Admin commands                                                     #
    ###################################################################################################################

    # A few commands I don't want every user to abuse, but can be useful if someone forgot to turn off the bot
    # and is using computation power for hours and hours.
    @is_owner()
    @command(nam='adminhelp',
             hidden=True,
             aliases=['admincommands'])
    async def adminhelp(self, context):
        await get_hidden_commands(self.client, dirname(__file__))

    # This command informs you on who is currently registered for wrist exercise pings, i.e. which user is in self.wrist
    @is_owner()
    @command(name='whowrist',
             hidden=True)
    async def whowrist(self, context):
        # Fetch user object of admin (to allow a DM/PM)
        owner = self.client.owner

        # Note : fetching users and using them (like with user.mention) must be done separately, or else it fails.
        users = [await self.client.fetch_user(userid) for userid in self.wrist]
        usernames = [user.mention for user in users]

        await owner.send("Currently requesting for wrist exercises:\n")

        # If no id is present in the list
        if not usernames:
            await owner.send("No one")
        else:
            await owner.send(';'.join(usernames))


def setup(client):
    client.add_cog(WhiteMage(client))
