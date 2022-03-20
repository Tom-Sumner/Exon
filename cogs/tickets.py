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

class Button(nextcord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)

	@nextcord.ui.button(label="New Ticket", style=nextcord.ButtonStyle.blurple, custom_id="create_ticket")
	async def create(self, button: nextcord.ui.Button, ctx: Interaction):
		await ctx.response.defer(ephemeral=True)

		ticket_created_embed = nextcord.Embed(
			title="Ticket Processed",
			description=f"""Hey {ctx.user.name}! Thanks for opening a ticket with us today.
			Please describe your enquiry and our team will respond shortly. We thank you in advance for your patience."""
		)

		overwrites = {
			ctx.guild.default_role: nextcord.PermissionOverwrite(view_channel=False),
			ctx.user: nextcord.PermissionOverwrite(view_channel=True),
			ctx.guild.me: nextcord.PermissionOverwrite(view_channel=True)
		}

		ticket = await ctx.channel.category.create_text_channel(f"{ctx.user.display_name}'s ticket", overwrites=overwrites)

		await ticket.send(ctx.user.mention, embed=ticket_created_embed)
		self.stop()

# Define the Cog
class SimpleTicket(commands.Cog):
	def __init__(self, client):
		self.client: nextcord.Client = client
		self.client.persistent_views_added = False

	@commands.Cog.listener(name="on_ready")
	async def on_ready(self):
		if not self.client.persistent_views_added:
			self.client.add_view(Button())
			self.persistent_views_added = True

	@commands.command()
	@commands.is_owner()
	async def sendticket(self, ctx):
		embed = nextcord.Embed(
			title="Contact Support",
			description="Click the button below to open a ticket"
		)
		await ctx.send(embed=embed, view=Button())


	@commands.command()
	@commands.has_guild_permissions(administrator=True)
	async def close(self, ctx):
		await ctx.send("Please confirm to delete the message", view=Confirm(ctx.author))


class Confirm(nextcord.ui.View):
	def __init__(self, user):
		super().__init__()
		self.value = None
		self.user = user

	@nextcord.ui.button(label="Delete Ticket", style=nextcord.ButtonStyle.red)
	async def delete(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		if ctx.user != self.user:
			await ctx.response.send_message("This is not your choice to make!")
		channel: nextcord.TextChannel = ctx.channel
		await ctx.response.send_message(f"{channel.mention} is being deleted")
		asyncio.sleep(5)
		if channel.name.endswith("ticket"):
				await ctx.channel.delete()
		self.stop()

	@nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.green)
	async def cancel(self, button: nextcord.ui.Button, ctx: nextcord.Interaction):
		if ctx.user != self.user:
			await ctx.response.send_message("This is not your choice to make!")
		channel: nextcord.TextChannel = ctx.channel
		await ctx.response.send_message("Canceled")
		await ctx.delete_original_message()
		
		self.value = True
		self.stop()


# Setup the Cog
def setup(client):
	client.add_cog(SimpleTicket(client))