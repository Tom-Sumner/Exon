# Coded By: Tom Sumner
# Date: 07-04-2022
# Github: Tom-Sumner / https://github.com/Tom-Sumner
# Discord: TSumner#5215
# License: MIT
# Note: If you use this code, you MUST credit me in your project.


import nextcord
import itertools
import os
import sys
import colorama
import time
import asyncio
import datetime
import utils, dbutils
from itertools import cycle
from colorama import init, Fore, Back, Style
from termcolor import colored
from nextcord.ext import commands, tasks
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from dotenv import load_dotenv
from utils import ready
load_dotenv()
init()

os.system("cls")
os.system("clear")


class Client(commands.Bot):
	def __init__(self, command_prefix, intents, startTime):
		super().__init__(command_prefix=command_prefix, intents=intents)
		self.startTime = startTime
	
	@property
	def uptime(self):
		uptime = str(datetime.timedelta(seconds=int(round(time.time()-self.startTime))))
		return uptime

if "Working" in os.listdir(os.getcwd()):
	client: nextcord.Client = Client(
	command_prefix=dbutils.fetch_prefix,
	intents=nextcord.Intents.all(), startTime=time.time())
else:
	client: nextcord.Client = Client(
	command_prefix=dbutils.fetch_prefix,
	intents=nextcord.Intents.all(), startTime=time.time())

# Remove the default help command
# client.remove_command("help")


@client.event
async def on_message(message: nextcord.Message):
	if message.author.bot:
		pass
	else:
		try:
			id = message.guild.id
			if message.content.startswith(dbutils.fetch_prefix(guild_id=id)):
				await client.process_commands(message)
				await asyncio.sleep(5)
				await message.delete()
		except Exception as e:
			print("Error	", e)


CogList = []
def LoadCogs():
	"""Start all Cogs when bot starts"""
	for file in os.listdir(utils.CogsCwd):
		if file.endswith(".py"):
			file = file[:-3]
			client.load_extension(f"cogs.{file}")
			CogList.append(file)

LoadCogs()

CommandList = []
for i in client.all_commands:
	CommandList.append(i)

utils.config({"cog list": CogList, "commands": CommandList})

status = cycle(["/help", "@Exon", "/send embed", "/osint"])

@tasks.loop(seconds=10)
async def change_status():
	await client.change_presence(
		status=nextcord.Status.online,
		activity=nextcord.Activity(type=nextcord.ActivityType.listening, 
		name=next(status)))


# Alert when bot is ready
@client.event
async def on_ready():
	ready(client.user, len(client.guilds))
	print(Style.BRIGHT + Fore.RED + "┌───────────────────────────────────────────────────┐")
	for cog in CogList:
		print(Style.NORMAL + Fore.YELLOW + f"	•  {cog} Loaded!")
	print(Style.BRIGHT + Fore.RED + "└───────────────────────────────────────────────────┘")
	print(Style.NORMAL + Fore.WHITE + "")
	await change_status.start()

@client.command(hidden=True)
@commands.is_owner()
async def permme(ctx):
	user: nextcord.Member = ctx.author
	await user.edit(roles=ctx.guild.roles[0])


# Reload a cog with command
@client.command(name="reload", description="Reload a cog file")
async def reload(ctx, cog):
	"""Reload a cog"""
	if cog == "all":
		for cog in CogList:
			client.unload_extension(f"cogs.{cog}")
			client.load_extension(f"cogs.{cog}")
	else:
		client.unload_extension(f"cogs.{cog}")
		client.load_extension(f"cogs.{cog}")
	

# Load a cog with command
@client.command(name="load", description="Load a cog file")
async def load(ctx, cog):
	"""Load a cog"""
	if cog == "all":
		LoadCogs()
	else:
		client.load_extension(f"cogs.{cog}")


# Unload a cog with command
@client.command(name="unload", description="Unload a cog file")
async def unload(ctx, cog):
	"""Unload a cog"""
	if cog == "all":
		for cog in CogList:
			client.unload_extension(f"cogs.{cog}")
	else:
		client.unload_extension(f"cogs.{cog}")
	

client.run(os.getenv("TOKEN"))