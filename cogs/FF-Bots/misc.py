from discord.ext import commands
import requests
import datetime


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

    @commands.command(name='epoch2dt')
    async def epoch2dt(self, context, epoch):
        dt = datetime.datetime.fromtimestamp(float(epoch))
        await context.send("Epoch *{}* is equivalent to datetime *{}*.".format(epoch, dt))

    @commands.command(name='dt2epoch')
    async def dt2epoch(self, context, date, time):
        fused = date + " " + time
        dt = datetime.datetime.strptime(fused, '%Y-%m-%d %H:%M:%S')
        await context.send("Datetime *{}* is equivalent to epoch *{}*.".format(fused, dt.timestamp()))


def setup(client):
    client.add_cog(Misc(client))
