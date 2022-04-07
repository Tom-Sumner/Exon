# Coded By: Tom Sumner
# Date: 07-04-2022
# Github: Tom-Sumner / https://github.com/Tom-Sumner
# Discord: TSumner#5215
# License: MIT
# Note: If you use this code, you MUST credit me in your project.



import nextcord, os, sys, colorama, time, asyncio, json, requests
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
class Osint(commands.Cog):
    def __init__(self, client):
        self.client: nextcord.Client = client

    # Osint social media accounts
    @nextcord.slash_command(name="osint", description="Get information about a discord user")
    async def osint(self, ctx: Interaction, target: nextcord.User):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot OTMxMTU4MjAxNzc5NDg2NzMw.YeAWpw.ZBLhTJaMw--oDRRqKmm5buTQLKI",
        }
        target = self.client.get_user(target.id)
        id = target.id
        response = requests.get(url=f"https://discord.com/api/v9/users/{id}", headers=headers)
        info: dict = response.json()
        info["created at"] = str(target.created_at)
        infomsg = nextcord.Embed(color=EmbedColors.notify, 
        title=f"{target.name}'s Data",
        description="Available data"
        )
        for name, value in info.items():
            if name == "avatar":
                name = "Avatar"
            else:
                FL = name[0]
                name = name.replace(FL, FL.capitalize())
            infomsg.add_field(name=name, value=value, inline=False)
        infomsg.set_footer(text=f"Requested by {ctx.user.display_name}", icon_url=ctx.user.display_avatar.url)
        infomsg.set_thumbnail(url=target.display_avatar.url)

        await ctx.response.send_message(embed=infomsg)




# Setup the Cog
def setup(client):
    client.add_cog(Osint(client))