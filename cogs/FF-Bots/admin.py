from discord.ext import commands
from utils import is_admin


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
        if is_admin(context):
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
        if is_admin(context):
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
