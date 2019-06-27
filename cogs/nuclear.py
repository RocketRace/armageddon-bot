import asyncio
import discord
import random

from discord.ext import commands

# For the "nuclear fallout" armageddon option
class NuclearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def nuclear(self, ctx):
        # For retaining sessions
        def user_accepted(new_ctx):
            if new_ctx.author.id != ctx.author.id:
                return False
            if new_ctx.content != "yes":
                raise commands.UserInputError()
            return True

        # Sends the warning message (visible in text/nuclear.txt)
        await ctx.trigger_typing()
        await asyncio.sleep(2)
        warning_message = open("text/nuclear.txt").read()
        await ctx.send(warning_message)

        try:
            await self.bot.wait_for("message", timeout=30.0, check=user_accepted)
        except (asyncio.TimeoutError, commands.UserInputError):
            await ctx.send("You ponder for a minute... In the end you choose not to press the button. Perhaps for the best...")
        else:
            # A bit of story
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("You smash the glass, exposing the magnificent button. You press your palm against the button, and **push down**...")
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send("You suddenly hear early warning response systems kick in outside.")
        
            # Prepares the guild for nuclear strike
            all_channels = ctx.guild.channels

            # Absolutely nukes each channel and all users recently active in those
            random.shuffle(all_channels)
            for marked_channel in all_channels:
                marked_users = []
                # Only does something for text & voice channels
                is_text_channel = isinstance(marked_channel, discord.TextChannel)
                is_voice_channel = isinstance(marked_channel, discord.VoiceChannel)
                if is_text_channel:
                    # Sends an early warning message
                    await marked_channel.send("@everyone **EARLY WARNING MESSAGE: NUCLEAR MISSILE HEADED THIS WAY. ALL USERS MUST EVACUATE IMMEDIATELY TO THE NEAREST UNDERGROUND SHELTER.**") 

                    # Chooses users to destroy along with the channel
                    message_history = marked_channel.history()
                    async for message in message_history:
                        if message.author not in marked_users:
                            marked_users.append(message.author)
                elif is_voice_channel:
                    # TODO: Sends a voice clip of a warning message
                    marked_users = marked_channel.members

                # Has a delay if any users are about to get kicked
                if marked_users: await asyncio.sleep(random.random() * 4)
                # Kicks every marked user
                for user in marked_users:
                    print(user.display_name)
                    try:
                        # await user.kick(reason="It's the end of the world!")
                        pass
                    # They already left the guild
                    except:
                        pass
                # Deletes the channel
                print(marked_channel.name)
                # await marked_channel.delete(reason="It's the end of the world!")

def setup(bot):
    bot.add_cog(NuclearCog(bot))