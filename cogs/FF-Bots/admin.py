import json
from os import listdir
from os.path import dirname, join

from discord.ext import commands
from utils import is_admin
from utils import fetch_admin


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

    @commands.command(nam='adminhelp',
                      hidden=True,
                      aliases=['admincommands'])
    async def adminhelp(self, context):
        if is_admin(context):
            admin_commands = {"admin.py": ["adminhelp"]}
            cogs_directory = dirname(__file__)  # getcwd()
            for cog_filename in filter(lambda z: z != "admin.py", listdir(cogs_directory)):
                with open(join(cogs_directory, cog_filename)) as f:
                    cog_code = f.read()
                    cog_code = cog_code.split("hidden=True")
                    if len(cog_code) == 1:
                        continue
                    cog_code = cog_code[1:]
                    for command in cog_code:
                        command = command.split("async def ")[1]
                        command = command.split("(self")[0]
                        admin_commands.setdefault(cog_filename, []).append(command)

            # From mooch and rss_manager so far
            admin = await fetch_admin(self.client)
            await admin.send("Current admin commands on admin are:\n```{}```".format(json.dumps(admin_commands, indent=4)))


def setup(client):
    client.add_cog(Admin(client))
