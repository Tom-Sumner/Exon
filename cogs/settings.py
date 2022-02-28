import discord as nextcord, os, sys, colorama, time, asyncio, requests
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
from nextcord.ui import InputText, Modal
import utils
from utils import EmbedColors, Images, pallate, token, tokens, fetch
from nextcord import ChannelType, TextChannel, slash_command, Webhook
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *

class PrefixPrompt(Modal):
    def __init__(self) -> None:
        super().__init__("Change prefix")
        self.add_item(InputText(label="Enter the new prefix", placeholder="New prefix")) 

    async def callback(self, ctx: nextcord.Interaction):
        prefix = self.children[0].value
        utils.Settings.Write.prefix(guild_id=ctx.guild.id, prefix=prefix)
		await ctx.followup.send(embed=nextcord.Embed(color=EmbedColors.success, title=":white_Check_mark:", 
		description=f"The prefix for {ctx.guild.name} has been update to {prefix}").set_footer(icon_url=ctx.user.display_avatar.url,
		text=f"{ctx.user.display_name} changed the prefix for Exon to {prefix} for {ctx.guild}"))


class EditPrefix(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.value = None

	@nextcord.ui.button(label="Edit Prefix", style=nextcord.ButtonStyle.blurple)
	async def edit(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		channel: nextcord.TextChannel = ctx.channel
		await ctx.response.send_modal(PrefixPrompt)		
		
		self.value = True
		self.stop()

	@nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
	async def cancel(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		channel: nextcord.TextChannel = ctx.channel
		await ctx.response.edit_message(
			embed=nextcord.Embed(color=EmbedColors.notify,
			title="Settings",
			description="Configure settings for this guild"),
		view=HomeView())
		
		self.value = True
		self.stop()


class Tickets(nextcord.ui.Select):
	def __init__(self):
		options = [
			nextcord.SelectOption(label="Add ticket server", description="Use an external server for tickets", emoji="1️⃣", value="ExtS"),
			nextcord.SelectOption(label="Use this server", description="Create tickets in this server", emoji="2️⃣", value="IntS"),
			nextcord.SelectOption(label="Delete ticket", description="Delete ticketing system for this server", emoji="3️⃣", value="DelT")
		]
		super().__init__(placeholder="Select an option", max_values=1, min_values=1, options=options)
	
	async def callback(self, ctx: Interaction):
		pass

class TicketsVeiw(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.add_item(Tickets())

class Home(nextcord.ui.Select):
	def __init__(self):
		options = [
			nextcord.SelectOption(label="Guild Prefix", description="Exon's prefix for this server", emoji="❗", value="prefix"),
			nextcord.SelectOption(label="Tickets", description="Change ticket settings", emoji="🎫", value="ticket"),
			nextcord.SelectOption(label="Welcome Message", description="Setup or customize a welcome message", emoji="👋", value="welcome")
		]
		
		super().__init__(placeholder="Select a setting", max_values=1, min_values=1, options=options)
	
	async def callback(self, ctx: Interaction):
		if self.values[0] == "prefix":
			await ctx.response.edit_message(embed=nextcord.Embed(
					color=EmbedColors.notify,
					title="Prefix Settings",
					description=f"Change prefix for {ctx.guild.name}"), view=EditPrefix())
			pass
		elif self.values[0] == "ticket":
			await ctx.message.edit(view=TicketsVeiw(), embed=nextcord.Embed(
				color=EmbedColors.notify,
				title="Ticket Settings",
				description="Configure ticket settings"
			))
		elif self.vlaues[0] == "welcome":
			await ctx.send(embed=nextcord.Embed(color=EmbedColors.error, title="Coming Soon...",
                description="This setting will be coming in the near future"))
		else:
			pass

class HomeView(nextcord.ui.View):
	def __init__(self):
		super().__init__()
		self.add_item(Home())


class Settings(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	@commands.command()
	async def settings(self, ctx):
		await ctx.send(
			embed=nextcord.Embed(color=EmbedColors.notify,
			title="Settings",
			description="Configure settings for this guild"),
		view=HomeView())

	async def wait_for(event, user):
		result = await Settings.__init__().wait_for(event)
		if result.author == user:
			return result
		else:
			pass

def setup(client):
	client.add_cog(Settings(client))