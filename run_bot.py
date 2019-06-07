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
DEFAULT_TOKEN_NAME = 'moogle'
VALID_TOKEN_NAMES = ['moogle', 'chocobo', 'lamia', 'whitemage']
WELCOME_PICTURE = "data/img/Chamo2.png"
with open(WELCOME_PICTURE, 'rb') as picture:
    WELCOME_PICTURE = discord.File(picture)

###################################
#    Setting up our little bot    #
###################################


########################################
# In case our script gets called as is #
########################################

if __name__ == '__main__':
    import sys
    COGS_FOLDER = 'cogs'
    token_name = DEFAULT_TOKEN_NAME if len(sys.argv) <= 1 else sys.argv[1]
    if token_name not in VALID_TOKEN_NAMES:
        print("/!\\ You did not input a valid argument for the script. The first argument represents the token name.")
        print("/!\\ Valid token names are : '", end='')
        print(*VALID_TOKEN_NAMES, sep='\', \'', end='')
        print("'.")
        print("/!\\ Defaulting to token: {}.".format(DEFAULT_TOKEN_NAME))
        token_name = DEFAULT_TOKEN_NAME

    # The following variable has a dual use :
    # - first for the file name,
    # - then for the content, which is the token id itself.
    TOKEN = "data/keys/{}.key".format(token_name)
    with open(TOKEN, 'r') as f:
        TOKEN = f.readline()

    if token_name == 'whitemage':
        BOT_PREFIX = "?"
        EXTENSIONS = [filename[:len(filename) - 3] for filename in os.listdir(COGS_FOLDER+"/WhiteMage") if
                  filename[0] != '_']  # We cut the '.py' from every filename, and don't take scripts starting with '_'.
        COGS_FOLDER = COGS_FOLDER+'.WhiteMage.'
    else:
        BOT_PREFIX = (".", "!")
        EXTENSIONS = [filename[:len(filename) - 3] for filename in os.listdir(COGS_FOLDER + "/FF-Bots") if
                      filename[0] != '_']  # We cut the '.py' from every filename,and don't take scripts starting w/ '_'
        COGS_FOLDER = COGS_FOLDER+'.FF-Bots.'

    client = commands.Bot(command_prefix=BOT_PREFIX)

    client.ADMIN_ID = ADMIN_ID
    # client.COGS_FOLDER is set in the main function.
    # client.CURRENT_BOT is set in the main function.
    # client.EXTENSIONS is set in the main function.
    client.WELCOME_PICTURE = WELCOME_PICTURE


    @client.event
    async def on_ready():
        print("---------------------------------------------------------------")
        print("Bot logged in as >>> {0.name} <<< (id : {0.id})".format(client.user))
        print("---------------------------------------------------------------")


    client.BOT_PREFIX = BOT_PREFIX
    client.COGS_FOLDER = COGS_FOLDER
    client.CURRENT_BOT = token_name
    client.EXTENSIONS = EXTENSIONS

    for extension in EXTENSIONS:
        try:
            client.load_extension(COGS_FOLDER+extension)
        except Exception as error:
            print('Extension \'{}\' cannot be loaded. [Reason: {}]'.format(extension, error))

    client.run(TOKEN)
