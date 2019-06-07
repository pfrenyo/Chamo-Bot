import discord
from discord.ext import commands
import random


class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def square(self, context, number):
        squared_value = int(number) * int(number)
        await context.channel.send(str(number) + " squared is " + str(squared_value))


def setup(client):
    client.add_cog(Math(client))