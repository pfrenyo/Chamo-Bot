import discord
from discord.ext import commands


#######################################################################################################################
#                                       ---  'Event Handler' cog  ---                                                 #
#                                  Cog handling all events except 2, namely :                                         #
#      - on_ready for initial bot connection (giving internal info only), handled by the main script (run_bot.py)     #
#      - on_member_join, handled by welcome.py                                                                        #
#######################################################################################################################
class EventHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Event handler for boot-up, number 2 (there's also an 'on_ready' in run_bot.py, giving internal info only).
    # This one changes the status of the bot (visible to everyone) according to its identity (chocobo, lamia or moogle)
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name="Xenogears"))

    # Event handler for message deletion
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author != self.client.user:
            await message.channel.send('Message deleted by the NSA.')


def setup(client):
    client.add_cog(EventHandler(client))
