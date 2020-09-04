import requests
from datetime import datetime
from discord.ext.commands import Cog, command


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                                    Cog containing miscellaneous commands                                            #
#######################################################################################################################
class Misc(Cog):
    def __init__(self, client):
        self.client = client

    # Get the current value of bitcoin
    @command()
    async def bitcoin(self, context):
        url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        response = requests.get(url)
        value = response.json()['bpi']['USD']['rate']
        await context.channel.send("Bitcoin price is: $" + value)

    # Debug function to get a person's current guild (which will just name the discord server the user is on)
    @command()
    async def myguild(self, context):
        await context.send(
            "Hey there {} AKA {}, your guild is {}.".format(context.message.author, context.message.author.mention,
                                                            context.message.author.guild))

    # Debug function to get a channel from a channel id
    @command()
    async def getchannel(self, context, channel):
        chan_id = int(channel)
        chan = self.client.get_channel(chan_id)
        if chan:
            await context.send("Channel name:\n{}".format(chan.name))
        else:
            usr = self.client.get_user(chan_id)
            if usr:
                await context.send("This isn't a real channel name. It is a DM Channel with user:\n{}".format(usr.name))
            else:
                await context.send("This doesn't seem like a valid channel id.")

    @command(name='epoch2dt')
    async def epoch2dt(self, context, epoch):
        dt = datetime.fromtimestamp(float(epoch))
        await context.send("Epoch *{}* is equivalent to datetime *{}*.".format(epoch, dt))

    @command(name='dt2epoch')
    async def dt2epoch(self, context, date, time):
        fused = date + " " + time
        dt = datetime.strptime(fused, '%Y-%m-%d %H:%M:%S')
        await context.send("Datetime *{}* is equivalent to epoch *{}*.".format(fused, dt.timestamp()))


def setup(client):
    client.add_cog(Misc(client))
