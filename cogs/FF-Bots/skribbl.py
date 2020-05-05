from discord.ext import commands
from os.path import dirname, join

SKRIBBL_RESOURCE_LOCATION = join(dirname(dirname(dirname(__file__))), "data", "skribbl")


#######################################################################################################################
#                                          ---  'Skribbl' cog  ---                                                    #
#                               Cog containing commands for Skribbl.io functions                                      #
#######################################################################################################################
class Skribbl(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.on_going_vocabulary = None
        self.cur_max_words = 0
        self.active_words = {}
        self.words_per_user = {}

    @commands.command()
    async def skribbl_start(self, context, words_per_person, *, skribbl_name):
        if not words_per_person.isdigit():
            await context.channel.send("You need to input a number of words per person (i.e., !skribbl_start 5 Test01)")
        if skribbl_name in self.active_words:
            await context.channel.send(f"There is already a skribbl vocabulary called {skribbl_name} being filled.")
            return
        # 0 as self.cur_max_words means no limit.
        self.cur_max_words = int(words_per_person)
        if self.cur_max_words < 0:
            self.cur_max_words = 0
        self.on_going_vocabulary = skribbl_name
        self.active_words[skribbl_name] = set()
        await context.channel.send(f"Started skribbl vocabulary with name {skribbl_name}.")

    # Event listener for messages sent to Moogle, Skribbl-related functions
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None \
                and not message.author.bot \
                and self.on_going_vocabulary \
                and message.content[0] not in self.client.BOT_PREFIX:
            split_msg = message.content\
                .replace("、", ",")\
                .replace(";", ",")\
                .replace("\n", ",")\
                .replace(".", ",")\
                .split(",")
            for word in split_msg:
                if word:
                    if message.author.id not in self.words_per_user:
                        self.words_per_user[message.author.id] = {}

                    if self.on_going_vocabulary not in self.words_per_user[message.author.id]:
                        self.words_per_user[message.author.id][self.on_going_vocabulary] = self.cur_max_words
                    elif self.words_per_user[message.author.id][self.on_going_vocabulary] == 0:
                        # With the elif, if self.cur_max_words = 0, it will go to the negatives and we can count
                        # the number of words with the negatives.
                        await message.channel.send(f"You have used up all {self.cur_max_words} of your "
                                                   f"words for this vocabulary set.")
                        return
                    self.words_per_user[message.author.id][self.on_going_vocabulary] -= 1
                    self.active_words[self.on_going_vocabulary].add(word.strip())
            await message.channel.send(f"Added the following words: {str(split_msg)}. "
                                       f"{self.words_per_user[message.author.id][self.on_going_vocabulary]} words "
                                       f"left.")

    @commands.command()
    async def skribbl_stop(self, context, skribbl_name):
        if skribbl_name not in self.active_words:
            await context.channel.send(f"No skribbl vocabulary called {skribbl_name}.")
            return

        output_file_name = join(SKRIBBL_RESOURCE_LOCATION, skribbl_name + ".txt")
        with open(output_file_name, "w", encoding='utf-8') as f:
            f.write(",".join(self.active_words[skribbl_name]))

        del self.active_words[skribbl_name]
        for k, v in self.words_per_user.items():
            if skribbl_name in v:
                del v[skribbl_name]
        if skribbl_name == self.on_going_vocabulary:
            self.on_going_vocabulary = None
            self.cur_max_words = 0
        else:
            await context.channel.send(f"FYI, you did not stop the current ongoing vocabulary, "
                                       f"which is '{self.on_going_vocabulary}'.")
        await context.channel.send(f"Vocabulary dumped in {output_file_name}.")


def setup(client):
    client.add_cog(Skribbl(client))
