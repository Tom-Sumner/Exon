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
from nextcord import slash_command
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound, MissingRequiredArgument
from nextcord import Interaction, SlashOption
from nextcord.abc import *

# Define the Cog
class ErrorHandlers(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, CommandNotFound):
			msg = await ctx.send("This command does not exist.")
			await asyncio.sleep(5)
			await msg.delete()

		elif isinstance(error, MissingPermissions):
			msg = await ctx.send(f"You dont have the necessary permissions to run this command\nNeeded perms: {error.missing_permissions}")
			await asyncio.sleep(5)
			await msg.delete()

		elif isinstance(error, MissingRole):
			msg = await ctx.send(f"You dont have the necessary roles to run the command\nNeeded roles: {error.missing_role}")
			await asyncio.sleep(5)
			await msg.delete()

		elif isinstance(error, MissingRequiredArgument):
			msg = await ctx.send(f"{error}")
			await asyncio.sleep(5)
			await msg.delete()

		else:
			await ctx.send("Something went badly wrong while running the command!")
			owner = await self.client.fetch_user(683700720515416065)
			await owner.send(f"Something went terribly wrong, sort me out!")
			await owner.send(error)

class EventHandlers(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client

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
			JoinAlertBot = nextcord.Webhook.from_url(
				session=session,
				url="https://discord.com/api/webhooks/951069049566138378/QrGi6IYaYZZMRWqLKZx1Rp6JZFpZ3FUaUx0_SMGiFQk05Vp4jxliVbIdSTsdoAdJ0Wis")
			await JoinAlertBot.send(embed=embed)

	# Auto delete commands
	@commands.Cog.listener()
	async def on_message(self, message: nextcord.Message):
		msg = message
		if msg.author == self.client.user:
			pass
		else:
			if msg.content == f"<@!{self.client.user.id}>":
				embed2 = nextcord.Embed(color=EmbedColors.success, title="About Exon", description="Current information about Exon")
				embed2.add_field(name="Uptime", value=f"Exon has been running for {self.client.uptime}")
				embed2.add_field(name="Amount of servers joined", value=f"Exon is currently serving in {len(self.client.guilds)} servers")
				embed2.add_field(name=f"Current preifx in {msg.guild.name}", value=f"The current prefix for {msg.guild.name} is {dbutils.fetch_prefix(guild_id=msg.guild.id)}")
				embed1 = nextcord.Embed(
					url="https://github.com/VasilyCodes/Exon/blob/main/README.md",
					color=EmbedColors.success,
					title="Exon's GitHub",
					description="Exon provides a multitude of user-friendly commands, including full slash command functionality and buttons, dropdowns, message commands and forms."
				)
				embed1.add_field(inline=False, name="Authors", value="- [@VasilyCodes](https://www.github.com/VasilyCodes)\n- [@ArtyomCodes](https://www.github.com/ArtyomCodes)")
				embed1.add_field(inline=False, name="Thanks To", value="- [Sinkez Hosting](https://hosting.sinkezstudios.com)")
				embed1.add_field(inline=False, name="Links", value="- [Website](https://sites.google.com/view/exon-bot)\n- [Invite to server](https://discord.com/oauth2/authorize?client_id=931158201779486730&permissions=1644972474359&scope=bot%20applications.commands)\n- [Help Server](https://discord.gg/invite/HXTzGzC2hA)\n- [GitHub README](https://github.com/CodeNEck-1/Exon)")
				embed1.add_field(inline=False, name="License", value="- [MIT License](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)")
				await msg.channel.send(embeds=[embed1, embed2])
			else:
				pass
	
	# @commands.Cog.listener()
	# async def on_member_join(self, member: nextcord.Member):
	# 	message = dbutils.fetch_welcome_message(member.guild.id)
	# 	message = message.replace(";user;", member.mention).replace(";guild;", member.guild.name)
	# 	await member.send(message)
		

# Setup the Cog
def setup(client):
	client.add_cog(ErrorHandlers(client))
	client.add_cog(EventHandlers(client))