#Imports
import discord
import os
from discord.ext import commands, tasks
import asyncio
import random
from discord.utils import find
from discord.utils import get
from os import listdir, path
from discord import File
import json
from random import randrange
from asyncio import sleep
import math

#TEST IMPORTS

#Bot permissions
intents=intents=discord.Intents.all()

#Basic command prefix and disabling help command
client = commands.Bot(command_prefix = "dm!", help_command=None, case_insensitive=True, intents = intents)

#Defining client
def __init__(self, client):
	self.client = client


#ON-READY STATUS
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Greetings | dm!help"))

    global boticon
    boticon = "https://cdn.discordapp.com/avatars/880775465042849834/6d01680ef2127f8f86dc4265dfbf86db.webp?size=128"

    _loadstats()
    _loadminigames()
    _loadingame()

    print("Main online!")



#Help Command
@client.command()
async def help(ctx):
    #Generates embed
    hembed = discord.Embed(title="Help commands!",description="`help`, `stats`, `play`, `cm`",timestamp=ctx.message.created_at)
    hembed.set_footer(text="Discord Minigames!",icon_url=boticon)

    #Sends Embed
    await ctx.send(embed=hembed)


#Stats/Profile Command
@client.command(aliases=["profile","prof"])
async def stats(ctx):
    
    #Stuff with ID's
    userID = str(ctx.author.id)
    _loadstats()

    #Check for user ID
    chrRes = _checkid(userID)
    if chrRes == False:

        #Generates new json entry if no ID is found
        _addid(userID)
        await ctx.send("You do not have an ID, i've just created one for you! (Run the command again)")
        return

    else:

        #Embed variables
        uMatches = stats[userID]["Matches"]
        uWins = stats[userID]["Wins"]
        uLoses = stats[userID]["Loses"]
        uPoints = stats[userID]["Points"]

        #Generates embed
        statEmbed = discord.Embed(title=f"{ctx.author.name}'s Stats",description="",timestamp=ctx.message.created_at)
        statEmbed.add_field(name="Matches Played:",value=uMatches, inline=False)
        statEmbed.add_field(name="Matches Won:",value=uWins, inline=False)
        statEmbed.add_field(name="Matches Lost:",value=uLoses, inline=False)
        statEmbed.add_field(name="DM! Points:",value=uPoints, inline=False)
        statEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)

        #Sends Embed
        await ctx.send(embed=statEmbed)
    

