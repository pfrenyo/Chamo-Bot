from os.path import dirname
from utils import get_hidden_commands
from discord.ext.commands import Cog, command, check_any, is_owner, has_permissions


#######################################################################################################################
#                                          ---  'Admin' cog  ---                                                      #
#                                   Cog containing admin-only commands                                                #
#######################################################################################################################
class Admin(Cog):
    def __init__(self, client):
        self.client = client

    # Command to load a cog (also called 'extension' or 'module')
    @check_any(has_permissions(administrator=True), is_owner())
    @command()
    async def load(self, context, extension):
        try:
            self.client.load_extension(self.client.COGS_FOLDER+extension)
            print('Successfully loaded extension \'{}\''.format(extension))
        except Exception as error:
            print('Extension \'{}\' cannot be loaded. [Reason: {}]'.format(extension, error))

    # Command to unload a cog (also called 'extension' or 'module')
    @check_any(has_permissions(administrator=True), is_owner())
    @command()
    async def unload(self, context, extension):
        if extension != "admin" and extension != "debug":
            try:
                self.client.unload_extension(self.client.COGS_FOLDER+extension)
                print('Successfully unloaded extension \'{}\''.format(extension))
            except Exception as error:
                print('Extension \'{}\' cannot be unloaded. [Reason: {}]'.format(extension, error))
        else:
            print('Access denied: You cannot EVER unload extensions \'admin\' or \'debug\'.')

    @check_any(has_permissions(administrator=True), is_owner())
    @command(nam='adminhelp',
             hidden=True,
             aliases=['admincommands'])
    async def adminhelp(self, context):
        await get_hidden_commands(self.client, dirname(__file__))


def setup(client):
    client.add_cog(Admin(client))
