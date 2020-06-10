import discord
from discord import File as discordFile
from discord.ext import commands


# Dual use variables
CHAMO_SERVER_ID = "data/keys/chamo_server.key"
with open(CHAMO_SERVER_ID, 'r') as f:
    CHAMO_SERVER_ID = int(f.readline())

GOJARU_ID = "data/keys/gojaru.key"
with open(GOJARU_ID, 'r') as f:
    GOJARU_ID = int(f.readline())


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                                  Cog handling events requiring greetings                                            #
#######################################################################################################################
class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Event handler for new member join
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild

        # Replace with chamo_id below
        if int(guild.id) == CHAMO_SERVER_ID and guild.system_channel is not None:  # guild.system_channel is the channel indicated as default for new members
            moogle_emoji = discord.utils.get(guild.emojis, name='moogle')
            message = "{0} {0} {0} {0} :flag_fr: Mon cher {1.mention}, bienvenue à la {2.name}!! " \
                      "Pour fêter ton arrivée, voici la magnifique jaquette de la Secte, rien que pour toi!\n" \
                      "{0} {0} {0} {0} :flag_us: My dear {1.mention}, welcome to {2.name}!! " \
                      "Let us celebrate your arrival with this magnificent game box representing our Sect!\n" \
                .format(moogle_emoji, member, guild)
            with open(self.client.WELCOME_PICTURE, 'rb') as picture:
                await guild.system_channel.send(content=message, file=discordFile(picture))

        elif int(guild.id) == GOJARU_ID and guild.system_channel is not None:
            await guild.system_channel.send(content=":flag_jp: :flag_be: {0.mention}君、このサーバーへようこそ！ぜひ楽しんでごじゃる！".format(member))

        elif guild.system_channel is not None:
            message = ":flag_fr: Mon cher {0.mention}, bienvenue à {1.name}!\n" \
                      ":flag_us: My dear {0.mention}, welcome to {1.name}!".format(member, guild)
            await guild.system_channel.send(content=message)



def setup(client):
    client.add_cog(Welcome(client))