#Game Command
@client.command(aliases=["game","start"])
async def play(ctx, user2: discord.User=None, user3: discord.User=None, user4: discord.User=None):
    #Startup variables
    channel = ctx.channel
    player1=ctx.author
    player2, player3, player4, gameType, gameError = _checkuser(user2,user3,user4)
    print(player2,player3,player4, gameType)

    #Check if user is duplicate
    if player1 == player2 or player1 == player3 or player1 == player4:
        gameError="Duplicate user found, please do not mention a player more than two times."
    if gameError != None:
        await ctx.send(gameError)
        print(gameError)
        return

    def checkreaction(reaction, rUser):
        return rUser == player1 and str(reaction.emoji) == '✅' or rUser == player2 and str(reaction.emoji) == '✅' or rUser == player3 and str(reaction.emoji) == '✅' or rUser == player4 and str(reaction.emoji) == '✅'

    def checkmessage(message):
        return message.channel == channel

    #User confirmations
    confirmations = gameType-1
    player2Reacted = False
    player3Reacted = False
    player4Reacted = False

    #Embed generation
    confirmEmbed = discord.Embed(title="Ready to play?",description="*React to confirm!*",timestamp=ctx.message.created_at)
    confirmEmbed.add_field(name=f"Player 1: {player1.name}",value="Status: Ready! :white_check_mark:", inline=False)
    if player2 != None:
        confirmEmbed.add_field(name=f"Player 2: {player2.name}",value="Status: Not ready! :x:", inline=False)
    if player3 != None:
        confirmEmbed.add_field(name=f"Player 3: {player3.name}",value="Status: Not ready! :x:", inline=False)
    if player4 != None:
        confirmEmbed.add_field(name=f"Player 4: {player4.name}",value="Status: Not ready! :x:", inline=False)

    confirmEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
    cEmbed = await ctx.send(embed=confirmEmbed)
    await cEmbed.add_reaction("✅")

    #Loop
    while confirmations > 0:
        try:
            reaction, rUser = await client.wait_for('reaction_add', timeout=20.0, check=checkreaction)

        #Result
        except asyncio.TimeoutError:
            await ctx.send("Someone didn't confirm on time...")
            return

        else:
            await cEmbed.remove_reaction("✅", rUser)
            #Generates embed with people that reacted and edits the lastest embed
            procedualEmbed = discord.Embed(title="Ready to play?",description="*React to confirm!*",timestamp=ctx.message.created_at)
            procedualEmbed.add_field(name=f"Player 1: {player1.name}",value="Status: Ready! :white_check_mark:", inline=False)

            if player2 != None and rUser.id == player2.id and player2Reacted == False:
                procedualEmbed.add_field(name=f"Player 2: {player2.name}",value="Status: Ready! :white_check_mark:", inline=False)
                confirmations = confirmations - 1
                player2Reacted = True
            elif player2 != None and rUser.id != player2.id and player2Reacted == False:
                procedualEmbed.add_field(name=f"Player 2: {player2.name}",value="Status: Not ready! :x:", inline=False)
            elif player2 != None and player2Reacted == True:
                procedualEmbed.add_field(name=f"Player 2: {player2.name}",value="Status: Ready! :white_check_mark:", inline=False)

            if player3 != None and rUser.id == player3.id and player3Reacted == False:
                procedualEmbed.add_field(name=f"Player 3: {player3.name}",value="Status: Ready! :white_check_mark:", inline=False)
                confirmations = confirmations - 1
                player3Reacted = True
            elif player3 != None and rUser.id != player3.id and player3Reacted == False:
                procedualEmbed.add_field(name=f"Player 3: {player3.name}",value="Status: Not ready! :x:", inline=False)
            elif player3 != None and player3Reacted == True:
                procedualEmbed.add_field(name=f"Player 3: {player3.name}",value="Status: Ready! :white_check_mark:", inline=False)

            if player4 != None and rUser.id == player4.id and player4Reacted == False:
                procedualEmbed.add_field(name=f"Player 4: {player4.name}",value="Status: Ready! :white_check_mark:", inline=False)
                confirmations = confirmations - 1
                player4Reacted = True
            elif player4 != None and rUser.id != player4.id and player4Reacted == False:
                procedualEmbed.add_field(name=f"Player 4: {player4.name}",value="Status: Not ready! :x:", inline=False)
            elif player4 != None and player4Reacted == True:
                procedualEmbed.add_field(name=f"Player 4: {player4.name}",value="Status: Ready! :white_check_mark:", inline=False)

            procedualEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
            await cEmbed.edit(embed=procedualEmbed)

    await cEmbed.clear_reactions()
    #Loop is over, now ask for the number of minigames that will be played to ALL players
    #User minigames
    askMinigame = gameType
    numListMinigames=[]
    player1Minigame = False
    player2Minigame = False
    player3Minigame = False
    player4Minigame = False

    #Typing thing, looks cool
    await ctx.trigger_typing()
    await asyncio.sleep(1.6)
    waitMsg = await ctx.send("Looks like everyone is ready!")
    await asyncio.sleep(1.9)

    #Minigame embed
    minigameEmbed = discord.Embed(title="Minigames played",description="Alright!, now it's time to decide how many minigames there will be played. Please everyone input a number from 5-20 and one player's number will be chosen!",timestamp=ctx.message.created_at)
    minigameEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
    await cEmbed.edit(embed=minigameEmbed)

    await waitMsg.delete()

    #Loop
    while askMinigame > 0:
        try:
            message = await client.wait_for('message', timeout=25.0, check=checkmessage)

        #Result
        except asyncio.TimeoutError:
            await ctx.send("Someone didn't decide on time...")
            return

        else:
            #Checking if the message was made by a player or not
            mNumber = _RepresentInt(message.content)
            if mNumber == True:
                if message.author.id == player1.id and player1Minigame == False and int(message.content) > 4 and int(message.content) < 21:
                    numListMinigames.append(message.content)
                    askMinigame = askMinigame -1
                    player1Minigame = True
                    await ctx.send("Number saved!")

                if player2 != None and message.author.id == player2.id and player2Minigame == False and int(message.content) > 4 and int(message.content) < 21:
                    numListMinigames.append(message.content)
                    askMinigame = askMinigame -1
                    player2Minigame = True
                    await ctx.send("Number saved!")

                if player3 != None and message.author.id == player3.id and player3Minigame == False and int(message.content) > 4 and int(message.content) < 21:
                    numListMinigames.append(message.content)
                    askMinigame = askMinigame -1
                    player3Minigame = True
                    await ctx.send("Number saved!")

                if player4 != None and message.author.id == player4.id and player4Minigame == False and int(message.content) > 4 and int(message.content) < 21:
                    numListMinigames.append(message.content)
                    askMinigame = askMinigame -1
                    player4Minigame = True
                    await ctx.send("Number saved!")

                print(numListMinigames)

    #Loop ends, random number is chosen and announced
    numMiniRand = randrange(0,gameType)
    numMinigames = int(numListMinigames[numMiniRand])

    #Typing thing, looks cool
    await ctx.trigger_typing()
    await asyncio.sleep(1.8)

    #Announce Number of minigames
    preMinigameEmbed = discord.Embed(title="Number chosen",description="Ok, the number of minigames that will be played is...",timestamp=ctx.message.created_at)
    preMinigameEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
    preMiniEmbed = await ctx.send(embed=preMinigameEmbed)

    await asyncio.sleep(3.0)
    MinigameEmbed = discord.Embed(title="Number chosen",description=f"{numMinigames} minigames!",timestamp=ctx.message.created_at)
    MinigameEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
    await preMiniEmbed.edit(embed=MinigameEmbed)

    #Typing thing, looks cool
    await asyncio.sleep(1.1)
    await ctx.send("Let the games begin...")

    #Adding player to ingame.json (One time only)
    await ctx.trigger_typing()
    _loadingame()
    gameInstance = player1.name+str(randrange(1,1000000000))

    #Checks for the gametype and adds to json
    if gameType == 1:
        ingame[gameInstance] = {"p1": {"id": player1.id, "miniPoints": 0, "miniWins": 0}, "numMinigames": numMinigames, "countMini": 0, "speedup": 0}

    if gameType == 2:
        ingame[gameInstance] = {"p1": {"id": player1.id, "miniPoints": 0, "miniWins": 0}, "p2": {"id": player2.id, "miniPoints": 0, "miniWins": 0}, "numMinigames": numMinigames, "countMini": 0, "speedup": 0}

    if gameType == 3:
        ingame[gameInstance] = {"p1": {"id": player1.id, "miniPoints": 0, "miniWins": 0}, "p2": {"id": player2.id, "miniPoints": 0, "miniWins": 0}, "p3": {"id": player3.id, "miniPoints": 0, "miniWins": 0}, "numMinigames": numMinigames, "countMini": 0, "speedup": 0}

    if gameType == 4:
        ingame[gameInstance] = {"p1": {"id": player1.id, "miniPoints": 0, "miniWins": 0}, "p2": {"id": player2.id, "miniPoints": 0, "miniWins": 0}, "p3": {"id": player3.id, "miniPoints": 0, "miniWins": 0}, "p4": {"id": player4.id, "miniPoints": 0, "miniWins": 0}, "numMinigames": numMinigames, "countMini": 0, "speedup": 0}

    _saveingame()

    #Minigame Stuff, ALL OF THIS WILL REPEAT ON A LOOP, IT CANNOT BE STOPPED. lmao what a big text wall
    miniPlayed = []
    game = True

    while game == True:
        #Variables
        didItSpeedup = False
        miniCondition1 = ""
        mNumber = False
        player1Minigame = False
        player2Minigame = False
        player3Minigame = False
        player4Minigame = False
        askMinigame = gameType
        winTable = []
        winningID1 = 0
        winningID2 = 0
        winningID3 = 0
        winningID4 = 0

        #Generates random number and chooses minigame
        currentMiniNum = str(randrange(1,2))
    
        #Rerolls if minigame has been already played, if not it gets added to the already played minigames list
        while currentMiniNum in miniPlayed:
            currentMiniNum = str(randrange(1,2))
    
        _loadminigames()
        miniPlayed.append(currentMiniNum)

        #Checks every minigame case and sets some variables
        #All minigames MUST have these 5 variables inside the json
        miniType = minigames[currentMiniNum]["type"]
        miniName = minigames[currentMiniNum]["name"]
        miniDesc = minigames[currentMiniNum]["desc"]
        miniWaitFor = minigames[currentMiniNum]["waitfor"]
        miniTimeout = minigames[currentMiniNum]["timeout"]

        #Game Speedup
        decoyCountMini = int(ingame[gameInstance]["countMini"])
        decoyNumMini = int(ingame[gameInstance]["numMinigames"])
        decoySpeedup = int(ingame[gameInstance]["speedup"])

        decoyNumMini2 = decoyNumMini/2
        decoyNumMini4 = decoyNumMini/4
        decoyNumMini6 = decoyNumMini2+decoyNumMini4

        if decoyCountMini >= decoyNumMini2 and decoySpeedup == 0:
            print("Speedup +1")
            didItSpeedup = True
        elif decoyCountMini >= decoyNumMini6 and decoySpeedup == 0:
            print("Speedup +1")
            didItSpeedup = True
        
        if didItSpeedup == True:
            await asyncio.sleep(1.5)
            speedupEmbed = discord.Embed(title="Speedup",description="The games will be faster now, good luck!",timestamp=ctx.message.created_at)
            speedupEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
            await ctx.send(embed=speedupEmbed)

        #Round embed
        await asyncio.sleep(2.2)
        playEmbed = discord.Embed(title=f"Round {decoyCountMini+1}!",description="Get ready...",timestamp=ctx.message.created_at)
        playEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
        playEmbedEdit = await ctx.send(embed=playEmbed)

        #Sends the embed, minigame can be played        
        await asyncio.sleep(miniWaitFor)
        playEmbed = discord.Embed(title=miniName,description=miniDesc,timestamp=ctx.message.created_at)
        playEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
        await playEmbedEdit.edit(embed=playEmbed)


        #Fastest message content
        if miniType == "fastest_message_content":
            miniCondition1 = minigames[currentMiniNum]["message"]

            #Another loop
            while askMinigame > 0:
                try:
                    message = await client.wait_for('message', timeout=miniTimeout, check=checkmessage)

                #Result
                except asyncio.TimeoutError:
                    await ctx.send("Too slow!")
                else:
                    #Checking if the message was made by a player or not
                    if message.content.lower() == miniCondition1:
                        if message.author.id == player1.id and player1Minigame == False:
                                askMinigame = askMinigame -1
                                player1Minigame = True
                                winTable.append(player1.id)

                        if player2 != None and message.author.id == player2.id and player2Minigame == False:
                                askMinigame = askMinigame -1
                                player2Minigame = True
                                winTable.append(player2.id)

                        if player3 != None and message.author.id == player3.id and player3Minigame == False:
                                askMinigame = askMinigame -1
                                player3Minigame = True
                                winTable.append(player3.id)

                        if player4 != None and message.author.id == player4.id and player4Minigame == False:
                                askMinigame = askMinigame -1
                                player4Minigame = True
                                winTable.append(player4.id)

        elif miniType == "fastest_reaction_randomized":
            miniCondition1 = minigames[currentMiniNum]["reaction"]
        
        #Minigame ended
        await asyncio.sleep(0.5)

        #Adding scores and wins to json file
        playersInWinning=["p1"]
        winningID1 = int(winTable[0])

        if gameType == 2:
            winningID2 = int(winTable[1])
            playersInWinning.append("p2")

        if gameType == 3:
            winningID3 = int(winTable[2])
            playersInWinning.append("p3")

        if gameType == 4:
            playersInWinning.append("p4")


        for x in playersInWinning:
            if winningID1 in ingame[gameInstance][x]["id"]:
                ingame[gameInstance][x]["miniPoints"] = ingame[gameInstance][x]["miniPoints"] + 3
                ingame[gameInstance][x]["miniWins"] = ingame[gameInstance][x]["miniWins"] + 1

            if gameType > 1:
                if winningID2 in ingame[gameInstance][x]["id"]:
                    ingame[gameInstance][x][winningID2]["miniPoints"] = ingame[gameInstance][x]["miniPoints"] + 2

            if gameType > 2:
                if winningID3 in ingame[gameInstance][x]["id"]:
                    ingame[gameInstance][x]["miniPoints"] = ingame[gameInstance][x]["miniPoints"] + 1

        _saveingame()

        #Minigame Embed
        miniPointsp1 = ingame[gameInstance]["p1"]["miniPoints"]

        statsEmbed = discord.Embed(title=f"Minigame stats",description="Here are the current round winners!",timestamp=ctx.message.created_at)
        statsEmbed.add_field(name=f"{player1.name}'s Score: ",value=miniPointsp1, inline=False)

        if player2 != None:
            miniPointsp2 = ingame[gameInstance]["p2"]["miniPoints"]
            statsEmbed.add_field(name=f"{player2.name}'s Score: ",value=miniPointsp2, inline=False)

        if player3 != None:
            miniPointsp3 = ingame[gameInstance]["p3"]["miniPoints"]
            statsEmbed.add_field(name=f"{player3.name}'s Score: ",value=miniPointsp3, inline=False)

        if player4 != None:
            miniPointsp4 = ingame[gameInstance]["p4"]["miniPoints"]
            statsEmbed.add_field(name=f"{player4.name}'s Score: ",value=miniPointsp4, inline=False)

        statsEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
        statsEmbed = await ctx.send(embed=statsEmbed)

