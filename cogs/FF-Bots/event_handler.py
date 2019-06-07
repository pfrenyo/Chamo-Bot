import discord
from discord.ext import commands


# This class handles all events except 2 :
# - on_ready for initial bot connection (giving internal info only), handled by the main script (run_bot.py)
# - on_member_join, handled by welcome.py
class EventHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="Xenogears"))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await message.channel.send('Message deleted by the NSA.')


def setup(client):
    client.add_cog(EventHandler(client))