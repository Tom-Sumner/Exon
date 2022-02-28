import re
import nextcord, os, sys, colorama, time, asyncio, json
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils
from utils import EmbedColors, Images, pallate, token, tokens, fetch
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
		pass


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
		await ctx.send(f"This message was sent to {channel.mention}", embed=embed)
		await ctx.send(f"You must now publish the message in {webhook.channel.mention}")

	# Clear command
	@nextcord.slash_command(guild_ids=[941810207804260352], name="purge", description="Delete all messages from a certain user or channel", default_permission=False)
	async def purge(self, ctx: Interaction, 
	channel: GuildChannel=SlashOption(name="channel", description="The channel to delete all messages in", required=False),
	user: Member=SlashOption(name="user", description="The user to delete all messages they sent", required=False)):
		await ctx.response.defer(ephemeral=True)
		embed: nextcord.Embed = nextcord.Embed(
			color=EmbedColors.notify,
			title=f":white_check_mark:", 
			description="")
		embed.set_footer(text=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)

		async def default(ctx: Interaction):
			await ctx.channel.purge()

		async def User(ctx: Interaction, user:Member):
			async for message in ctx.channel.history():
				if message.author == user:
					await message.delete()
				else:
					pass

		async def Channel(ctx:Interaction, channel:GuildChannel):
			await channel.purge()

		async def ChannelAndUser(ctx: Interaction, channel:GuildChannel, user:Member):
			async for message in channel.history():
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
	@commands.command(name="kick", description="Kick a user from the server")
	async def kick(self, ctx, user: nextcord.Member, *reason):
		reason = "".join(reason, " ")
		try:
			await user.kick(reason=reason)
			kick = nextcord.Embed(
				color=EmbedColors.notify,
				title=f":boot: Kicked {user.name}!",
				description=f"Reason: {reason}\nBy: {ctx.author.mention}")
			await ctx.send(embed=kick)
			await user.send(embed=kick)
		except:
			pass
	
	# Warn user
	@commands.command()
	@commands.has_guild_permissions(kick_members=True, moderate_members=True)
	async def warn(self, ctx, user: nextcord.Member, *reason):
		reason = "".join(reason, " ")
		# with open(fr"{os.getcwd()}\User Data\{user.name}.json", "w+") as f:
		data = {}
		data["user"] = user
		data["reason"] = "".join(reason, " ")
		print(json.dump(data))
		msg = nextcord.Embed(title=f"{user.name} Warned", color=EmbedColors.success)
		msg.add_field(name="__Who was warned__", value=user.mention, inline=False)
		msg.add_field(name="__Who used the warn command__", value=ctx.author.mention, inline=False)
		msg.add_field(name="__Reason__", value=reason)
		msg.add_field(name="__Conclusion__", value=f"{ctx.author.mention} warned {user.mention} for {reason}")
		await ctx.send(embed=msg)

		


# Setup the Cog
def setup(client):
	client.add_cog(Admin(client))