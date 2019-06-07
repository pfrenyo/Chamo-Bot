import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            moogle_emoji = discord.utils.get(guild.emojis, name='moogle')
            message = "{0} {0} {0} {0} :flag_fr: Mon cher {1.mention}, bienvenue à la {2.name}!! " \
                      "Pour feter ton arrivée, voici la magnifique jacquette de la Secte, rien que pour toi! " \
                      ":flag_fr: {0} {0} {0} {0}\n" \
                      "{0} {0} {0} {0} :flag_us: My dear {1.mention}, welcome to {2.name}!! " \
                      "Let us celebrate your arrival with this magnificent game box representing our Sect! " \
                      ":flag_us: {0} {0} {0} {0}\n" \
                .format(moogle_emoji, member, guild)
            await guild.system_channel.send(content=message, file=self.client.WELCOME_PICTURE)


def setup(client):
    client.add_cog(Welcome(client))