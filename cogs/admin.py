# Coded By: Tom Sumner
# Date: 07-04-2022
# Github: Tom-Sumner / https://github.com/Tom-Sumner
# Discord: TSumner#5215
# License: MIT
# Note: If you use this code, you MUST credit me in your project.



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
from nextcord import TextChannel

# Define the Cog
class Admin(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	@nextcord.slash_command(name="send-embed", description="Send an embed message to desired channel")
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
		await ctx.send(ephemeral=True, content="Message sent!", embed=embed)

	# Clear command
	@nextcord.slash_command(name="clear-channel", description="Delete all messages from a certain user or channel")
	async def clear(self, ctx: Interaction, 
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
		async def default(ctx: Interaction):
			amount = await ctx.channel.purge(limit=count)
			return amount

		async def User(ctx: Interaction, user:Member):
			amount = 0
			async for message in ctx.channel.history(limit=count):
				amount += 1
				if message.author == user:
					await message.delete()
				else:
					pass
			return amount

		async def Channel(ctx:Interaction, channel:TextChannel):
			amount = await channel.purge(limit=count)

		async def ChannelAndUser(ctx: Interaction, channel:TextChannel, user:Member):
			amount = 0
			async for message in channel.history(limit=count):
				amount += 1
				if message.author == user:
					await message.delete()
				else:
					pass
			return amount

		if channel == None:
			if user == None:
				amount = await default(ctx)
				embed.description = f"Deletd {len(amount)} messages from {channel.mention}"
			else:
				amount = await User(ctx, user)
				embed.description = f"Deleted {amount} messages from {user.mention}"
		elif user == None:
			if channel == None:
				pass
			else:
				amount = await Channel(ctx, channel)
				embed.description = f"Deleted {len(amount)} in {channel.mention}"
		elif user and channel != None:
			amount = await ChannelAndUser(ctx, channel, user)
			embed.description = f"Deleted {amount} messages from {user.mention} in {channel.mention}"
		else:
			amount = await default(ctx)
			embed.description = f"Deletd {len(amount)} messages from {channel.mention}"

		await ctx.send(embed=embed)



	# Kick command
	@nextcord.slash_command(name="kick", description="Kick a user from the server")
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


	@nextcord.message_command(name="Kick Author")
	async def kick_message(self, ctx: nextcord.Interaction, msg: nextcord.Message):
		if ctx.user.guild_permissions.kick_members:
			try:
				await msg.author.kick(reason=msg.content)
				kick = nextcord.Embed(
					color=EmbedColors.notify,
					title=f":boot: Kicked {msg.author.name}!",
					description=f"Reason: {msg.content}\nBy: {ctx.user.mention}")
				await ctx.send(ephemeral=True, embed=kick)
				await msg.author.send(embed=kick)
			except:
				pass
		else:
			await ctx.send(ephemeral=True, content=f"{ctx.user.mention} You do not have permission to kick users!")
	
	@nextcord.message_command(name="Ban Author")
	async def ban_message(self, ctx: nextcord.Interaction, msg: nextcord.Message):
		if ctx.user.guild_permissions.ban_members:
			try:
				await msg.author.ban(reason=msg.content)
				ban = nextcord.Embed(
					color=EmbedColors.notify,
					title=f":hammer: Banned {msg.author.name}!",
					description=f"Reason: {msg.content}\nBy: {ctx.user.mention}")
				await ctx.send(embed=ban)
				await msg.author.send(embed=ban)
			except:
				pass
		else:
			await ctx.send(ephemeral=True, content=f"{ctx.user.mention} You do not have permission to ban users!")


# Setup the Cog
def setup(client):
	client.add_cog(Admin(client))