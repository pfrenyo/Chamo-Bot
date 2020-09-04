import json
from os.path import join
from discord.ext.commands import Cog, command, check_any, is_owner, has_permissions

VOICE_MANAGER_DATA_FILE = join("data", "info", "voicemanager.json")
MUTABLE_CHANNELS = "mutable_channels"  # the right spelling is 'muteable' but in this case but whatever


#######################################################################################################################
#                                        ---  'Voice Manager' cog  ---                                                #
#                         Cog containing commands managing a select number of voice chats                             #
#######################################################################################################################
class VoiceManager(Cog):
    """
    Note to self:
    Maybe implement a backup unmute mechanism
    (store people muted, unmute them after like 5 minutes or something if they've been muted through here).
    They can unmute themselves anyway, though (through Moogle's !unmute in a a mutable channel).
    """
    def __init__(self, client):
        self.client = client

        # Loading information on Voice Manager from previous iterations
        try:
            with open(VOICE_MANAGER_DATA_FILE, 'r') as f:
                self.data = json.load(f)
                print("> Successfully loaded data from {}".format(VOICE_MANAGER_DATA_FILE))
        except IOError:
            print(f"/!\\ VOICE MANAGER DATA NOT FOUND AT {VOICE_MANAGER_DATA_FILE}, DEFAULTING TO BLANK VALUES!")
            self.data = {
                MUTABLE_CHANNELS: {}
            }
            with open(VOICE_MANAGER_DATA_FILE, 'w') as f:
                json.dump(self.data, f)

    # Save function to keep information about VoiceManager between instances
    async def save_data(self):
        with open(VOICE_MANAGER_DATA_FILE, 'w') as f:
            json.dump(self.data, f)

    # Load function loading up information about previous instances of VoiceManager
    async def load_data(self):
        with open(VOICE_MANAGER_DATA_FILE, 'r') as f:
            self.data = json.load(f)

    @check_any(has_permissions(administrator=True), is_owner())
    @command(name='set_mutable_channel',
             hidden=True)
    async def set_mutable_channel(self, context):
        if not context.author.voice or not context.author.voice.channel:
            await context.send("You are not connected to a voice channel")
            return

        cur_voice_channel = context.author.voice.channel
        cur_voice_channel_id = str(cur_voice_channel.id)  # stringified for clarity, it is apparently done by default

        if cur_voice_channel_id in self.data[MUTABLE_CHANNELS]:
            await context.send("This channel is already set as mutable. "
                               "If you want to unset this, use !unset_mutable_channel.")
            return

        await context.send(f"Voice channel '{cur_voice_channel.name}' has been set as a mutable channel.\n"
                           "Use !mute to mute all the people in that channel, if you're in it.\n"
                           "Use !unmute to unmute everyone.")
        self.data[MUTABLE_CHANNELS][cur_voice_channel_id] = False
        await self.save_data()

    @command(name='mute')
    async def mute(self, context):
        if not context.author.voice or not context.author.voice.channel:
            await context.send("You are not connected to a voice channel")
            return

        cur_voice_channel = context.author.voice.channel
        cur_voice_channel_id = str(cur_voice_channel.id)  # stringified for clarity, it is apparently done by default

        if cur_voice_channel_id not in self.data[MUTABLE_CHANNELS]:
            await context.send("This channel is not mutable.")
            return

        if self.data[MUTABLE_CHANNELS][cur_voice_channel_id]:
            await context.send("This channel is already muted, but whatever, let's mute again.")

        for member in cur_voice_channel.members:
            await member.edit(mute=True)

        self.data[MUTABLE_CHANNELS][cur_voice_channel_id] = True
        await context.send(f"Channel '{cur_voice_channel.name}' muted.")
        await self.save_data()

    @command(name='unmute')
    async def unmute(self, context):
        if not context.author.voice or not context.author.voice.channel:
            await context.send("You are not connected to a voice channel")
            return

        cur_voice_channel = context.author.voice.channel
        cur_voice_channel_id = str(cur_voice_channel.id)  # stringified for clarity, it is apparently done by default

        if cur_voice_channel_id not in self.data[MUTABLE_CHANNELS]:
            await context.send("This channel is not even mutable.")
            return

        if not self.data[MUTABLE_CHANNELS][cur_voice_channel_id]:
            await context.send("This channel is already unmuted, but whatever, LET THE PEOPLE SPEAK (again).")

        for member in cur_voice_channel.members:
            await member.edit(mute=False)

        self.data[MUTABLE_CHANNELS][cur_voice_channel_id] = False
        await context.send(f"Channel '{cur_voice_channel.name}' unmuted.")
        await self.save_data()

    @check_any(has_permissions(administrator=True), is_owner())
    @command(name='stfu',
             hidden=True)
    async def stfu(self, context):
        if not context.author.voice or not context.author.voice.channel:
            await context.send("You are not connected to a voice channel")
            return

        cur_voice_channel = context.author.voice.channel

        for member in cur_voice_channel.members:
            if member != context.author:
                await member.edit(mute=True)

        await context.send(f"Everyone besides the admin has been muted on '{cur_voice_channel.name}'.")
        await self.save_data()

    @check_any(has_permissions(administrator=True), is_owner())
    @command(name='unstfu',
             hidden=True)
    async def unstfu(self, context):
        if not context.author.voice or not context.author.voice.channel:
            await context.send("You are not connected to a voice channel")
            return

        cur_voice_channel = context.author.voice.channel

        for member in cur_voice_channel.members:
            await member.edit(mute=False)

        await context.send(f"Everyone has been unmuted on '{cur_voice_channel.name}'.")
        await self.save_data()

    @check_any(has_permissions(administrator=True), is_owner())
    @command(name='unset_mutable_channel',
             hidden=True)
    async def unset_mutable_channel(self, context):
        if not context.author.voice or not context.author.voice.channel:
            await context.send("You are not connected to a voice channel")
            return

        cur_voice_channel = context.author.voice.channel
        cur_voice_channel_id = str(cur_voice_channel.id)  # stringified for clarity, it is apparently done by default

        if cur_voice_channel_id not in self.data[MUTABLE_CHANNELS]:
            await context.send("This channel is not set as mutable. "
                               "If you want to set this, use !set_mutable_channel.")
            return

        if self.data[MUTABLE_CHANNELS][cur_voice_channel_id]:  # If the channel is muted when this is executed.
            for member in cur_voice_channel.members:           # We first unmute everyone
                await member.edit(mute=False)

        del self.data[MUTABLE_CHANNELS][cur_voice_channel_id]
        await context.send(f"Voice channel '{cur_voice_channel.name}' is not a mutable channel anymore.")
        await self.save_data()


def setup(client):
    client.add_cog(VoiceManager(client))
