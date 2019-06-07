import discord
from discord.ext import commands


class WhiteMage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        whitemage_intro_msg = ":flag_us: Allow me to introduce myself.\nI am WhiteMage, " \
                              "a gentle bot designed to help you with your general health needs.\n" \
                              'I reply to commands starting with the \'?\' sign. ' \
                              'To get all of my possible commands, just type \'?help\' ' \
                              "in any chatroom or via PM.\n" \
                              'I generally work by pinging you via Personal Messages (PMs). ' \
                              "Please treat me kindly.\n" \
                              'PS : If you have any ideas about some improvements for this bot, ' \
                              'please send them ' \
                              'to my maker, {0.mention}.' \
                              "\n\n" \
                              ":flag_fr: Permettez-moi de me présenter.\n Je suis WhiteMage, " \
                              'un gentil bot infirmier conçu pour vous aider quant à vos ' \
                              "besoins de santé.\n" \
                              'Je réponds aux commandes commençant par le caractère \'?\'. ' \
                              'Pour connaitre l\'entièreté de mes commandes, tapez \'?help\' dans ' \
                              "n\'importe quel salon de chat ou via MP.\n" \
                              'En général, je compte vous ping via Message Personnel (MP). ' \
                              "Soyez gentil avec moi.\n" \
                              'PS : Si vous avez des idées d\'améliorations pour ce bot, ' \
                              'veuillez les envoyer à mon' \
                              'créateur, {0.mention}.'.format(await self.client.fetch_user(self.client.ADMIN_ID))
        for server in self.client.guilds:
            await server.system_channel.send(whitemage_intro_msg)


def setup(client):
    client.add_cog(WhiteMage(client))