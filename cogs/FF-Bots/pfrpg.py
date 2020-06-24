import json
import discord
from os.path import join
from discord.ext import commands

from utils import is_admin, send_temporary_msg

PFRPG_DATA_FILE = join("data", "info", "pfrpg.json")
ACTIVE_QUEST_CHANNELS = "active_quest_channels"
QUEST_CHANNELS = "quest_channels"
DISCORD_CHARACTER_LIMIT = 2000

data_template = {
    ACTIVE_QUEST_CHANNELS: {},
    QUEST_CHANNELS: {
        "channel_id": {
            "players": {
                # "Catherina": {
                #     "icon": "",
                #     "custom_icon": True
                # }
            },
            "quests": {
                # 0: {  # level
                #     1: {  # quest number/id
                #         "quest_object"
                #     }
                # }
            }
        }
    }
}

# Also keep track of PLAYERS with CUSTOM EMOJIS to put instead of NAMES in QUEST_COMPLETED and QUEST_ACCEPTED
# INSIDE QUEST_CHANNEL!

quest_template = {
    "id": "lvl.zfill(2)+quest_number.zfill(2) = 0001",  # lvl 0, quest number 1
    "message_id": 0,
    "title": 0,
    "reward_xp": 0,
    "reward_gold": 0,
    "reward_item": None,
    "reward_title": None,
    "reward_extra": None,  # genre "si mari laissé en vie, blah blah")
    "client": 0,
    "location": 0,
    "text": 0,
    "accepted": [],
    "succeeded": [],
    "extra": None
}


#######################################################################################################################
#                                      ---  'Pathfinder RPG' cog  ---                                                 #
#                     Cog containing commands for a specific tabletop RPG (quest list, etc.)                          #
#######################################################################################################################
class PathfinderRPG(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Loading information on PFRPG from previous iterations
        try:
            with open(PFRPG_DATA_FILE, 'r') as f:
                self.data = json.load(f)
                print("> Successfully loaded data from {}".format(PFRPG_DATA_FILE))
        except IOError:
            print("/!\\ PFRPG DATA NOT FOUND AT {}, DEFAULTING TO BLANK VALUES!"
                  .format(PFRPG_DATA_FILE))
            self.data = {
                ACTIVE_QUEST_CHANNELS: {},
                QUEST_CHANNELS: {}
            }
            with open(PFRPG_DATA_FILE, 'w') as f:
                json.dump(self.data, f)

    # Save function to keep information about RSSManager between instances
    async def save_data(self):
        with open(PFRPG_DATA_FILE, 'w') as f:
            json.dump(self.data, f)

    # Load function loading up information about previous instances of RSSManager
    async def load_data(self):
        with open(PFRPG_DATA_FILE, 'r') as f:
            self.data = json.load(f)
        # A json to store order of messages
        # dictionary of questname to message id
    
    #  I really need something to list admin commands

    @commands.command(name='pfrpg_set_quest_channel',
                      hidden=True)
    async def pfrpg_set_quest_channel(self, context):
        if not is_admin(context):
            await context.send("Only the adminstrator can use the *pfrpg_set_quest_channel* function")
            return

        cur_channel = context.channel.id

        if not cur_channel:
            await context.send("Private message channel cannot be set as a PFRPG quest channel.")
            return

        if cur_channel in self.data[ACTIVE_QUEST_CHANNELS]:
            if self.data[ACTIVE_QUEST_CHANNELS][cur_channel]:
                await send_temporary_msg(context, "This channel has already been set up as a PFRPG quest channel.")
                await context.message.delete()
                return
            else:
                await send_temporary_msg(context, "Previously active PFRPG quest channel found. "
                                                  "Reviving previous configurations.")
        else:
            self.data[QUEST_CHANNELS][cur_channel] = {}
            await send_temporary_msg(context, "Current channel successfully set as a PFRPG quest channel.")

        self.data[ACTIVE_QUEST_CHANNELS][cur_channel] = True
        await context.message.delete()
        await self.save_data()

    @commands.command(name='pfrpg_unset_quest_channel',
                      hidden=True)
    async def pfrpg_unset_quest_channel(self, context):
        if not is_admin(context):
            await context.send("Only the adminstrator can use the *pfrpg_unset_quest_channel* function")
            return

        cur_channel = context.channel.id

        if cur_channel not in self.data[ACTIVE_QUEST_CHANNELS] or not self.data[ACTIVE_QUEST_CHANNELS][cur_channel]:
            await send_temporary_msg(context, "Current channel is not an active PFRPG quest channel: "
                                              "no need to unset.")
            await context.message.delete()
            return

        self.data[ACTIVE_QUEST_CHANNELS][cur_channel] = False
        await send_temporary_msg(context, "Current channel successfully unset: no longer a PFRPG quest channel.")
        await context.message.delete()
        await self.save_data()

    @commands.command(name='pfrpg_delete_quest_channel_data_iamsure',
                      hidden=True)
    async def pfrpg_delete_quest_channel_data_iamsure(self, context):
        if not is_admin(context):
            await context.send("Only the adminstrator can use the *pfrpg_delete_quest_channel_data_iamsure* function")
            return

        cur_channel = context.channel.id

        if cur_channel not in self.data[ACTIVE_QUEST_CHANNELS]:
            await context.send("Why would you want to delete quest channel data of a channel that isn't even one?")
            return

        del self.data[ACTIVE_QUEST_CHANNELS][cur_channel]

        if cur_channel not in self.data[QUEST_CHANNELS]:
            await context.send("Weirdly enough, this channel was listed as a PFRPG quest channel "
                               "but didn't have quest data.")
            return

        del self.data[QUEST_CHANNELS][cur_channel]

        await context.send("Current channel's quest data successfully deleted.")
        await self.save_data()

    @commands.command()
    async def add_quest(self, context):
        pass

    @commands.command()
    async def edit_quest(self, context):
        pass

    @commands.command()
    async def delete_quest(self, context):
        pass

    @commands.command()
    async def complete_quest(self, context):
        pass

    @commands.command()
    async def add_player(self, context):
        pass

    @commands.command()
    async def edit_player(self, context):
        pass

    @commands.command()
    async def delete_player(self, context):
        pass

    # Event listener for messages sent to Moogle
    @commands.Cog.listener()
    async def on_message(self, message):
        pass


def setup(client):
    client.add_cog(PathfinderRPG(client))
