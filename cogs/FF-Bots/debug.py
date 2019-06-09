from discord.ext import commands


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                            Cog containing debug commands (generally for admin only)                                 #
#######################################################################################################################
class Debug(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Debug(client))
