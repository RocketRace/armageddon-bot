import discord

from discord.ext import commands
from json        import load

# Sets up the bot
config = load(open("config.json"))

setup = {
    "command_prefix":config.get("prefixes"),
    "help_command":None
}

bot = commands.Bot(**setup)

# Loads the bot modules
modules = ["cogs.nuclear"]
if __name__ == "__main__":
    for cog in modules:
        bot.load_extension(cog)

# Adds a global check to all commands.
# Invoker must have administratir permissions and be in a guild channel (outside a DM & group channel).
@bot.check
def guild_and_admin(ctx):
    if not isinstance(ctx.channel, discord.abc.GuildChannel):
        return False
    if not ctx.channel.permissions_for(ctx.author).administrator:
        return False
    return True


# Begins the bot
bot.run(config.get("token"))