from discord.ext import commands


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                           Cog handling RSS subs from HorribleSubs (for anime updates)                               #
#######################################################################################################################
class RSSHorribleSubs(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(RSSHorribleSubs(client))