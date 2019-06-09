from discord.ext import commands
import requests


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                                    Cog containing miscellaneous commands                                            #
#######################################################################################################################
class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Get the current value of bitcoin
    @commands.command()
    async def bitcoin(self, context):
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        response = requests.get(url)
        value = response.json()['bpi']['USD']['rate']
        await context.channel.send("Bitcoin price is: $" + value)

    # Debug function to get a person's current guild (which will just name the discord server the user is on)
    @commands.command()
    async def myguild(self, context):
        await context.send(
            "Hey there {} AKA {}, your guild is {}.".format(context.message.author, context.message.author.mention,
                                                            context.message.author.guild))


def setup(client):
    client.add_cog(Misc(client))
