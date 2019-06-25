import discord
from discord.ext import commands

# For the "nuclear fallout" armageddon option
class NuclearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nuclear(selft, ctx):
        print("nuclear")

def setup(bot):
    bot.add_cog(NuclearCog(bot))