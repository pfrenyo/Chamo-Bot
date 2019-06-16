#######################################################################################################################
#                                             Helper functions                                                        #
#######################################################################################################################

# The following variable has a dual use :
# - first for the file name,
# - then for the content, which is the admin's id itself.
# These type of variables will have a '# Dual use variable' comment before they're used.
ADMIN_ID = "data/keys/admin.key"
with open(ADMIN_ID, 'r') as f:
    ADMIN_ID = int(f.readline())


# Function checking whether or not a user is the administrator of the bot.
#
# @pre: the Admin object, the command/message's context
# @post: boolean value indicating whether or not the sender is admin
def is_admin(context):  # Can be done with a sexy decorator later: TO BE IMPLEMENTED!!!
    return context.author.id == ADMIN_ID


# Function fetching the discord user object of the admin of the server.
#
# @pre: a bot's Client object
# @post: discord.User object of the administrator
async def fetch_admin(client):
    return await client.fetch_user(ADMIN_ID)
