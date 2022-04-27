import nextcord, os, sys, colorama, time, asyncio, requests
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils, dbutils
from utils import EmbedColors, Images
from nextcord import (
	Button,
	ChannelType,
	Guild,
	Message,
	SelectOption,
	TextChannel,
	slash_command,
	Webhook
)
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *

class welcome_message_prompt(nextcord.ui.Modal):
	def __init__(self):
		super().__init__("Change Welcome Message", timeout=5 * 60)

		self.message = nextcord.ui.TextInput(
			label="New Welcome Message",
			style=nextcord.TextInputStyle.paragraph, 
			placeholder="Use ;user; to mention the user and ;guild; to mention the guild", 
			required=True
		)
		
		self.add_item(self.message)

	async def callback(self, ctx: Interaction):
		dbutils.update_welcome_message(ctx.user.guild.id, self.message.value)
		await ctx.send(ephemeral=True, content="The welcome message has been updated!")

class EditWelcomeMessage(nextcord.ui.View):
	def __init__(self, client):
		super().__init__()
		self.value = None
		self.client = client

	@nextcord.ui.button(label="Edit Welcome Message", style=nextcord.ButtonStyle.blurple)
	async def edit(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		await ctx.response.send_modal(welcome_message_prompt())
		await ctx.edit_original_message(
			embed=nextcord.Embed(color=EmbedColors.notify,
			title="Settings",
			description="Configure settings for this guild"),
		view=HomeView(self.client))
		self.value = True
		self.stop()

	@nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.red)
	async def cancel(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		channel: nextcord.TextChannel = ctx.channel
		await ctx.response.edit_message(
			embed=nextcord.Embed(color=EmbedColors.notify,
			title="Settings",
			description="Configure settings for this guild"),
		view=HomeView(self.client))
		
		self.value = True
		self.stop()

class SetLogChannel(nextcord.ui.View):
	def __init__(self, client):
		self.client = client
		super().__init__()

	@nextcord.ui.button(label="Change Log", style=nextcord.ButtonStyle.blurple)
	async def edit(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		if ctx.user.guild_permissions.administrator == False:
			await ctx.send(embed=nextcord.Embed(color=EmbedColors.error,
				title="Error",
				description="You do not have the administrator permission to do this!"))
		else:
			await ctx.send("Please type #channelname and send it to set the log channel")
			channel: Message = await self.client.wait_for("message")
			chnl = channel.channel_mentions[0].id
			dbutils.update_log_channel(ctx.guild.id, chnl)
			logchnl = await ctx.guild.fetch_channel(chnl)
			await logchnl.send(embed=nextcord.Embed(
				color=EmbedColors.notify,
				title="Log Channel", 
				description="This channel has been set to Exon's log channel"))
			await ctx.channel.last_message.delete()
			await ctx.edit_original_message(
				embed=nextcord.Embed(color=EmbedColors.notify,
				title="Settings",
				description="Configure settings for this guild"),
			view=HomeView(self.client))

class EditPrefix(nextcord.ui.View):
	def __init__(self, client):
		self.client = client
		super().__init__()

	@nextcord.ui.button(label="Edit Prefix", style=nextcord.ButtonStyle.blurple)
	async def edit(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		class Pet(nextcord.ui.Modal):
			def __init__(self):
				super().__init__(
					"Change Prefix",
					timeout=5 * 60,  # 5 minutes
				)

				self.prefix = nextcord.ui.TextInput(
					label="New Prefix",
					placeholder=".",
					min_length=1,
					max_length=6
				)
				self.add_item(self.prefix)

			async def callback(self, interaction: nextcord.Interaction) -> None:
				prefix = self.prefix.value
				dbutils.update_prefix(interaction.guild.id, prefix)
				await ctx.send(ephemeral=True, content=f"The prefix for Exon has been changed to {prefix}")
		await ctx.response.send_modal(Pet())
		await ctx.edit_original_message(
			embed=nextcord.Embed(color=EmbedColors.notify,
			title="Settings",
			description="Configure settings for this guild"),
		view=HomeView(self.client))
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

class Home(nextcord.ui.Select):
	def __init__(self, client):
		self.client = client
		options = [
			nextcord.SelectOption(label="Guild Prefix", description="Change the prefix for this server", emoji="❗", value="prefix"),
			nextcord.SelectOption(label="Welcome Message", description="Setup or customize a welcome message", emoji="👋", value="welcome"),
			nextcord.SelectOption(label="Log Channel", description="Change / Set the log channel for this server", emoji="📓", value="log")
		]
		
		super().__init__(placeholder="Select a setting", max_values=1, min_values=1, options=options)
	
	async def callback(self, ctx: Interaction):
		if self.values[0] == "prefix":
			await ctx.response.edit_message(embed=nextcord.Embed(
					color=EmbedColors.notify,
					title="Prefix Settings",
					description=f"Change prefix for {ctx.guild.name}"), view=EditPrefix(client=self.client))
			pass
		elif self.values[0] == "welcome":
			await ctx.response.edit_message(embed=nextcord.Embed(
					color=EmbedColors.notify,
					title="Welcome Message Settings",
					description=f"Change welcome message for {ctx.guild.name}"), view=EditWelcomeMessage(client=self.client))

		elif self.values[0] == "log":
			await ctx.response.edit_message(embed=nextcord.Embed(
					color=EmbedColors.notify,
					title="Log Channel",
					description=f"Change log channel for {ctx.guild.name}"), view=SetLogChannel(client=self.client))
		else:
			pass

class HomeView(nextcord.ui.View):
	def __init__(self, client):
		super().__init__()
		self.add_item(Home(client=client))


class Settings(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	@commands.command()
	async def settings(self, ctx):
		await ctx.send(
			embed=nextcord.Embed(color=EmbedColors.notify,
			title="Settings",
			description="Configure settings for this guild"),
		view=HomeView(client=self.client))

def setup(client):
	client.add_cog(Settings(client))