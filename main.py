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
init()

os.system("cls")
os.system("clear")

def ready(user, guilds):
	line1 = Style.NORMAL + Fore.CYAN + rf"        ┌───────────────────────────────────────────────────┐"
	line2 = Style.NORMAL + Fore.CYAN + rf"        |      ┌───────┐___   ___   ______   ┌──┐ ┌──┐      |"
	line3 = Style.NORMAL + Fore.CYAN + rf"        |      |   ____|\  \ /  /  /  __  \  |  \ |  |      |" + Style.NORMAL + Fore.YELLOW + "    User:" + f"{user}"
	line4 = Style.NORMAL + Fore.CYAN + rf"        |      |  |__    \  V  /  |  |  |  | |   \|  |      |"
	line5 = Style.NORMAL + Fore.CYAN + rf"        |      |   __|    >   <   |  |  |  | |  . `  |      |"
	line6 = Style.NORMAL + Fore.CYAN + rf"        |      |  |____  /  .  \  |  `--'  | |  |\   |      |"
	line7 = Style.NORMAL + Fore.CYAN + rf"        |      |_______|/__/ \__\  \______/  |__| \__|      |" + Style.NORMAL + Fore.YELLOW + "    Guilds Count:" + f"{guilds}"
	line8 = Style.NORMAL + Fore.CYAN + rf"        |                                                   |"
	line9 = Style.NORMAL + Fore.CYAN + rf"        └───────────────────────────────────────────────────┘"

	lines = [line1, line2, line3, line4, line5, line6, line7, line8, line9]
	print(Style.NORMAL + Fore.RED + "\n")
	for line in lines:
		print(Style.NORMAL + Fore.RED + line)
	print(Style.NORMAL + Fore.RED + "\n")

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
	if "Working" in os.listdir(os.getcwd()):
		if message.content.startswith("test."):
			await asyncio.sleep(5)
			await message.delete()
	else:
		if message.content.startswith(dbutils.fetch_prefix(guild_id=(message.guild.id))):
			await asyncio.sleep(5)
			await message.delete()
	await client.process_commands(message)

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
	

client.run(utils.token())