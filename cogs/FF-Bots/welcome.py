import json
import discord
from os.path import join, isfile
from discord.ext import commands
from discord import File as discordFile

# Format the following with .format(member, guild)
DEFAULT_WELCOME_MESSAGE = ":flag_fr: Mon cher {0.mention}, bienvenue à {1.name}!\n" \
                          ":flag_us: My dear {0.mention}, welcome to {1.name}!"

# Check the other custom welcome messages for servers
CUSTOM_WELCOME_MESSAGES_DATA_FILE = join("data", "info", "welcome.json")

# Dual use variables - hard-coded custom welcome message for the most important server
# Both of these need to exist together
CHAMO_SERVER_ID = join("data", "keys", "chamo_server.key")
WELCOME_PICTURE = join("data", "img", "Chamo2.png")


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                                  Cog handling events requiring greetings                                            #
#######################################################################################################################
class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Check if custom messages are needed
        try:
            with open(CUSTOM_WELCOME_MESSAGES_DATA_FILE, 'r') as f:
                self.custom_welcome_messages = json.load(f)
                print("> Successfully loaded data from {}".format(CUSTOM_WELCOME_MESSAGES_DATA_FILE))
        except IOError:
            self.custom_welcome_messages = None
            print("> No custom welcome message file (at {}).\n"
                  "> Feel free to make one if you want custom welcome messages "
                  "for some specific servers (instructions in data/info/README.md)."
                  .format(CUSTOM_WELCOME_MESSAGES_DATA_FILE))

        # Check if we need the Chamo server custom message and image
        self.chamo_server_id = None
        try:
            if isfile(WELCOME_PICTURE):  # We just check if WELCOME_PICTURE exists. No further checks, we trust you.
                with open(CHAMO_SERVER_ID, 'r') as f:
                    self.chamo_server_id = int(f.readline())
            else:
                print("> No Chamo welcome picture: ignoring hard-coded Chamo server shenanigans.")
        except IOError:
            print("> Could not find the Chamo server id: ignoring hard-coded Chamo server shenanigans.")

    # Event handler for new member join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        print("hello")

        # guild.system_channel is the channel indicated as default for new members
        if self.chamo_server_id and int(guild.id) == self.chamo_server_id and guild.system_channel is not None:
            moogle_emoji = discord.utils.get(guild.emojis, name='moogle')
            message = "{0} {0} {0} {0} :flag_fr: Mon cher {1.mention}, bienvenue à la {2.name}!! " \
                      "Pour fêter ton arrivée, voici la magnifique jaquette de la Secte, rien que pour toi!\n" \
                      "{0} {0} {0} {0} :flag_us: My dear {1.mention}, welcome to {2.name}!! " \
                      "Let us celebrate your arrival with this magnificent game box representing our Sect!\n" \
                .format(moogle_emoji, member, guild)
            with open(WELCOME_PICTURE, 'rb') as picture:
                await guild.system_channel.send(content=message, file=discordFile(picture))
            return

        elif self.custom_welcome_messages:
            for guild_id, message in self.custom_welcome_messages.items():
                if guild.id == int(guild_id) and guild.system_channel is not None:
                    await guild.system_channel.send(content=message.format(member))
                    return

        if guild.system_channel is not None:
            await guild.system_channel.send(content=DEFAULT_WELCOME_MESSAGE.format(member, guild))


def setup(client):
    client.add_cog(Welcome(client))
