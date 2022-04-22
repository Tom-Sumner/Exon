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
	invis = 0x37393F

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

tokens = {
	"3": "OTMxMTU4MjAxNzc5NDg2NzMw.YeAWpw.ZBLhTJaMw--oDRRqKmm5buTQLKI",
	"4": "OTM3MTE5Njk0NjE0MzI3MzQ2.YfXGug.SgfizuolZhwSU5npSGrtU_6HkXI"
}

def config(data: dict):
	"""Adds data to config.json file"""
	with open(f"{MainCwd}/config.json", "r+") as f:
		f.write(json.dumps(data, indent=4))


MsgTargets = {
 1: 5,
 2: 10,
 3: 20,
 4: 40,
 5: 65,
 6: 100,
 7: 140,
 8: 180,
 9: 250,
 10: 300,
 11: 380,
 12: 470,
 13: 580,
 14: 700,
 15: 1000
}


def token():
# 	print("""
# Tokens:
# 	Maciej's: 1
# 	Tom's: 2
# 	Exon's: 3
# 	Exon BETA's: 4
# 	""")
	# wanted = input("Enter a number to choose\n>>>  ")
	# TOKEN = tokens[wanted]
	if "Working" in os.listdir(os.getcwd()):
		return "OTM3MTE5Njk0NjE0MzI3MzQ2.YfXGug.SgfizuolZhwSU5npSGrtU_6HkXI"
	else:
		return "OTMxMTU4MjAxNzc5NDg2NzMw.YeAWpw.hRYRrWYBSH_IwllskdWgpToxtuc"

def fetch(target):
	"""Fetch data from config.json

Returns:
	`data`: The requested information
	"""	
	with open(f"{str(os.getcwd())}/Bot/config.json", "r") as f:
		data = json.load(f)
		return data[target]


# class Exon:
# 	name = fetch_exon("name")
# 	discrim = fetch_exon("discriminator")
# 	HelpServer = fetch_exon("help server id")
# 	JoinChannel = fetch_exon("guild join channel id")
# 	LogChannel = fetch_exon("bot logs channel id")
# 	StatusChannel = fetch_exon("status channel id")
# 	AnnouncementsChannel = fetch_exon("announcement channel id")
# 	all = [name, discrim, HelpServer, JoinChannel, LogChannel, StatusChannel, AnnouncementsChannel]

class Settings:	
	def check(guild_id: int) -> bool:
		"""Checks if the guilds settings file exists

		Args:
			`guild_id` (int): The guild id to check
		"""		
		if f"{guild_id}.json" in os.listdir(f"{MainCwd}/guild settings"):
			pass
		else:
			Settings.Write.new(guild_id)

	class Write:
		"""Write data to guilds settings file
		"""
		data = {
		"settings": {
			"prefix": ".",
			"announcements": {
				"channel": "",
				"roles": []
			},
			"tickets": {
        		"count": "0"
    		}
		}
	}
		def new(guild_id):
			"""Create a new settings file"""
			with open(f"{MainCwd}/guild settings/{guild_id}.json", "w+") as f:
				json.dump(Settings.Write.data, f, indent=4)

		def prefix(guild_id: id, prefix: str):
			"""Update the guilds prefix"""
			Settings.check(guild_id)

			with open(f"{MainCwd}/guild settings/{guild_id}.json", "r+") as f:
				data = json.load(f)
				data["settings"]["prefix"] = prefix
				f.seek(0)
				object = json.dumps(data, indent=4)
				object = object.replace(object[len(object) - 1], "")
				f.write(object)

		def ticket(guild_id: int):
			"""Update ticket count, adds 1 to the current guilds ticket count.

			Args:
				`guild_id` (int): The current guilds id
			"""
			Settings.check(guild_id)
			with open(f"{MainCwd}/guild settings/{guild_id}.json", "r") as f:
				data = json.load(f)
				data["settings"]["tickets"]["count"] = int(data["settings"]["tickets"]["count"]) + 1
				f.seek(0)
				json.dump(data, f, indent=4)


	class Read:
		"""Read data from a guilds settings file"""

		def prefix(client=None, message=None, guild_id=None) -> str:
			"""Get the current guilds prefix for Exon

			Args:
				`guild_id (int)`: The current guilds id

			Returns:
				`str`: The prefix
			"""
			if guild_id != None:
				Settings.check(guild_id)
				with open(f"{MainCwd}/guild settings/{guild_id}.json", "r") as f:
					data = json.load(f)
					return data["settings"]["prefix"]
			elif message != None:
				Settings.check(message.guild.id)
				with open(f"{MainCwd}/guild settings/{message.guild.id}.json", "r") as f:
					data = json.load(f)
					return data["settings"]["prefix"]