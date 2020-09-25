import json
import asyncio
from os.path import join
from datetime import datetime
from utils import send_msg_to_all_channels
from discord.ext.commands import Cog, command, check_any, has_permissions, is_owner

INKTOBER_DATA_FILE = join("data", "info", "inktober.json")
INKTOBER_SLEEPTIME = 21600  # 6 hours in seconds
OCTOBER = 10
START_DAY = "1"
PAINTBRUSH_MESSAGE = ":paintbrush: :art: :art: :art: :art: :art: :art: :art: :art: :art: :art: :art: :paintbrush:\n"
START_MESSAGE = "Ladies and gentlemen, Inktober is starting today!\n" \
                "Feel free to post your drawings or doodles in this channel so we enjoy your art! :)\n"
TODAY_MESSAGE = "--- Today's Inktober challenge word is: `{}` ---\n" \
                "Draw or doodle something and share it with us! :)\n"


#######################################################################################################################
#                                         ---  'Inktober' cog  ---                                                    #
#                                   Cog managing Inktober channel information                                         #
#######################################################################################################################
class Inktober(Cog):
    def __init__(self, client):
        now = datetime.utcnow()
        if now.month not in (9, 10):
            try:
                self.client.unload_extension(join(self.client.COGS_FOLDER, "inktober"))
                print("> The month isn't September or October: unloading Inktober cog")
            except Exception as error:
                print(f'> Extension \'Inktober\' cannot be unloaded. [Reason: {error}]')

        # Loading Inktober information
        try:
            with open(INKTOBER_DATA_FILE, 'r') as f:
                self.inktober = json.load(f)
                print(f"> Successfully loaded data from {INKTOBER_DATA_FILE}")
        except IOError:
            try:
                self.client.unload_extension(join(self.client.COGS_FOLDER, "inktober"))
                print("> No inktober.json data file found: unloading Inktober cog")
            except Exception as error:
                print(f'> Extension \'Inktober\' cannot be unloaded. [Reason: {error}]')

        self.client = client
        if "channels" not in self.inktober:
            # sets are faster to see if a channel is contained in the set,
            # but lists are faster for iterating, which we will do more often.
            # So this will be a list.
            self.inktober["channels"] = []

    async def save_data(self):
        with open(INKTOBER_DATA_FILE, 'w') as f:
            json.dump(self.inktober, f, indent=4)

    async def load_data(self):
        with open(INKTOBER_DATA_FILE, 'r') as f:
            self.inktober = json.load(f)

    @Cog.listener()
    async def on_ready(self):
        await self.inktober_loop()

    async def inktober_loop(self):
        now = datetime.utcnow()

        year = str(now.year)
        day = str(now.day)

        if now.month == OCTOBER and year in self.inktober and day in self.inktober[year]:
            if day == START_DAY:
                await send_msg_to_all_channels(self.client, self.inktober['channels'], START_MESSAGE)
            await send_msg_to_all_channels(self.client, self.inktober['channels'],
                                           PAINTBRUSH_MESSAGE +
                                           TODAY_MESSAGE.format(self.inktober[year][day]) +
                                           PAINTBRUSH_MESSAGE)

        await asyncio.sleep(INKTOBER_SLEEPTIME)
        await asyncio.ensure_future(self.inktober_loop())

    # Sets a channel as Inktober channel
    @check_any(has_permissions(administrator=True), is_owner())
    @command(name='inktober', hidden=True)
    async def inktober(self, context):
        cur_channel = context.channel.id

        if context.guild is None:
            cur_channel = context.author.id

        if cur_channel in self.inktober['channels']:
            self.inktober['channels'].remove(cur_channel)
            await context.send("This channel is no longer an Inktober channel "
                               "and will stop receiving Inktober-related messages.")
        else:
            self.inktober['channels'].append(cur_channel)
            await context.send("This channel is now an Inktober channel "
                               "and will receive Inktober-related messages.")

        await self.save_data()


def setup(client):
    client.add_cog(Inktober(client))
