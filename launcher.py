import glob
import pathlib
import traceback

from discord.ext import commands

import constant


class MyBot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix=commands.when_mentioned_or("/"), **options)
        print("Starting Cubers Bot...")
        self.remove_command("help")

        for cog in pathlib.Path("cogs/").glob("*.py"):
            try:
                self.load_extension("cogs." + cog.stem)
                print(f"{cog.stem}.py has been loaded.")
            except:
                traceback.print_exc()

    async def on_ready(self):
        # channel = self.bot.get_channel(constant.CH_REGISTER_ID)
        # message = await channel.fetch_message(constant.MESSAGE_REGISTER_ID)
        # if not message.reactions:
        #     message.add_reaction("👍")
        print("logged in as:", self.user.name, self.user.id)

    async def on_command_error(self, ctx, error):
        ignore_errors = (commands.CommandNotFound, commands.CheckFailure)
        if isinstance(error, ignore_errors):
            return
        await ctx.send(error)


if __name__ == '__main__':
    bot = MyBot()
    bot.run(constant.DISCORD_BOT_TOKEN)
