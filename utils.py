import json
import asyncio
from os import listdir
from os.path import join

#######################################################################################################################
#                                             Helper functions                                                        #
#######################################################################################################################

# # DEPRECATED
# # The following variables have a dual use :
# # - first for the file name,
# # - then for the content, which is the id itself.
# # These type of variables will have a '# Dual use variable' comment before they're used.
# ADMIN_ID = "data/keys/admin.key"
# with open(ADMIN_ID, 'r') as f:
#     ADMIN_ID = int(f.readline())

# # DEPRECATED
# # Function checking whether or not a user is the administrator (owner) of the bot.
# #
# # @pre: the Admin object, the command/message's context
# # @post: boolean value indicating whether or not the sender is admin
# def is_bot_admin(context):  # Can be done with a sexy decorator later: TO BE IMPLEMENTED!!!
#     return context.author.id == ADMIN_ID

# # DEPRECATED
# # Function fetching the discord user object of the admin of the server.
# #
# # @pre: a bot's Client object
# # @post: discord.User object of the administrator (owner)
# async def fetch_admin(client):
#     return await client.fetch_user(ADMIN_ID)


# Function sending a message that gets deleted after (delay) seconds.
#
# @pre: context, message, delay
# @post: void
async def send_temporary_msg(context, message, delay=3):
    message_object = await context.send(message)
    await asyncio.sleep(delay)
    await message_object.delete()


# Function getting all the hidden commands and returning them.
#
# @pre: - a bot's Client object
#       - directory of the cogs whose source code will be analyzed for hidden commands
# @post: void (sends a message with a dictionary of all the hidden commands in every file inside cog_directory)
async def get_hidden_commands(client, cogs_directory):
    admin_commands = {}
    for cog_filename in filter(lambda x: "pycache" not in x, listdir(cogs_directory)):
        with open(join(cogs_directory, cog_filename)) as f:
            cog_source_code = f.read()
            cog_source_code = cog_source_code.split("hidden=True")
            if len(cog_source_code) < 2:
                continue
            cog_source_code = cog_source_code[1:]
            for cmd in cog_source_code:
                cmd = cmd.split("async def ")[1]
                cmd = cmd.split("(self")[0]
                admin_commands.setdefault(cog_filename, []).append(cmd)
    await client.AppInfo.owner.send(f"Current admin commands available on {client.CURRENT_BOT} are:\n"
                                    f"```{json.dumps(admin_commands, indent=4)}```")
