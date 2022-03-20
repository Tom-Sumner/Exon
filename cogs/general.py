import nextcord, os, sys, colorama, time, asyncio, requests
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils
from utils import EmbedColors, Images
from nextcord import ChannelType, Embed, TextChannel, slash_command, Webhook
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *
import aiohttp


# Define the Cog
class General(commands.Cog):
    def __init__(self, client):
        self.client: nextcord.Client = client

    # @nextcord.slash_command(description="Get help on a command")
    # async def help(self, ctx: Interaction, command):
    #     pass

    @nextcord.message_command(name="repeat")
    async def repeat(self, ctx: Interaction, msg: nextcord.Message):
        """Repeat a message"""
        if msg.embeds != None or [] or "":
            embed = msg.embeds[0].copy()
            embed.set_author(icon_url=msg.author.display_avatar.url, name=msg.author.display_name)
            await ctx.response.send_message(embed=embed)
        else:
            await ctx.response.send_message(f">>>  {msg.content}        |       By: {msg.author.mention}")

    @nextcord.message_command(name="bookmark")
    async def bookmark(self, ctx: Interaction, msg: nextcord.Message):
        """Bookmark a message so you can find it later"""
        await ctx.response.send_message("****")
        sent = await ctx.send("Bookmarked in your DM's :white_check_mark:")
        if msg.embeds != None or [] or "":
            embed = msg.embeds[0].copy()
            embed.set_author(icon_url=msg.author.display_avatar.url, name=msg.author.display_name)
            await ctx.user.send(embed=embed)
        else:
            await ctx.user.send(f">>>  {msg.content}        |       By: {msg.author.mention}")
        await sent.delete()

# Setup the Cog
def setup(client):
    client.add_cog(General(client))