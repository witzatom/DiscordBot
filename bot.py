import discord
import asyncio
import re
import model
import json

client = discord.Client()

bitchCounter = model.JsonDictionary('lilbitch')

handles = {
	re.compile('^!hello$'): model.StringReply('Hello {0.author.mention}'),
	re.compile('^!help$'): model.StringReply('Try !hello, !top or !source'),
	re.compile('^!source$'): model.StringReply('My source is located at https://github.com/Tommassino/LilBitchBot'),
	re.compile('.*lil.*bitch.*'): model.UserIncrement(bitchCounter),
	re.compile('.*who.*lil.*bitch.*'): model.ReplyTop(bitchCounter),
	re.compile('^!top$'): model.ListTop(bitchCounter,3)
}

@client.event
@asyncio.coroutine
def on_message(message):
	# we do not want the bot to reply to itself
	if message.author == client.user:
		return

	for regexp in handles:
		match = regexp.match(message.content)
		if match:
			msg = handles[regexp](message,match)
			if msg:
				yield from client.send_message(message.channel, msg)

@client.event
@asyncio.coroutine
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

config = {}

with open('config.json','r') as fp:
	config=json.load(fp)


client.run(config['token'])
