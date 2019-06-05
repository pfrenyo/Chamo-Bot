import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await message.channel.send('Message deleted by the NSA.')


def setup(client):
    client.add_cog(Events(client))