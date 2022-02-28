from ssl import Options
from turtle import color
from unicodedata import name
import nextcord, os, sys, colorama
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils
from utils import EmbedColors
from nextcord.utils import get
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions

# Define the Cog
class Poll(commands.Cog):
    def __init__(self, client):
        self.client: nextcord.Client = client

    @nextcord.slash_command(name="poll", description="Vote, Create and look for polls")
    async def poll(self, ctx: Interaction):
        pass

    @poll.subcommand(name="create", description="Create a new poll")
    async def create(self, ctx: Interaction,
        name = SlashOption(name="name", required=True, description="The name of the poll"),
        description = SlashOption(name="description", description="the description of the poll", required=True),
        options = SlashOption(name="options", description="The options to choose from", required=True),
        location: nextcord.abc.GuildChannel = SlashOption(name="where", description="Where to send the poll message", required=True)):
        embed = nextcord.Embed(color=EmbedColors.success, title=f"Poll: {name}, created :white_check_mark:", description="Created succesfully")
        embed.add_field(name="__Name__", value=name)
        embed.add_field(name="__Description__", value=description)
        embed.add_field(name="__Options__", value=options)
        embed.add_field(name="__Location__", value=location.mention)
        await ctx.response.send_message(embed=embed)

# Setup the Cog
def setup(client):
    client.add_cog(Poll(client))