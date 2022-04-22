# Coded By: Tom Sumner
# Date: 07-04-2022
# Github: Tom-Sumner / https://github.com/Tom-Sumner
# Discord: TSumner#5215
# License: MIT
# Note: If you use this code, you MUST credit me in your project.



import aiohttp
import nextcord, os, sys, colorama, time, asyncio
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils, dbutils
from utils import EmbedColors, Images
from nextcord import Client, Embed, slash_command
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound, MissingRequiredArgument
from nextcord import Interaction, SlashOption
from nextcord.abc import *


async def log(guild_id, type, client: Client, member=None, message=None, messages=None):
	channel_id = dbutils.fetch_log_channel(guild_id)
	try:
		channel = await client.fetch_channel(channel_id)
	except:
		channel = None
	if channel == None:
		pass
	else:
		if type == "join":
			embed = Embed(color=EmbedColors.invis, title="New Member", description=f"{member.mention} has joined the server.")
			await channel.send(embed=embed)
		elif type == "leave":
			embed = Embed(color=EmbedColors.invis, title="Member Left", description=f"{member.mention} has left the server.")
			await channel.send(embed=embed)
		elif type == "ban":
			embed = Embed(color=EmbedColors.invis, title="Member Banned", description=f"{member.mention} has been banned.")
			await channel.send(embed=embed)
		elif type == "unban":
			embed = Embed(color=EmbedColors.invis, title="Member Unbanned", description=f"{member.mention} has been unbanned.")
			await channel.send(embed=embed)
		elif type == "bulk":
			embed = Embed(color=EmbedColors.invis, title="Messages Deleted", description=f"A large amount of messages were deleted")
			embed.add_field(name="Messages", value=f"{messages}", inline=False)
			await channel.send(embed=embed)
		else:
			pass



class Logging(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	@commands.Cog.listener()
	async def on_member_join(self, member: nextcord.Member):
		if member.guild.large:
			pass
		else:
			if member.guild.system_channel == None:
				pass
			else:
				message = dbutils.fetch_welcome_message(member.guild.id)
				message = message.replace(";user;", member.mention).replace(";guild;", member.guild.name)
				await member.guild.system_channel.send(message)
		await log(member.guild.id, "join", self.client, member)
		
	@commands.Cog.listener()
	async def on_raw_bulk_message_delete(self, payload: nextcord.RawBulkMessageDeleteEvent):
		await log(payload.guild_id, "bulk", self.client, payload.cached_messages)

	@commands.Cog.listener()
	async def on_member_remove(self, member: nextcord.Member):
		await log(member.guild.id, "leave", self.client, member)

	@commands.Cog.listener()
	async def on_member_ban(self, guild: nextcord.Guild, member: nextcord.Member):
		await log(guild.id, "ban", self.client, member)

	@commands.Cog.listener()
	async def on_member_unban(self, guild: nextcord.Guild, member: nextcord.Member):
		await log(guild.id, "unban", self.client, member)

# Setup the Cog
def setup(client):
	client.add_cog(Logging(client))
