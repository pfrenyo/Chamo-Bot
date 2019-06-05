import os
import discord
from discord.ext import commands

#####################################################
# Setting up the script directory as main directory #
#####################################################

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

###################################
# Setting up our global variables #
###################################

# The following variable has a dual use :
# - first for the file name,
# - then for the content, which is the admin's id itself.
ADMIN_ID = "data/keys/admin.key"
with open(ADMIN_ID, 'r') as f:
    ADMIN_ID = f.readline()
BOT_PREFIX = (".", "?", "!")
COGS_FOLDER = 'cogs'
EXTENSIONS = [filename[:len(filename)-3] for filename in os.listdir(COGS_FOLDER) if filename[0] != '_']  # We cut the '.py' from every filename.
WELCOME_PICTURE = "data/img/Chamo2.png"
with open(WELCOME_PICTURE, 'rb') as picture:
    WELCOME_PICTURE = discord.File(picture)

###################################
#    Setting up our little bot    #
###################################

client = commands.Bot(command_prefix=BOT_PREFIX)

client.ADMIN_ID = ADMIN_ID
client.COGS_FOLDER = COGS_FOLDER
client.EXTENSIONS = EXTENSIONS
client.WELCOME_PICTURE = WELCOME_PICTURE

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="FF Tactics"))
    print("---------------------------------------------------------------")
    print("Bot logged in as >>> {0.name} <<< (id : {0.id})".format(client.user))
    print("---------------------------------------------------------------")


# @client.event
# async def on_message_delete(message):

@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        moogle_emoji = discord.utils.get(guild.emojis, name='moogle')
        message = "{0} {0} {0} {0} Mon cher {1.mention}, bienvenue à la {2.name}!! " \
                  "Pour feter ton arrivée, voici la magnifique jacquette de la Secte, rien que pour toi! " \
                  "{0} {0} {0} {0}\n" \
                  "{0} {0} {0} {0} My dear {1.mention}, welcome to the {2.name}!! " \
                  "Let us celebrate your arrival with this magnificent game box representing our Sect! " \
                  "{0} {0} {0} {0}\n" \
            .format(moogle_emoji, member, guild)
        await guild.system_channel.send(content=message, file=WELCOME_PICTURE)


########################################
# In case our script gets called as is #
########################################

if __name__ == '__main__':
    import sys
    DEFAULT_TOKEN = 'moogle'
    token_name = DEFAULT_TOKEN if len(sys.argv) <= 1 else sys.argv[1]
    if token_name != 'moogle' and token_name != 'chocobo' and token_name != 'lamia':
        print("/!\\ You did not input a valid argument for the script. The first argument represents the token name.")
        print("/!\\ Valid token names are : moogle, lamia, chocobo.")
        print("/!\\ Defaulting to token: {}.".format(DEFAULT_TOKEN))
        token_name = DEFAULT_TOKEN

    # The following variable has a dual use :
    # - first for the file name,
    # - then for the content, which is the token id itself.
    TOKEN = "data/keys/{}.key".format(token_name)
    with open(TOKEN, 'r') as f:
        TOKEN = f.readline()

    for extension in EXTENSIONS:
        try:
            client.load_extension(COGS_FOLDER+'.'+extension)
        except Exception as error:
            print('Extension \'{}\' canot be loaded. [Reason: {}]'.format(extension, error))

    client.run(TOKEN)
