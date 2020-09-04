#######################################################################################################################
#                                             Helper functions                                                        #
#######################################################################################################################

# The following variables have a dual use :
# - first for the file name,
# - then for the content, which is the id itself.
# These type of variables will have a '# Dual use variable' comment before they're used.
import asyncio

ADMIN_ID = "data/keys/admin.key"
with open(ADMIN_ID, 'r') as f:
    ADMIN_ID = int(f.readline())


# DEPRECATED
# Function checking whether or not a user is the administrator (owner) of the bot.
# DEPRECATED
#
# @pre: the Admin object, the command/message's context
# @post: boolean value indicating whether or not the sender is admin
def is_bot_admin(context):  # Can be done with a sexy decorator later: TO BE IMPLEMENTED!!!
    return context.author.id == ADMIN_ID


# Function fetching the discord user object of the admin of the server.
#
# @pre: a bot's Client object
# @post: discord.User object of the administrator (owner)
async def fetch_admin(client):
    return await client.fetch_user(ADMIN_ID)


# Function sending a message that gets deleted after (delay) seconds.
#
# @pre: context, message, delay
# @post: void
async def send_temporary_msg(context, message, delay=3):
    message_object = await context.send(message)
    await asyncio.sleep(delay)
    await message_object.delete()
