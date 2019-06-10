from discord import File as discordFile
from discord.ext import commands
import random
BOOGALOO_URL = 'https://i.imgur.com/O9QjSPT.png'
WHAT_LALALAND = 'https://www.youtube.com/watch?v=J5sZadTEWTc'


#######################################################################################################################
#                                           ---  'Fun' cog  ---                                                       #
#                               Cog containing several fun (and useless) functions                                    #
#######################################################################################################################
class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    # An "eight ball" function, replying to a yes/no question.
    @commands.command(name='tellme',
                      description="Answers a yes/no question with divine knowledge from God himself. \n"
                                  "The reply is irrefutable",
                      brief="Yes/no question answered with absolute truth.",
                      aliases=['tell me', 'Tellme', 'Tell me'])
    async def tell_me(self, context):
        possible_responses = [
            'That is a resounding no',
            'It is not looking likely',
            'Too hard to tell',
            'It is quite possible',
            'Most definitely',
            'It is very very very likely',
            'Of course not',
            'It\'s an absolute yes from me',
            'Lol dunno'
        ]
        possible_names = [
            'my dear',
            'you sexy beast',
            'poor',
            'my friend',
            'my dearest companion',
            'you fuckboi',
            'dear',
            'my friend',
            'my dear',
            'my friend',
            'my dear',
            'my friend',
            'my dear',
            'my friend',
            'my dear',
            'my friend',
            'my dear',
            'my friend',
            'my dear',
            'my friend',
            'my dear'
        ]
        await context.channel.send("{}, {} {}".
                                   format(random.choice(possible_responses), random.choice(possible_names),
                                          context.message.author.mention))

    # Sends the user the game box of Chamo 2 (by uploading it to discord)
    @commands.command()
    async def boogaloo(self, context):
        with open(self.client.WELCOME_PICTURE, 'rb') as picture:
            await context.channel.send(content='\"Really makes you FEEL like a camel\" - Machinima',
                                       file=discordFile(picture))

    # Sends the user the game box of Chamo 2 (by sending a url)
    @commands.command()
    async def boogaloo_url(self, context):
        await context.send(BOOGALOO_URL)  # Same as context.channel.send

    # Tells a joke from a joke database
    @commands.command()
    async def joke(self, context):
        await context.send("This is a WIP. This will be a command telling a joke from a joke database.")

    # Reaction video: WHAT?! NO! from La La Land.
    @commands.command(name='what',
                      aliases=['what?', 'what!', 'what?!', 'what!?', 'whatno'])
    async def what(self, context):
        await context.send(WHAT_LALALAND)


def setup(client):
    client.add_cog(Fun(client))
