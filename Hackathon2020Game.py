from nltk.corpus import wordnet
from bs4 import BeautifulSoup
import json
'''
This is a text based adventure game that uses the Natural Language Toolkit for Python 
by comparing human inputs and the synonyms of a list of commands. 
'''
class Item:
    def __init__(self,name,description):
        self.name=name
        self.description=description



class Room:
    def __init__(self,description):
        self.description=description
        self.exits={}
        self.items=[]

    def addExit(self,room,direction):
        self.exits[direction]=room

    def getExit(self,direction):
        return self.exits[direction]

    def fullDescription(self):
        returnStr="You are "+self.description+".\nExits are:\n   "
        x=0
        for key in self.exits:
            returnStr+=key
            if x!=len(self.exits)-1 and len(self.exits)>2:
                returnStr+=","
            if x!=len(self.exits)-1:
                returnStr+=" "
            if x==len(self.exits)-2:
                returnStr+="and "
            x+=1
        returnStr+=".\n"
        if len(self.items)>0:
            returnStr+="In the room, you can see:\n"
            for item in self.items:
                returnStr+="   "+item.name+"\n"
        return returnStr
        
    def addItem(self,item):
        self.items.append(item)



class Player:
    def __init__(self):
        self.currentRoom = None
        self.inventory = []

    def setCurrentRoom(self,currentRoom):
        self.currentRoom=currentRoom

    def walk(self, command):
        direction=command.wordList[0]
        if direction == None:
            printStr = "Go Where? \n"
        else:
            try:
                nextRoom = self.currentRoom.getExit(direction)
                self.currentRoom=nextRoom
                printStr=self.currentRoom.fullDescription() 
            except:
                printStr="There is no room."
        return printStr

    def take(self, command):
        if command.wordList[0]==None:
            return "Take what?"
        else:
            for value in self.currentRoom.items:
                itemToTake = self.currentRoom.items[self.currentRoom.items.index(value)]
                if itemToTake.name.split() == command.wordList:
                    self.inventory.append(itemToTake)
                    self.currentRoom.items.remove(itemToTake)
                    return "you have taken " + itemToTake.name
            return "This item does not exist."

    def drop(self,item):
        if command.wordList[0]==None:
                return "Take what?"
        else:
            for value in self.currentRoom.items:
                itemToDrop = self.inventory[self.inventory.index(value)]
                if itemToDrop.name.split() == command.wordList:
                    self.inventory.remove(itemToDrop)
                    self.currentRoom.items.append(itemToDrop)
                    return "you have dropped " + itemToDrop.name
            return "This item is not in your inventory."

    def getInventory(self,command):
        if len(self.inventory)>0:
            printStr="Inventory:\n"
            for item in self.inventory:
                printStr+="   "+item.name
        else:
            printStr="There is nothing in your inventory."
        return printStr



class Command:
    def __init__(self,wordList):
        self.commandWord = wordList[0]
        self.wordList = wordList[1:]
        
    def isUnknown(self):
        return (self.commandWord == None)
        
    def hasOtherWords(self):
        return (self.wordList[1] != None)
        
        

class CommandWords:
    validCommands=["quit","look","go","take","drop","inventory","attack","talk","inspect","use"]
    allSynonyms={}
    for value in validCommands:
        allSynonyms[value]=[]
        for syn in wordnet.synsets(value):
            for lemma in syn.lemmas():
                allSynonyms[value].append(lemma.name())
        for synonym in allSynonyms[value]:
            newSyn=synonym.replace("_"," ")
            allSynonyms[value].insert(allSynonyms[value].index(synonym),newSyn)
            allSynonyms[value].remove(synonym)
        
    def checkCommand(self, command):
        for command in self.validCommands:
           if command in self.allSynonyms[command]:
                return True
        return False



class Parser:
    commands = CommandWords()
    def getCommand(self):
        user = input("> ")
        wordList = user.split()
        if self.commands.checkCommand(wordList[0]):
            return Command(wordList)
        else:
            return Command[None, None]



player=Player()
parser=Parser()
def createRooms():
    westRoom=Room("in a room to the west")
    eastRoom=Room("in a room to the east")
    northRoom=Room("in a room to the north")
    southRoom=Room("in a room to the south")
    centerRoom=Room("in a room in the center")
    centerRoom.addExit(westRoom,"west")
    centerRoom.addExit(eastRoom,"east")
    centerRoom.addExit(northRoom,"north")
    centerRoom.addExit(southRoom,"south")
    westRoom.addExit(centerRoom,"east")
    eastRoom.addExit(centerRoom,"west")
    northRoom.addExit(centerRoom,"south")
    southRoom.addExit(centerRoom,"north")
    southRoom.addItem(Item("funny word","it is the funnee word"))
    player.setCurrentRoom(centerRoom)

def play():
    print(player.currentRoom.fullDescription())
    finished = False
    while finished == False:
        command = parser.getCommand()
        finished = processCommand(command)
    print("bye bye")

def processCommand(command):
    wantToQuit=False
    if command.isUnknown():
        print("What.")
        return False
    commandWord=command.commandWord
    if commandWord in CommandWords.allSynonyms["go"]:
        print(player.walk(command))
    elif commandWord in CommandWords.allSynonyms["quit"]:
        wantToQuit=quit(command)
    elif commandWord in CommandWords.allSynonyms["look"]:
        print(player.currentRoom.fullDescription())
    elif commandWord in CommandWords.allSynonyms["take"]:
        print(player.take(command))
    elif commandWord in CommandWords.allSynonyms["inventory"]:
        print(player.getInventory(command))
    return wantToQuit

def quit(command):
    if command.wordList[1:]!=None:
        print("Quit what?")
        return False
    else:
        print("bye bye")
        return True

createRooms()
play()