import re
from discord import TextChannel
import nextcord, os, sys, colorama, time, asyncio, json
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils
from utils import EmbedColors
from nextcord import Guild, Member, WebhookMessage, slash_command
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *

# Define the Cog
class Admin(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	@nextcord.slash_command(default_permission=False)
	async def send(self, interaction: nextcord.Interaction):
		await interaction.response.send_autocomplete()


	@send.subcommand(description="Send an embed message to desired channel")
	async def embed(self, ctx: nextcord.Interaction, channel: GuildChannel, 
		title: str = SlashOption(name="title", description="What should the title of the embed say"), message = SlashOption(name="message",
		description="The message of the embed")):
		await ctx.response.defer()
		embed = nextcord.Embed(
		title=title,
		color=EmbedColors.notify)
		embed.add_field(name="__Message__", value=message, inline=False)
		embed.set_footer(text=f"From {ctx.user.display_name}", icon_url=ctx.user.display_avatar)
		TChannel = nextcord.utils.get(ctx.guild.text_channels, id=channel.id)
		webhook = await TChannel.create_webhook(
		name=ctx.user.display_name)
		await webhook.send(embed=embed, avatar_url=ctx.user.display_avatar)
		await webhook.delete()

	# Clear command
	@nextcord.slash_command(name="purge", description="Delete all messages from a certain user or channel", default_permission=False)
	async def purge(self, ctx: Interaction, 
	channel: GuildChannel=SlashOption(name="channel", description="The channel to delete all messages in", required=False),
	user: Member=SlashOption(name="user", description="The user to delete all messages they sent", required=False),
	count: int=SlashOption(name="count", description="The count of messages to delete", required=False)):
		await ctx.response.defer(ephemeral=True)
		embed: nextcord.Embed = nextcord.Embed(
			color=EmbedColors.notify,
			title=f":white_check_mark:", 
			description="")
		embed.set_footer(text=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
		if count == None or 0:
			count = None
		else:
			count = count
		print(count)
		async def default(ctx: Interaction):
			await ctx.channel.purge(limit=count)

		async def User(ctx: Interaction, user:Member):
			async for message in ctx.channel.history(limit=count):
				if message.author == user:
					await message.delete()
				else:
					pass

		async def Channel(ctx:Interaction, channel:TextChannel):
			await channel.purge(limit=count)

		async def ChannelAndUser(ctx: Interaction, channel:TextChannel, user:Member):
			async for message in channel.history(limit=count):
				if message.author == user:
					await message.delete()
				else:
					pass

		if channel == None:
			if user == None:
				await default(ctx)
				embed.description = f"{ctx.channel.mention} has been purged!"
			else:
				await User(ctx, user)
				embed.description = f"All messages from {user.mention} have been deleted in {ctx.channel.mention}"
		elif user == None:
			if channel == None:
				pass
			else:
				await Channel(ctx, channel)
				embed.description = f"{ctx.channel.mention} has been purged!"
		elif user and channel != None:
			await ChannelAndUser(ctx, channel, user)
			embed.description = f"All messages from {user.mention} have been deleted in {channel.mention}"
		else:
			await default(ctx)
			embed.description = f"{ctx.channel.mention} has been purged!"


		msg = await ctx.send(embed=embed)
		time.sleep(1)



	# Kick command
	@nextcord.slash_command(name="kick", description="Kick a user from the server", default_permission=False)
	async def kick(self, ctx: Interaction, user: nextcord.Member, reason):
		if user == ctx.user:
			await ctx.send(ephemeral=True, content=f"{ctx.user.mention} You cannot kick yourself!")
		else:
			if ctx.user.guild_permissions.kick_members:
				try:
					await user.kick(reason=reason)
					kick = nextcord.Embed(
						color=EmbedColors.notify,
						title=f":boot: Kicked {user.name}!",
						description=f"Reason: {reason}\nBy: {ctx.user.mention}")
					await ctx.send(embed=kick)
					await user.send(embed=kick)
				except:
					pass
			else:
				await ctx.send(ephemeral=True, content=f"{ctx.user.mention} You do not have permission to kick users!")
	
	
	@nextcord.slash_command(warn)

		


# Setup the Cog
def setup(client):
	client.add_cog(Admin(client))