from nltk.corpus import wordnet
from bs4 import BeautifulSoup
class Player:
    currentRoom=None
    def walk(self, command):
        direction=command.wordList[1:]
        if direction == None:
            print = "Go Where? \n"
        else:
            try:
                nextRoom = self.currentRoom.exits.get(direction.lower())
                self.currentRoom=nextRoom
                print=self.currentRoom.fullDescription()
            except:
                print="There is no room"
class Room:
    exits={}
    description=""
    def __init__(self,description):
        self.description=description
    def addExit(self,room,direction):
        self.exits[direction]=room
    def fullDescription(self):
        returnStr="You are "+self.description+".\nExits are:\n   "
        x=0
        for key in self.exits:
            returnStr+=key
            if x!=len(self.exits)-1 and len(self.exits)>2:
                returnStr+=","
            returnStr+=" "
            if x==len(self.exits)-2:
                returnStr+="and "
            x+=1
        return returnStr
class Parser:
    commands = CommandWords()
    def getCommand(self):
        user = input("> ")
        wordList = user.split()
        if commands.checkCommand(wordList[0]):
            return Command(wordList)
        else:
            return Command[None, None]
        
class Command:
    commandWord = ""
    def __init__(self,wordList):
        commandWord = wordList[0]
        self.wordList = wordList[1:]
    def isUnknown(self):
        return (commandWord == None)
    def hasOtherWords(self):
        return (self.wordList[1] != None)
class CommandWords:
    validCommands=["go","take","drop","inventory","attack","talk","inspect"]
    def checkCommand(self, command):
        for command in self.validCommands:
            synonyms=[]
            for syn in wordnet.synsets(command):
                for lemma in syn.lemmas():
                    synonyms.append(lemma.name())
            for synonym in synonyms:
                newSyn=synonym.replace("_"," ")
                synonyms.insert(synonyms.index(synonym),newSyn)
                synonyms.remove(synonym)
            if command in synonyms:
                return True
        return False
