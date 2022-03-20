import nextcord, os, sys, colorama, time, asyncio
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils, dbutils
from utils import EmbedColors, Images
from nextcord import slash_command
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *

# Define the Cog
class TestCommands(commands.Cog):
    def __init__(self, client):
        self.client: nextcord.Client = client

    @commands.group(invoke_without_subcommnads=True)
    async def testsettings(self, ctx):
        pass
    
    
    @testsettings.command(name="id")
    async def id(self, ctx):
        await ctx.send(f"{dbutils.fetch_prefix(guild_id = ctx.message.id)}")
    
    
    @testsettings.command(name="subcommand_name")
    async def prefix(self, ctx):
        await ctx.send(f"d")
    

    @nextcord.slash_command(guild_ids=[941810207804260352])
    async def uptime(self, ctx: Interaction):
        await ctx.send(f"Exon has been running for: {self.client.uptime}")

# Setup the Cog
def setup(client):
    client.add_cog(TestCommands(client))