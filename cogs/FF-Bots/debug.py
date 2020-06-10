from discord.ext import commands


#######################################################################################################################
#                                          ---  'Welcome' cog  ---                                                    #
#                            Cog containing debug commands (generally for admin only)                                 #
#######################################################################################################################
class Debug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, commands.errors.CommandNotFound):
            await context.send("This command does not seem to exist on this bot.")
            # did you mean: command list?
        else:
            await context.send(f"A command error seems to have occurred.\nError: {error}")


def setup(client):
    client.add_cog(Debug(client))
