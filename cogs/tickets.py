# Coded By: Tom Sumner
# Date: 07-04-2022
# Github: Tom-Sumner / https://github.com/Tom-Sumner
# Discord: TSumner#5215
# License: MIT
# Note: If you use this code, you MUST credit me in your project.



from typing import Text
import nextcord, os, sys, colorama, time, asyncio
from colorama import init, Fore, Back, Style
from termcolor import colored
init()
sys.path.insert(1, "..")
import utils, dbutils
from utils import EmbedColors
from nextcord import InteractionMessage, slash_command, Message
from nextcord.utils import get
from nextcord.ext import commands
from nextcord import TextChannel
from nextcord.ext.commands import Context
from nextcord.ext.commands.errors import MissingPermissions, MissingRole, CommandNotFound
from nextcord import Interaction, SlashOption
from nextcord.abc import *

class Button(nextcord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)

	@nextcord.ui.button(label="New Ticket", style=nextcord.ButtonStyle.blurple, custom_id="new_ticket")
	async def create(self, button: nextcord.ui.Button, ctx: Interaction):
		await ctx.response.send_message(ephemeral=True, content="Your ticket is being created now....")

		ticket_created_embed = nextcord.Embed(
			title="Ticket Processed",
			description=f"""Hey <@!{ctx.user.id}>! Thanks for opening a ticket with us today.\nPlease describe your enquiry and our team will respond shortly. We thank you in advance for your patience."""
		)

		overwrites = {
			ctx.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
			ctx.user: nextcord.PermissionOverwrite(view_channel=True),
			ctx.guild.me: nextcord.PermissionOverwrite(view_channel=True)
		}
		count = dbutils.fetch_ticket_count(guild_id=ctx.guild_id)
		dbutils.update_ticket_count(guild_id=ctx.guild_id, count=count + 1)
		msg: InteractionMessage = ctx.message
		ticket = await ctx.channel.category.create_text_channel(f"ticket-{count}", overwrites=overwrites)
		with open(f"{utils.MainCwd}/temp/tickets/{msg.guild.id}-{count}.txt", "a+") as f:
				f.write(f"""
{ctx.user.display_name.upper()}#{ctx.user.discriminator}'s ticket transcript
Created at: {time.strftime("%d/%m/%Y %H:%M")}
Server: {ctx.guild.name}

Messages:\n\n""")

		await ticket.send(embed=ticket_created_embed, view=Confirm(ctx.user))

# Define the Cog
class SimpleTicket(commands.Cog):
	def __init__(self, client: nextcord.Client):
		self.client: nextcord.Client = client
		self.client.persistent_views_added = False

	@commands.Cog.listener()
	async def on_message(self, msg: Message):
		if msg.channel.type == nextcord.ChannelType.text:
			channel: TextChannel = msg.channel
			if channel.name.startswith("ticket-") and channel.name != "ticket-transcripts":
				with open(f"{utils.MainCwd}/temp/tickets/{msg.guild.id}-{msg.channel.name.split('-')[1]}.txt", "a+") as f:
					f.write(f"At: {time.strftime('%d/%m/%Y %H:%M')} - {msg.author.name}: {msg.content}\n")
			else:
				pass

	@commands.Cog.listener(name="on_ready")
	async def on_ready(self):
		if not self.client.persistent_views_added:
			self.client.add_view(Button())
			self.persistent_views_added = True

	@commands.command()
	@commands.has_permissions(manage_channels=True, administrator=True)
	async def sendticket(self, ctx: Context):
		embed = nextcord.Embed(
			title="Contact Support",
			description="Click the button below to open a ticket"
		)
		await ctx.send(embed=embed, view=Button())
		overwrites = {
			ctx.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
			ctx.guild.me: nextcord.PermissionOverwrite(view_channel=True)
		}
		await ctx.guild.create_text_channel("ticket-transcripts", overwrites=overwrites, reason="To store all the ticket transcripts")

		

	@commands.command()
	@commands.has_permissions(view_channel=True)
	async def add(self, ctx, user: nextcord.User):
		await ctx.send(f"{user.mention} has been added to the ticket")
		await ctx.channel.set_permissions(user, read_messages=True, send_messages=True, view_channel=True)


class Confirm(nextcord.ui.View):
	def __init__(self, user):
		super().__init__(timeout=None)
		self.user = user

	@nextcord.ui.button(label="Delete Ticket", style=nextcord.ButtonStyle.red, custom_id="close_ticket")
	async def delete(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		if ctx.user != self.user:
			await ctx.response.send_message("This is not your choice to make!")
		channel: nextcord.TextChannel = ctx.channel
		await ctx.channel.delete()
		await ctx.response.send_message(f"{channel.mention} is being deleted")
		transcript_channel: TextChannel = get(ctx.guild.text_channels, name="ticket-transcripts")
		await transcript_channel.send(file=nextcord.File(f"{utils.MainCwd}/temp/tickets/{ctx.guild.id}-{ctx.channel.name.split('-')[1]}.txt"))
		os.remove(f"{utils.MainCwd}/temp/tickets/{ctx.guild.id}-{ctx.channel.name.split('-')[1]}.txt")
		self.stop()


# Setup the Cog
def setup(client):
	client.add_cog(SimpleTicket(client))

