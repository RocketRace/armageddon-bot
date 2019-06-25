import discord

from discord.ext import commands
from json        import load

# Sets up the bot
config = load(open("config.json"))

setup = {
    "command_prefix":config.get("prefixes")
}

bot = commands.Bot(**setup)

# Loads the bot modules
modules = ["nuclear"]
if __name__ == "__main__":
    for cog in modules:
        bot.load_extension(cog)

# Begins the bot
bot.run(config.get("token"))