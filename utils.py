"""Exon bot utils

Classes:
	Images: class
	EmbedColors: class
	Exon: class

Attributes:
	`pallate`: json
	`tokens`: json
	`cwd`: str

Functions:
	`token()`
	`fetch()`
"""

import nextcord, os, sys, json
sys.path.insert(1, "..")
from nextcord.utils import get
from nextcord.ext import commands
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import GuildChannel

if "Working" in os.listdir(os.getcwd()):
	CogsCwd = f"{os.getcwd()}/Working/cogs"
	MainCwd = f"{os.getcwd()}/Working"
else:
	CogsCwd = f"{os.getcwd()}/cogs"
	MainCwd = f"{os.getcwd()}"



class Images:
	"""Imgur links for Exon

	Attributes:
		BetaPNG: Link to PNG file
		BetaGIF: Link to GIF file
		MainPNG: Link to PNG file
		MainGIF: Link to GIF file
		NullPNG: Link to PNG file
	"""
	NullPNG = "https://i.imgur.com/R2KMzwX.png"

class EmbedColors:
	"""Exon's embed color pallate

	Colors:
		notify: 0x48AEF6 - light blue
		success: 0x54F33A - light green
		fail: 0xDD0000 - red
		error: 0xFF7A03 - orange
		ban: fail
		kick: error
		mute: notify"""	
	notify = 0x48AEF6
	success = 0x54F33A
	fail = 0xDD0000
	error = 0xFF7A03
	ban = fail
	kick = error
	mute = notify

# async def GuildMessageFrame(guild):
# 	if guild.icon == None:
# 		icon = Images.NullPNG
# 	else:
# 		icon = guild.icon
	
# 	embed = nextcord.Embed(color=EmbedColors.notify, title=f"I have joined {guild.name}", description=f"About {guild.name}")
# 	embed.add_field(name="__Name:__", value=guild.name, inline=False)
# 	embed.add_field(name="__Owner:__", value=f"<@!{guild.owner_id}>", inline=False)
# 	if guild.description != None:
# 		embed.add_field(name="__Description__", value=guild.description, inline=False)
# 	else:
# 		pass
# 	embed.add_field(name="__Server Icon__", value="** **", inline=False)
# 	embed.set_image(url=icon)
	
# 	return 

pallate = {
	"ban": EmbedColors.ban,
	"kick": EmbedColors.kick,
	"timeout": EmbedColors.kick,
	"mute": EmbedColors.mute,
	"cmd": EmbedColors.notify
}

def config(data: dict):
	"""Adds data to config.json file"""
	with open(f"{MainCwd}/config.json", "r+") as f:
		data["token"] = "token"
		f.write(json.dumps(data, indent=4))



def token():
	with open("config.json", "r") as f:
		data = json.loads(f.read())
		prefix = data["token"]
	return prefix

def fetch(target):
	"""Fetch data from config.json

Returns:
	`data`: The requested information
	"""	
	with open(f"{str(os.getcwd())}/Bot/config.json", "r") as f:
		data = json.load(f)
		return data[target]