# Coded By: Tom Sumner
# Date: 07-04-2022
# Github: Tom-Sumner / https://github.com/Tom-Sumner
# Discord: TSumner#5215
# License: MIT
# Note: If you use this code, you MUST credit me in your project.



import nextcord, os, sys, colorama, time, asyncio
from operator import itemgetter
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils, dbutils
from utils import EmbedColors
from nextcord import slash_command
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands import Context
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *

class model(nextcord.ui.Modal):
	def __init__(self, channel):
		super().__init__("Send an update to the bot", timeout=300)
		self.channel: nextcord.TextChannel = channel

		self.url = nextcord.ui.TextInput(
			style=nextcord.TextInputStyle.short,
			label="Title Link",
			placeholder="URL for the title",
			required=False
		)
		self.heading = nextcord.ui.TextInput(
			style=nextcord.TextInputStyle.short,
			label="Title Text",
			placeholder="The text for the title",
			required=True
		)
		self.message = nextcord.ui.TextInput(
			style=nextcord.TextInputStyle.paragraph,
			label="Message",
			placeholder="The message of the update",
			required=True
		)
		self.add_item(self.url)
		self.add_item(self.heading)
		self.add_item(self.message)
	async def callback(self, ctx: nextcord.Interaction) -> None:
		channel = self.channel
		embed =  nextcord.Embed(color=EmbedColors.info, url=self.url.value,
			title=self.heading.value,
			description="New Exon update!")
		embed.add_field(name="Message", value=self.message.value)
		message:nextcord.Message = await channel.send(embed=embed)
		await message.publish()
		await ctx.response.send_message(ephemeral=False, content="Update sent!", embed=embed)
class Confirm(nextcord.ui.View):
		def __init__(self, channel):
			super().__init__()
			self.value = None
			self.channel: nextcord.TextChannel = channel

		@nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.blurple)
		async def edit(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
			await ctx.response.send_modal(model(channel=self.channel))

class DevCommands(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	@commands.group(aliases=["db"], invoke_without_command=True)
	async def database(self, ctx):
		await ctx.send(f"{ctx.author.mention} You need to specify a subcommand.")
	

	@database.command(name="guilds")
	async def guilds(self, ctx):
		guildsp = dbutils.fetch_all_guilds()
		guilds = []
		for guilda in guildsp:
			if guilda[0] == 0 or "0":
				pass
			else:
				guild = {}
				guild["id"] = guilda[0]
				guild["prefix"] = guilda[1]
				guild["ticket"] = guilda[2]
				guild["welcome"] = guilda[3]
				guilds.append(guild)

		for guild in guilds:
			embed = nextcord.Embed(color=EmbedColors.success, title="All data in the database", description="The id, prefix, ticket category and welcome message of the guild")
			embed.add_field(name="ID", value=guild["id"], inline=False)
			embed.add_field(name="Prefix", value=guild["prefix"], inline=False)
			embed.add_field(name="Ticket Category", value=guild["ticket"], inline=False)
			embed.add_field(name="Welcome Message", value=guild["welcome"], inline=False)
			await ctx.send(embed=embed)

	@commands.command(name="storage")
	@commands.is_owner()
	async def storage(self, ctx):
		await ctx.author.send(file=nextcord.File("storage.sqlite3"))
		await ctx.send(f"{ctx.author.mention} Sent you the file.")

	@commands.command(name="update")
	@commands.is_owner()
	async def update(self, ctx: Context):
		channel = await self.client.fetch_channel(936999558582525989)
		# await ctx.send(view=Confirm(channel=channel))
		m = model(ctx.channel)
		print(m, type(m))



def setup(client):
	client.add_cog(DevCommands(client))