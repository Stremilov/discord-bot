import discord
from discord.ext import commands
from loguru import logger
from youtube_dl import YoutubeDL

if __name__ == "__main__":

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='-', intents=intents)

    logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")



    @bot.event
    async def on_ready():
        print(f"We have logged in as {bot.user} (ID: {bot.user.id})\n----------")


    @bot.command()
    async def hello(ctx):
        """Says hello to user."""
        await ctx.send('Hello my bro')
        await ctx.send('Have fun here!')


    @bot.command()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = f'Welcome {member.mention} to {guild.name}!'
            await guild.system_channel.send(to_send)


    YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
                   'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 - reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


    @bot.command()
    async def playyt(ctx, *, arg):
        vc = await ctx.message.author.voice.channel.connect()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            if 'https://' in arg:
                info = ydl.extract_info(arg, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

        url = info['formats'][0]['url']

        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))


    class MyClient(discord.Client):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.role_message_id = 0  # ID of the message that can be reacted to add/remove a role.
            self.emoji_to_role = {
                discord.PartialEmoji(name='🔴'): 0,  # ID of the role associated with unicode emoji '🔴'.
                discord.PartialEmoji(name='🟡'): 0,  # ID of the role associated with unicode emoji '🟡'.
                discord.PartialEmoji(name='green', id=0): 0,  # ID of the role associated with a partial emoji's ID.
            }

        async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
            """Gives a role based on a reaction emoji."""
            # Make sure that the message the user is reacting to is the one we care about.
            if payload.message_id != self.role_message_id:
                return

            guild = self.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                return

            try:
                role_id = self.emoji_to_role[payload.emoji]
            except KeyError:
                # If the emoji isn't the one we care about then exit as well.
                return

            role = guild.get_role(role_id)
            if role is None:
                # Make sure the role still exists and is valid.
                return

            try:
                # Finally, add the role.
                await payload.member.add_roles(role)
            except discord.HTTPException:
                # If we want to do something in case of errors we'd do it here.
                pass

        async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
            """Removes a role based on a reaction emoji."""
            # Make sure that the message the user is reacting to is the one we care about.
            if payload.message_id != self.role_message_id:
                return

            guild = self.get_guild(payload.guild_id)
            if guild is None:
                # Check if we're still in the guild and it's cached.
                return

            try:
                role_id = self.emoji_to_role[payload.emoji]
            except KeyError:
                # If the emoji isn't the one we care about then exit as well.
                return

            role = guild.get_role(role_id)
            if role is None:
                # Make sure the role still exists and is valid.
                return

            # The payload for `on_raw_reaction_remove` does not provide `.member`
            # so we must get the member ourselves from the payload's `.user_id`.
            member = guild.get_member(payload.user_id)
            if member is None:
                # Make sure the member still exists and is valid.
                return

            try:
                # Finally, remove the role.
                await member.remove_roles(role)
            except discord.HTTPException:
                # If we want to do something in case of errors we'd do it here.
                pass


    bot.run('MTAyNDA0MzAzODE0Nzg4NzEzNA.G74tIt.SQFmPwoilQzToc1XQ22_hpa4NLaz4zP_2Om63I')