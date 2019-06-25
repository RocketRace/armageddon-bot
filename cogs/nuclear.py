import discord
from discord.ext import commands

class NuclearCog(commands.Cog, name="nuclear"):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(NuclearCog(bot))