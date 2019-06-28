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
modules = ["cogs.nuclear", "cogs.snap", "cogs.zombie", "cogs.the"]
if __name__ == "__main__":
    for cog in modules:
        bot.load_extension(cog)

# Adds a global check to all commands.
# Invoker must have administrator permissions and be in a guild channel (outside a DM & group channel).
@bot.check
def guild_and_admin(ctx):
    if not isinstance(ctx.channel, discord.abc.GuildChannel):
        raise commands.NoPrivateMessage()
    if not ctx.channel.permissions_for(ctx.author).administrator:
        raise commands.MissingPermissions(discord.Permissions.administrator)
    if not ctx.channel.permissions_for(ctx.me).administrator:
        raise commands.BotMissingPermissions(discord.Permissions.administrator)
    return True

@bot.event
async def on_command_error(ctx, error):
    print(error)
    if isinstance(error, commands.UserInputError):
        await ctx.send("You hesitate, and decide not to follow through. Perhaps that's for the best...")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("Commands are guild-only. There is not much chaos I can incite in a private channel.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Only administrators can invoke my calamity. Otherwise, the world would be a more dangerous place...")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I need the administrator permission for everything I do. For maximum cinematic effect, consider also putting my role at the top of the role list.")

# Begins the bot
bot.run(config.get("token"))