@client.command(aliases=["cm","cmini"])
async def checkminigames(ctx, pos: str):
    #Startup variables
    _loadminigames()

    #Checks specified minigame from json file (STUFF MAY VARY)
    miniCondition2 = None
    miniCondition3 = None
    miniName = minigames[pos]["name"]
    miniType = minigames[pos]["type"]
    miniWaitFor = minigames[pos]["waitfor"]
    miniTimeout = minigames[pos]["timeout"]

    if miniType == "fastest_message_content":
        miniCondition1 = minigames[pos]["message"]

    if miniType == "fastest_reaction":
        miniCondition1 = minigames[pos]["reaction"]

    #The embed
    MiniEmbed = discord.Embed(title="Minigame Information",description="*This is procedually generated and results may vary*",timestamp=ctx.message.created_at)
    MiniEmbed.add_field(name=f"Minigame Name",value=miniName, inline=False)
    MiniEmbed.add_field(name=f"Minigame Type",value=miniType, inline=False)
    MiniEmbed.add_field(name=f"Minigame Condition 1",value=miniCondition1, inline=False)
    MiniEmbed.add_field(name=f"Minigame Condition 2",value=miniCondition2, inline=False)
    MiniEmbed.add_field(name=f"Minigame Condition 3",value=miniCondition3, inline=False)
    MiniEmbed.add_field(name=f"Minigame WaitFor",value=miniWaitFor, inline=False)
    MiniEmbed.add_field(name=f"Minigame Timeout",value=miniTimeout, inline=False)

    MiniEmbed.set_footer(text="Discord Minigames!",icon_url=boticon)
    await ctx.send(embed=MiniEmbed)



