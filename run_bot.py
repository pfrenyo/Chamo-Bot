import os
import discord
from discord.ext import commands

#######################################################################################################################
#                                Setting up the script directory as main directory                                    #
#######################################################################################################################

abspath = os.path.abspath(__file__)
dir_name = os.path.dirname(abspath)
os.chdir(dir_name)

#######################################################################################################################
#                                               Main function                                                         #
#######################################################################################################################

if __name__ == '__main__':

    ###################################################################################################################
    #                                         Setting up our constants                                                #
    ###################################################################################################################

    # The following variable has a dual use :
    # - first for the file name,
    # - then for the content, which is the admin's id itself.
    # These type of variables will have a '# Dual use variable' comment before they're used.
    ADMIN_ID = "data/keys/admin.key"
    with open(ADMIN_ID, 'r') as f:
        ADMIN_ID = f.readline()

    BOT_PREFIX = (".", "?", "!")

    # Dual use variable : will first only be the cogs folder, then become the exact folder for calling extensions in
    #                     the client.load_extensions function (using the 'dot' format, i.e. 'folder1.folder2.some_cog').
    COGS_FOLDER = 'cogs'
    DEFAULT_TOKEN_NAME = 'moogle'
    VALID_TOKEN_NAMES = ['moogle', 'chocobo', 'lamia', 'whitemage']

    # Dual use variable: file name, then picture file itself.
    WELCOME_PICTURE = "data/img/Chamo2.png"
    with open(WELCOME_PICTURE, 'rb') as picture:
        WELCOME_PICTURE = discord.File(picture)

    ###################################################################################################################
    #                                          Fetching our tokens                                                    #
    ###################################################################################################################

    # Fetching the arguments used with the script (if any).
    import sys
    token_name = DEFAULT_TOKEN_NAME if len(sys.argv) <= 1 else sys.argv[1]

    if token_name not in VALID_TOKEN_NAMES:
        print("/!\\ You did not input a valid argument for the script. The first argument represents the token name.")
        print("/!\\ Valid token names are : '", end='')
        print(*VALID_TOKEN_NAMES, sep='\', \'', end='')
        print("'.")
        print("/!\\ Defaulting to token: {}.".format(DEFAULT_TOKEN_NAME))
        token_name = DEFAULT_TOKEN_NAME

    # Dual use variable : file name, then token id itself (content of the file).
    TOKEN = "data/keys/{}.key".format(token_name)
    with open(TOKEN, 'r') as f:
        TOKEN = f.readline()

    ###################################################################################################################
    #                                    Fetching our extensions (AKA cogs)                                           #
    ###################################################################################################################

    # Separating whitemage and the other tokens, using two different cog folders.
    # WhiteMage replies to commands starting with '?', while Moogle, Lamia and Chocobo reply to '.' and '!' commands.
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

    ###################################################################################################################
    #                        Initializing bot and setting up our 'globals' (between cogs)                             #
    ###################################################################################################################

    # We initialize the bot object as 'client'.
    client = commands.Bot(command_prefix=BOT_PREFIX)

    # Setting up global variables (accessible to all cogs/extensions)
    client.ADMIN_ID = ADMIN_ID
    client.BOT_PREFIX = BOT_PREFIX
    client.COGS_FOLDER = COGS_FOLDER
    client.CURRENT_BOT = token_name
    client.EXTENSIONS = EXTENSIONS
    client.WELCOME_PICTURE = WELCOME_PICTURE

    ###################################################################################################################
    #                             Setting up event handlers (common to all bots)                                      #
    ###################################################################################################################

    # Event handler for boot-up
    @client.event
    async def on_ready():
        print("---------------------------------------------------------------")
        print("Bot logged in as >>> {0.name} <<< (id : {0.id})".format(client.user))
        print("---------------------------------------------------------------")

    ###################################################################################################################
    #                              Loading up extensions and launching the bot                                        #
    ###################################################################################################################

    for extension in EXTENSIONS:
        try:
            client.load_extension(COGS_FOLDER+extension)
        except Exception as error:
            print('Extension \'{}\' cannot be loaded. [Reason: {}]'.format(extension, error))

    client.run(TOKEN)
