from discord.ext import commands


#######################################################################################################################
#                                             Helper functions                                                        #
#######################################################################################################################

# Function checking whether or not a user is the administrator of the bot.
#
# @pre: the Admin object, the command/message's context
# @post: boolean value indicating whether or not the sender is admin
def _is_admin(self, context):  # Can be done with a sexy decorator later: TO BE IMPLEMENTED!!!
    return int(context.author.id) == int(self.client.ADMIN_ID)


#######################################################################################################################
#                                          ---  'Admin' cog  ---                                                      #
#                                   Cog containing admin-only commands                                                #
#######################################################################################################################
class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Command to load a cog (also called 'extension' or 'module')
    @commands.command()
    async def load(self, context, extension):
        if _is_admin(self, context):
            try:
                self.client.load_extension(self.client.COGS_FOLDER+extension)
                print('Successfully loaded extension \'{}\''.format(extension))
            except Exception as error:
                print('Extension \'{}\' cannot be loaded. [Reason: {}]'.format(extension, error))
        else:
            await context.send('Command \'load\' can only be used by my administrator')

    # Command to unload a cog (also called 'extension' or 'module')
    @commands.command()
    async def unload(self, context, extension):
        if _is_admin(self, context):
            if extension != "admin" and extension != "debug":
                try:
                    self.client.unload_extension(self.client.COGS_FOLDER+extension)
                    print('Successfully unloaded extension \'{}\''.format(extension))
                except Exception as error:
                    print('Extension \'{}\' cannot be unloaded. [Reason: {}]'.format(extension, error))
            else:
                print('Access denied: You cannot EVER unload extensions \'admin\' or \'debug\'.')
        else:
            await context.send('Command \'unload\' can only be used by my administrator')


def setup(client):
    client.add_cog(Admin(client))
