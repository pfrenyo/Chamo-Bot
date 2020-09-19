import random
import asyncio
import datetime
from os.path import join
from discord.ext.commands import Cog, command, check_any, is_owner, has_permissions


#######################################################################################################################
#                                   Setting up our constants for mooch                                                #
#######################################################################################################################

# Every variable or function containing 'mooch' is related to a function I just use to periodically send love messages
# to my girlfriend. Disregard all of those.

# Dual use: filename then id
MOOCH_ID_FILE = join("data", "keys", "mooch.key")
MOOCH_FILE = join("data", "info", "moochreplies.txt")
MAX_MOOCH = 3
HOURS_3 = 10800
MIN_2 = 120
STARTUP_TIME = 30  # Time to avoid spamming Mooch at each boot. Use this time to use !mooch if you don't want to spam.


#######################################################################################################################
#                                          ---  'Mooch' cog  ---                                                      #
#                                   Cog containing moochypooch commands                                               #
#######################################################################################################################
class Mooch(Cog):
    def __init__(self, client):
        self.client = client
        self.mooch = False  # Default mooch value is False now
        self.mooch_counter = 0
        self.today = datetime.datetime.now().day
        # self.first = True

        try:
            with open(MOOCH_ID_FILE, 'r') as f:
                self.mooch_id = f.readline()
            with open(MOOCH_FILE, 'r') as f:
                self.possible_moochy = [line.rstrip('\r\n')
                                            .replace('\xc3\xa0', 'à')
                                            .replace('\xc3\xa8', 'è')
                                            .replace('\xc3\xa9', 'é')
                                            .replace('\xc3\xaa', 'ê')
                                            .replace('\\n', '\n')
                                        for line in f]
            print("> Mooch data found! Leaving cog up.")
        except IOError:
            try:
                self.client.unload_extension(join(self.client.COGS_FOLDER, "mooch"))
                print("> No mooch data found: unloading cog.")
            except Exception as error:
                print(f'> Extension \'Mooch\' cannot be unloaded. [Reason: {error}]')

    # Event listener for boot-up:
    # In this cog, it is only used to launch the main loop for my 'mooch' function. Disregard this.
    @Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(STARTUP_TIME)
        await self.mooch_loop()

    # Event listener for messages sent to Moogle, Mooch-related functions
    @Cog.listener()
    async def on_message(self, message):
        if message.guild is None \
                and int(message.author.id) == int(self.mooch_id) \
                and message.content[0] not in self.client.BOT_PREFIX:
            msg = random.choice(self.possible_moochy)
            await message.channel.send(msg)

    # These two following functions periodically send messages to my girlfriend. Disregards these.
    # The first one (command) deactivates or activates the function,
    # the second one is a loop activating every few hours.
    @is_owner()
    @command(name='mooch',
             hidden=True)
    async def mooch(self, context):
        self.mooch = not self.mooch
        owner = self.client.AppInfo.owner
        await owner.send("Current mooch value: {}".format(self.mooch))

    # How it works :
    # if mooch is authorized (self.mooch = True),
    # every 3 hours, has a 1/3 chance of sending a random message among
    # a choice of messages (from data/info/moochreplies.txt) to the user with id self.mooch_id.
    # This can only happen 3 times per day, so as to avoid spam.
    async def mooch_loop(self):
        if self.mooch:
            rand = random.randint(0, 2)
            if not rand and self.mooch_counter < MAX_MOOCH:
                owner = self.client.AppInfo.owner
                mooch = await self.client.fetch_user(self.mooch_id)
                msg = random.choice(self.possible_moochy)
                await mooch.send(msg)
                await owner.send("Message sent to Moochy. Content:\n{}".format(msg))
                self.mooch_counter += 1
                # if self.first:
                #     self.first = False

        now = datetime.datetime.now().day
        if now != self.today:
            self.today = now
            self.mooch_counter = 0

        # if self.first:
        #     await asyncio.sleep(MIN_2)
        # else:
        #     await asyncio.sleep(HOURS_3)
        await asyncio.sleep(HOURS_3)

        await asyncio.ensure_future(self.mooch_loop())

    # Get all the possible automated messages to Mooch
    @is_owner()
    @command(name='mooch_options',
             hidden=True)
    async def mooch_options(self, context):
        owner = self.client.AppInfo.owner
        await owner.send("Options for automatic replies to mooch:\n{}".format("\n".join(self.possible_moochy)))

    # Send a message to Mooch, using the Bot as sender.
    @is_owner()
    @command(name='mooch_message',
             hidden=True)
    async def mooch_message(self, context):
        # Parsing command content
        message = context.message.content.lstrip('!mooch_message').strip()
        if message.startswith('"') and message.endswith('"'):
            message = message.strip('" ')

        mooch = await self.client.fetch_user(self.mooch_id)
        await mooch.send(message)


def setup(client):
    client.add_cog(Mooch(client))
