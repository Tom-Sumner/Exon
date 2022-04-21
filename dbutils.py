import nextcord, json
import sqlite3, os, utils, asyncio
from asyncio import run
from utils import MainCwd
from sqlite3 import Error

connection = sqlite3.connect(r"storage.sqlite3", isolation_level=None)
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
	c.execute(f"insert or ignore into settings values ({guild_id}, '.', null, 'Welcome ;user;, to ;guild;!', null)")
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

def fetch_all_prefix():
	result = c.execute(f"select settings.prefix from settings")
	results = [''.join(tuple(i)) for i in result.fetchall()]
	return results

def fetch_all_guilds():
	result = c.execute(f"select * from settings")
	return result.fetchall()

def update_prefix(guild_id: int, prefix: str):
	check(guild_id)
	c.execute(f"update settings set prefix = '{prefix}' where id = {guild_id}")
	connection.commit()

def update_log_channel(guild_id: int, channel: int):
	check(guild_id)
	c.execute(f"update settings set [log channel] = {channel} where id = {guild_id}")
	connection.commit()

def fetch_log_channel(guild_id: int):
	check(guild_id)
	result = c.execute(f"select settings.[log channel] from settings where id = {guild_id}")
	channel = int(result.fetchone()[0])
	return channel

def update_ticket_count(guild_id: int, count: int):
	check(guild_id)
	c.execute(f"update settings set [ticket count] = {count} where id = {guild_id}")
	connection.commit()

def fetch_ticket_count(guild_id: int):
	check(guild_id)
	result = c.execute(f"select settings.[ticket count] from settings where id = {guild_id}")
	count = int(result.fetchone()[0])
	return count

def fetch_welcome_message(guild_id: int):
	check(guild_id)
	result = c.execute(f"select settings.[welcome msg] from settings where id = {guild_id}")
	message = "".join(tuple(result.fetchone()))
	return message

def update_welcome_message(guild_id: int, message: str):
	check(guild_id)
	c.execute(f"update settings set [welcome msg] = '{message}' where id = {guild_id}")
	connection.commit()