import nextcord
import sqlite3, os, utils, asyncio
from asyncio import run
from utils import MainCwd
from sqlite3 import Error

connection = sqlite3.connect(r"Working\storage.sqlite3", isolation_level=None)
c = connection.cursor()

def check(guild_id: int):
	result = c.execute(f"select settings.id from settings where id = {guild_id}")
	if result.fetchone() == None:
		default_config(guild_id)
	else:
		pass

def fetch_guild(guild_id):
	check(guild_id)
	result = c.execute(f"select * from settings where settings.id = {guild_id}")
	result = result.fetchall()
	return result

def default_config(guild_id: int):
	c.execute(f"insert or ignore into settings values ({guild_id}, '.', null, 'Welcome ;user;, to ;guild;!')")
	connection.commit()
	return fetch_guild(guild_id)

def fetch_prefix(client:nextcord.Client=None, msg: nextcord.Message=None, guild_id: int=False):
	check(guild_id)
	if not guild_id:
		guild_id = msg.guild.id
	else:
		pass
	result = c.execute(f"select settings.prefix from settings where id = {guild_id}")
	prefix = "".join(tuple(result.fetchone()))
	return prefix

def update_prefix(guild_id: int, prefix: str):
	check(guild_id)
	c.execute(f"update settings set prefix = '{prefix}' where id = {guild_id}")
	connection.commit()
