import discord
import json
import os
import time
import subprocess
from discord.ext import commands

class Manage():
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='update',
                      description="update the code from github and reboot [OWNER ONLY]",
                      brief="update the bot",
                      pass_context=True)
    async def update(self, ctx):
        appInfo = await self.bot.application_info()
        if ctx.message.author == appInfo.owner:
            await self.bot.change_presence(game=discord.Game(name='rebooting'))
            subprocess.call("./update.sh")
        else:
            await self.bot.say("Invalid User")
    

    @commands.command(name='setplay',
                      description="change the game tag off the bot [ADMIN ONLY]",
                      brief="change the game tag",
                      pass_context=True)
    async def setplay(self, ctx,*, play):
        if ctx.message.author.server_permissions.administrator:
            await self.bot.change_presence(game=discord.Game(name=play))
        else:
            await self.bot.say("Invalid User")


    @commands.command(name='faketype',
                      description="send typing to the channel [ADMIN ONLY]",
                      brief="send typing",
                      pass_context=True)
    async def faketype(self, ctx, *playing):
        if ctx.message.author.server_permissions.administrator:
            await self.bot.delete_message(ctx.message)
            await self.bot.send_typing(ctx.message.channel)
        else:
            await self.bot.say("Invalid User")


    @commands.command(name='info',
                      description="get info on a specific user",
                      brief="info of a user",
                      pass_context=True)
    async def info(self, ctx):
        for user in ctx.message.mentions:
            member = ctx.message.server.get_member(user.id)
            embed_colour = self.bot.embed_color
            if member.colour != member.colour.default():
                embed_colour = member.colour.value
            embed = discord.Embed(title=str(user), url=user.avatar_url, description=user.display_name, color=embed_colour)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name='Is bot', value=user.bot, inline=True)
            embed.add_field(name='Voice channel', value=user.voice_channel, inline=True)
            role_list = "None"
            if len(member.roles) > 1:
                role_array = []
                for role in member.roles:
                    role_array.append(role.name)
                role_array.pop(0)
                role_array.reverse()
                role_list = ', '.join(role_array)
            embed.add_field(name='Roles', value=role_list, inline=False)
            embed.add_field(name='Playing', value=member.game, inline=False)
            embed.add_field(name='Joined discord at', value=user.created_at, inline=True)
            embed.add_field(name='Joined server at', value=member.joined_at, inline=True)
            await self.bot.say(embed=embed)

    @commands.command(name='serverinfo',
                      description="get info on the server",
                      brief="server info",
                      pass_context=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        total = len(ctx.message.server.members)
        bot  = 0
        online = 0
        gaming = 0
        for member in server.members:
            if member.bot:
                bot += 1
            if member.status != discord.Status.offline:
                online += 1
            if member.game and not member.bot:
                gaming += 1
        embed = discord.Embed(
            title="serverInfo",
            description=server.name,
            color=self.bot.embed_color
        )
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name='Owner', value=server.owner, inline=False)
        embed.add_field(name='Region', value=server.region, inline=False)
        text_channel = 0
        voice_channel = 0
        for channel in server.channels:
            if channel.type == discord.ChannelType.text:
                text_channel += 1
            elif channel.type == discord.ChannelType.voice:
                voice_channel += 1
        embed.add_field(name='Text Channels', value=text_channel, inline=False)
        embed.add_field(name='Voice Channels', value=voice_channel, inline=False)
        embed.add_field(name='Members', value=total, inline=False)
        embed.add_field(name='Humans', value=total-bot, inline=False)
        embed.add_field(name='Bots', value=bot, inline=False)
        embed.add_field(name='Gaming', value=gaming, inline=False)
        embed.add_field(name='Online', value=online, inline=False)
        embed.add_field(name='Roles', value=len(server.roles), inline=False)
        await self.bot.say(embed=embed)
        
    @commands.command(name='say',
                      description="bot sends query and deletes trigger message",
                      brief="bot sends query",
                      pass_context=True)
    async def say(self, ctx, *,word):
        await self.bot.delete_message(ctx.message)
        await self.bot.say(word)

def setup(bot):
    bot.add_cog(Manage(bot))
