from cgitb import text
import aiohttp
import nextcord, os, sys, colorama, time, asyncio
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils
from utils import EmbedColors, Images, pallate, token, tokens, fetch
from nextcord import slash_command
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *

# Define the Cog
class ErrorHandlers(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

class EventHandlers(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	# Whenever bot joins new server, alert the help server that i have
	@commands.Cog.listener()
	async def on_guild_join(self, guild: nextcord.Guild):
		if guild.icon == None:
			icon = Images.NullPNG
		else:
			icon = guild.icon
		embed = nextcord.Embed(color=EmbedColors.notify, title=f"I have joined {guild.name}", description=f"About {guild.name}")
		embed.add_field(name="__Name:__", value=guild.name, inline=False)
		embed.add_field(name="__Owner:__", value=f"<@!{guild.owner_id}>", inline=False)
		if guild.description != None:
			embed.add_field(name="__Description__", value=guild.description, inline=False)
		else:
			pass
		FC = guild.text_channels[0]
		invite = await FC.create_invite()
		embed.add_field(name="__Invite__", value=str(invite), inline=False)
		embed.set_image(url=icon)
		embed.set_footer(text=f"Guild created at: {guild.created_at}")
		async with aiohttp.ClientSession() as session:
			JoinAlertBot = nextcord.Webhook.from_url(session=session, url="https://discord.com/api/webhooks/941431518780325948/-KpptFovvPrgAIEzaiHW1iqQOko2pORx7xvleUMKaK3K1lFkqI7IEqattu0W_7StwuFa")
			await JoinAlertBot.send(embed=embed)

	# Auto delete commands
	@commands.Cog.listener()
	async def on_message(self, msg: nextcord.Message):
		if msg.author == self.client.user:
			pass
		else:
			if msg.content.startswith(utils.Settings.Read.prefix(guild_id=msg.guild.id)):
				if "purge" in msg.content:
					pass
				else:
					await asyncio.sleep(5)
					await msg.delete()
			elif msg.content == f"<@!{self.client.user.id}>":
				await msg.channel.send(f"Im here {msg.author}, whats up?\nTo see my commands type {utils.Settings.Read.prefix(guild_id=msg.guild.id)}help")
			else:
				pass

# Setup the Cog
def setup(client):
	client.add_cog(ErrorHandlers(client))
	client.add_cog(EventHandlers(client))