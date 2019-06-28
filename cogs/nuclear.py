import asyncio
import discord
import random

from discord.ext import commands

# For the "nuclear fallout" armageddon option
class NuclearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # "corrupts" a message
    def corrupt(self, text):
        # How many characters to change
        corrupt_count = int(len(text) / 4) + 1
        # Which ones from / to
        chosen_characters = random.sample(text, corrupt_count)
        # Arbitrary chars from my keyboard
        chosen_characters.extend("-_;:[]#£|½^¨~?<>§¤z")
        corrupted_text = []
        for c in text:
            if c in chosen_characters:
                # Chance of deleting chars altogether
                if random.random() < 0.75:
                    # Replace with ""corrupted"" char
                    corrupted_text.append(random.choice(chosen_characters))
            else:
                corrupted_text.append(c)
        return "".join(corrupted_text)


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
        warning_message = open("text/nuclear.txt")
        await ctx.send(warning_message.read())
        warning_message.close()

        try:
            await self.bot.wait_for("message", timeout=45.0, check=user_accepted)
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

            # Don't nuke the channel this was sent from
            try:
                for i, channel in enumerate(all_channels):
                    if channel == ctx.channel:
                        all_channels.pop(i)
                        raise Exception()
            # To activate once and then break two layers of loop
            except:
                pass

            # Absolutely nukes each channel and all users recently active in those
            own_role_position = ctx.guild.me.top_role.position
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
                        if message.author not in marked_users and message.author.discriminator != "0000":
                            marked_users.append(message.author)
                elif is_voice_channel:
                    # TODO: Sends a voice clip of a warning message
                    marked_users = marked_channel.members

                # Has a delay if any users are about to get kicked
                if marked_users: await asyncio.sleep(random.random() * 4)
                # Kicks every marked user
                for user in marked_users:
                    try:
                        if user.top_role.position < own_role_position:
                            print(user.display_name  + str(user.discriminator) + "is getting kicked")
                            await user.kick(reason="It's the end of the world!")
                    # They already left the guild
                    except:
                        pass
                # Deletes the channel
                print(marked_channel.name)
                await marked_channel.delete(reason="It's the end of the world!")
            
            # Purges inactive members
            await ctx.guild.prune_members(days=7, compute_prune_count=False)

            # Turns all roles to dust
            all_roles = ctx.guild.roles
            # (But only ones the bot can access)
            to_delete = []
            for i, role in enumerate(all_roles):
                # Can't delete the @everyone role
                if role.is_default():
                    to_delete.append(i)
                # Can't delete roles above you
                elif role.position >= own_role_position:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_roles.pop(i)
            # Dusty color, minimal permissions (read/write only)
            permissions = discord.Permissions(3524672)
            color = discord.Color(0x998c85)
            for role in all_roles:
                # Mutates the names
                name = self.corrupt(role.name)
                print("role " + role.name + " turned into " + name)
                await role.edit(name=name, permissions=permissions, color=color, reason="It's the end of the world!")

            # Turns all remaining members to dust
            all_members = ctx.guild.members
            # (If accessible)
            to_delete.clear()
            for i, member in enumerate(all_members):
                # Can't kick users with higher roles than you
                if member.top_role.position >= own_role_position:
                    to_delete.append(i)
                # You probably don't want yourself to be kicked
                elif member.id == ctx.author.id:
                    to_delete.append(i)
                # You don't want to kick the bot, since that will most likely interrupt the snap
                elif member.id == self.bot.user.id:
                    to_delete.append(i)
            to_delete.reverse()
            for i in to_delete:
                all_members.pop(i)

            # Corrupts their nicknames
            for member in all_members:
                name = self.corrupt(member.display_name)
                print(member.display_name + " turned into " + name)
                await member.edit(name=name)

            # Corrupts the server
            name = self.corrupt(ctx.guild.name)
            print(ctx.guild.name + " turned into " + name)
            await ctx.guild.edit(name=name)

def setup(bot):
    bot.add_cog(NuclearCog(bot))