#Check if tagged users are correct
def _checkuser(u2,u3,u4):
    #Player variables
    p2=None
    p3=None
    p4=None
    error=None

    #Check if none
    if u2 != None:
        p2="I exist"
    if u3 != None:
        p3="I exist"
    if u4 != None:
        p4="I exist"

    #Check if user is duplicate
    if u2 != None and u2 == u3 or u2 != None and u2 == u4:
        error="Duplicate user found, please do not mention a player more than two times."

    if u3 != None and u3 == u2 or u3 != None and u3 == u4:
        error="Duplicate user found, please do not mention a player more than two times."

    if u4 != None and u4 == u2 or u4 != None and u4 == u3:
        error="Duplicate user found, please do not mention a player more than two times."

    #Game Types
    if p2 == None:
        gType=1

    elif p2 != None and p3 == None:
        gType=2

    elif p2 != None and p3 != None and p4 == None:
        gType=3

    elif p2 != None and p3 != None and p4 != None:
        gType=4

    #Return variables
    return u2, u3, u4, gType, error

#Add ID to database
def _addid(uid):
    stats[uid]={"Matches": 0, "Wins": 0, "Loses": 0, "Points": 0}
    print("I've added ID:",uid,"to the database!")
    _savestats()

#Check if ID is in the database
def _checkid(checkid):
    if checkid in stats:
        checkres=True
    else:
        checkres=False
    return checkres

#Check if something is an integer
def _RepresentInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#Load stats.json
def _loadstats():
    with open("database/stats.json") as f:
        global stats 
        stats = json.load(f)

#Stats Save
def _savestats():
    with open("database/stats.json", 'w+') as f:
        json.dump(stats, f, indent=4)


#Load minigames.json
def _loadminigames():
    with open("database/minigames.json") as f:
        global minigames
        minigames = json.load(f)


#Load ingame.json
def _loadingame():
    with open("database/ingame.json") as f:
        global ingame
        ingame = json.load(f)

#Save ingame.json
def _saveingame():
    with open("database/ingame.json", 'w+') as f:
        json.dump(ingame, f, indent=4)

#Client token
client.run("YOUR TOKEN HERE")