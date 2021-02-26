import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import CommandNotFound
import game


client = commands.Bot(command_prefix = '!', case_insensitive = True)
game = game.Game(client)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print(client.user.id)


    


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith('!start'):
        await game.g_start(message)
    elif message.content.lower().startswith('!used'):
        await game.g_list(message.channel)
    elif len(game.used) == 0:
        await game.g_first_input(message)
    else:
        await game.g_input(message)



client.run('ODEyNDczMjk1OTgyOTUyNTEw.YDBQuA.2a5HP49qf2ULGboVZWlDUyUdxyk')