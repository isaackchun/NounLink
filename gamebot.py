import discord
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands import CommandNotFound
import game


client = commands.Bot(command_prefix = '!', case_insensitive = True)
server_list = []

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    print(client.user.id)

def inGame(message):
    for x in server_list:
        if x._channel == message.channel:
            return x
    return None
    


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    gaming = inGame(message)

    #game has not been initated
    if gaming == None:
        if message.content.lower().startswith('!start'):
            new = game.Game(message.channel,client)
            server_list.append(new)
            await new.g_start(message)
        
        elif message.content.lower().startswith('!'):
             await message.channel.send("We haven't started the game!\nTo start type: !start")




    #if game has been initated
    else:
        if message.content.lower().startswith('!used'):
            await gaming.usedList()
        elif len(gaming.used) == 0:
            await gaming.g_first_input(message)
        else:
            await gaming.g_input(message)

        if gaming.end == True:
            server_list.remove(gaming)




client.run('insert token here')