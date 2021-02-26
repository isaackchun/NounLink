import nltk 
from nltk.corpus import wordnet as wn
import asyncio

nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}


class Node:
    def __init__(self, user):
        self.user = user
        self.next = None


class Game:
    def __init__(self, client):
        self.inGame = False

        self._channel = None
        self._client = client

        self.total_user = 0
        self.current_player = Node(None)
        self.prev_player = Node(None)

        self.used = []
    
    #game start
    async def g_start(self, message):
        print("start initiated")
        if (self.inGame == True):
            await self._channel.send("We are already in game!")

        else:
            self._channel = message.channel
            msg = await self._channel.send("React to join the game!")
            await msg.add_reaction('👍')
            await asyncio.sleep(10)

            #getting list of players who reacted and adding it to linkedlist
            msg = await message.channel.fetch_message(msg.id)
            
            #ptr node
            ptr = Node(None)
            head = Node(None)

            for reaction in msg.reactions:
                if reaction.emoji == '👍':
                    async for user in reaction.users():
                        if user != self._client.user:
                            if self.total_user == 0:
                                head = Node(user)
                                ptr = head
                            else:
                                ptr.next = Node(user)
                                ptr = ptr.next
                            print(ptr.user.mention)
                            self.total_user += 1
            
            #linked list to cycle
            ptr.next = head

            #change it to 2 later
            if self.total_user < 1:
                await message.channel.send("We dont have enough players to play D:")
                return
            else:
                print(self.total_user)
                self.current_player = head
                self.inGame = True
                await message.channel.send("Enter the first noun " + self.current_player.user.mention)


    #checking if first two letters of noun matches last two letter of previous noun
    #if noun, returns true. if not returns false
    def add_noun(self, message):
        prev = self.used[-1]
        if prev[-1:] == message.content[:-1]:
            self.used.append(message.content)
            return True
        return False



    #first input of the game
    async def g_first_input(self, message):
        if message.author == self.current_player.user:
            if message.content in nouns:
                self.used.append(message.content)
                await message.add_reaction('✅')
                self.prev_player = self.current_player
                self.current_player = self.current_player.next
                await message.channel.send("Enter the next " + self.current_player.user.mention)

            else:
                await message.add_reaction('❌')
                await message.channel.send("<" + message.content + ">"+" is not noun")
        
    
    
    #input other than first input must be from user who is not the previous user
    async def g_input(self, message):
        if message.author == self.current_player.user:
            if message.content in nouns:
                if message.content in self.used:
                    await message.add_reaction('❌')
                    await self._channel.send("<" + message.content + ">" + " is already used!")
                elif self.add_noun(message) == False:
                    await message.add_reaction('❌')
                    await self._channel.send("<" + message.content + ">" + " doesnt work with " + "<" + self.used[-1] + ">")
                else:
                    await message.add_reaction('✅')
                    self.prev_player = self.current_player
                    self.current_player = self.current_player.next
                    await message.channel.send("Enter the next " + self.current_player.user.mention)
            else:
                await message.add_reaction('❌')
                await self._channel.send("<" + message.content + ">"+" is not noun")

    
    #prints all previously used nouns
    async def g_list(self, channel):
        if self.inGame == False:
            await channel.send("Please start the game to use this command!")
        else:
            for x in range(len(self.used)):
                await channel.send (self.used[x])

