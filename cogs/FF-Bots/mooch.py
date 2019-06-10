from discord.ext import commands
from utils import is_admin
from utils import fetch_admin
import datetime
import asyncio
import random

#######################################################################################################################
#                                   Setting up our constants for mooch                                                #
#######################################################################################################################

# Every variable or function containing 'mooch' is related to a function I just use to periodically send love messages
# to my girlfriend. Disregard all of those.

# Dual use: filename then id
MOOCH_ID = "data/keys/mooch.key"
with open(MOOCH_ID, 'r') as f:
    MOOCH_ID = f.readline()
MAX_MOOCH = 3
HOURS_3 = 10800
MOOCH_FILE = 'data/info/moochreplies'
possible_moochy = [line.rstrip('\r\n')
                       .replace('\xc3\xa0', 'à')
                       .replace('\xc3\xa8', 'è')
                       .replace('\xc3\xa9', 'é')
                       .replace('\xc3\xaa', 'ê')
                       .replace('\\n', '\n')
                   for line in open(MOOCH_FILE)]

#######################################################################################################################
#                                          ---  'Mooch' cog  ---                                                      #
#                                   Cog containing moochypooch commands                                               #
#######################################################################################################################
class Mooch(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mooch = False
        self.mooch_counter = 0
        self.today = datetime.datetime.now().day

    # Event listener for boot-up:
    # In this cog, it is only used to launch the main loop for my 'mooch' function. Disregard this.
    @commands.Cog.listener()
    async def on_ready(self):
        await self.mooch_loop()

    # These two following functions periodically send messages to my girlfriend. Disregards these.
    # The first one (command) deactivates or activates the function,
    # the second one is a loop activating every few hours.
    @commands.command(name='mooch',
                      hidden=True)
    async def mooch(self, context):
        if is_admin(context):
            self.mooch = not self.mooch
            admin = await fetch_admin(self.client)
            await admin.send("Current mooch value: {}".format(self.mooch))

    # How it works :
    # if mooch is authorized (self.mooch = True),
    # every 3 hours, has a 1/3 chance of sending a random message among
    # a choice of messages (from data/info/moochreplies) to the user with id MOOCH_ID.
    # This can only happen 3 times per day, so as to avoid spam.
    async def mooch_loop(self):
        if self.mooch:
            rand = random.randint(0, 2)
            if not rand and self.mooch_counter < MAX_MOOCH:
                mooch = await self.client.fetch_user(MOOCH_ID)
                mooch.send(random.choice(possible_moochy))
                self.mooch_counter += 1

        now = datetime.datetime.now().day
        if now != self.today:
            self.today = now
            self.mooch_counter = 0

        await asyncio.sleep(HOURS_3)
        await asyncio.ensure_future(self.mooch_loop())


def setup(client):
    client.add_cog(Mooch(client))
