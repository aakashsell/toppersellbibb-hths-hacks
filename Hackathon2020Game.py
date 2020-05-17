from nltk.corpus import wordnet
from bs4 import BeautifulSoup as bs
import urllib.request
import random
import NPC
import sys
'''
This is a text based adventure game that uses the Natural Language Toolkit for Python 
by comparing human inputs and the synonyms of a list of commands.
'''
timePeriods = ["1940s","1980s","colonial"]
timePeriod=random.choice(timePeriods)
#npc = NPC.NPC(timePeriod)

locked=True

class Item:
    def __init__(self,name,description,type,value): # 0 - weapon (damage), 1 - Food (health), 2 - keys, 3 - money, 4 - other
        self.name=name
        self.description=description
        self.type = type
        self.value=0
        self.health=0
        self.damage=0
        if self.type == 0:
            self.damage = value
        elif self.type == 1:
            self.health = value
        elif self.type == 3:
            self.value = value
    def use(self,player):
        if self.type==1:
            if player.hp+self.health>player.hpMax:
                healNum=player.hpMax-player.hp
                player.hp=100
            else:
                healNum=self.health
                player.hp+=self.health
            print="You ate the "+self.name+" and healed "+healNum+" hp!"
        elif self.type==0:
            if not inBattle:
                print="You can't use that here."
            else:
                print="How..."
        elif self.type==3 or self.type==2 or self.type==4:
            print="Whatcha gonna do with that here?"
        return print
            

itemList = []
if timePeriod == "colonial":
    itemList.append(Item("arrow","a discarded arrow on the ground",0,7))
    itemList.append(Item("knife","a small, sharp knife",0,15))
    itemList.append(Item("spear","a crudely made spear with a metal tip",0,20))
    itemList.append(Item("berries","a cluster of bright red berries freshly picked from a tree",1,10))
    itemList.append(Item("fish","a large, freshly caught fish",1,20))
    itemList.append(Item("corn","a regular ear of corn",1,25))
    itemList.append(Item("coin","an intricately engraved coin",3,1))
    itemList.append(Item("coins","a collection of coins",3,5))
    itemList.append(Item("hat","a classic pilgrim hat with the distinctive buckle",4,0))
    itemList.append(Item("key","a large metal key",2,0))
elif timePeriod=="1940s":
    itemList.append(Item("high-heeled shoe","a lonely high-heeled shoe",0,8))
    itemList.append(Item("crowbar","a sturdy steel crowbar, perfect for bashing someone's skull in...",0,15))
    itemList.append(Item("pistol","a pistol",0,25))
    itemList.append(Item("cigarette","a cigarette laying pristine on the floor",1,-5))
    itemList.append(Item("Mike & Ike","a box of classic Mike & Ike",1,20))
    itemList.append(Item("Spam","a can of Spam, unopened, ready to be consumed",1,20))
    itemList.append(Item("cash","some forgotten cash",3,0))
    itemList.append(Item("stack of cash","a stack of cash",3,0))
    itemList.append(Item("telephone","an old dial-up telephone",4,0))
    itemList.append(Item("key","a labeled key for access to the prop room of the studio",2,0))
elif timePeriod == "1980s":
    itemList.append(Item("bat","a sturdy baseball bat with a steel handle",0,10))
    itemList.append(Item("knife","a sharp knife with potent cutting power",0,15))
    itemList.append(Item("handgun","a handgun out in the open. Who could be so careless?",0,25))
    itemList.append(Item("cigar","a cigar that seems to have not been used. Bad for your health",1,-5))
    itemList.append(Item("apple","a crisp, red apple. Effective against doctors",1,15))
    itemList.append(Item("hamburger","a hamburger wrapped in familiar, arch-decorated wrapping paper",1,25))
    itemList.append(Item("money","a crisp five-dollar bill",3,5))
    itemList.append(Item("wad of cash","a wad of cash",3,25))
    itemList.append(Item("tape","a used roll of Scotch tape",4,0))
    itemList.append(Item("key","an unlabeled key",2,0))



class Room:
    def __init__(self):
        self.exits={}
        self.items=[]
        self.requiresKey={}
        self.description = ""
        self.npcs = []

    def setDescription(self,desc):
        self.description =  desc

    def addExit(self,room,requiresKey,direction):
        self.exits[direction]=room
        self.requiresKey[direction]=requiresKey

    def getExit(self,direction):
        return self.exits[direction]

    def fullDescription(self):
        returnStr="You are "+self.description+"\nExits are:\n   "
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
                returnStr+="   "+item.description+"\n"
        if len(self.npcs)>0:
            if len(self.npcs)>1:
                returnStr+="In the room there are also "+str(len(self.npcs))+" people:\n"
            else:
                returnStr+="In the room there is also 1 person:\n"
            for npc in self.npcs:
                returnStr+="   "+npc.name+"\n"
        return returnStr
    def addItem(self,item):
        self.items.append(item)

    def addNPC(self,npc):
        self.npcs.append(npc)



class Player:
    def __init__(self):
        self.inventory=[]
        self.hp=100
        self.hpMax=self.hp
        self.equipped=Item("fists","fists. That's just about as simple as you can get",0,5)
        self.previousRoom=None
        
    def setCurrentRoom(self,currentRoom):
        self.currentRoom=currentRoom

    def walk(self, command):
        direction=command.wordList[0]
        if direction == None:
            printStr = "Go Where? \n"
        else:
            try:
                if self.currentRoom.requiresKey[direction]:
                    keyFound=False
                    for item in self.inventory:
                        if item.name=="key":
                            keyFound=True
                    if not keyFound:
                        if timePeriod == "1980s":
                            printStr = "You approach a door to the building to the west of the Watergate building, and when you attempt to open it, the knob doesn't budge. You figure there is a key laying about somewhere."
                        elif timePeriod == "1940s":
                            printStr = "You approach a door labeled \"Prop Shed\", and when you try to turn the knob it stays in place. You figure there is a key laying about somewhere."
                        elif timePeriod == "colonial":
                            printStr = "You attempt to walk west but you are blocked by a group of people and the door to the town hall. The door is locked and blocked by a guard."
                        printStr+="\n"+self.currentRoom.fullDescription()
                    else:
                        print("You unlocked the door with your key!")
                        nextRoom = self.currentRoom.getExit(direction.lower())
                        self.previousRoom=currentRoom
                        self.currentRoom=nextRoom
                        printStr="You unlocked the door!\n"
                        printStr+=self.currentRoom.fullDescription()
                else:
                    nextRoom = self.currentRoom.getExit(direction.lower())
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
                if itemToTake.name.lower().split() == command.wordList.lower():
                    self.inventory.append(itemToTake)
                    self.currentRoom.items.remove(itemToTake)
                    return "you have taken the " + itemToTake.name
            return "This item does not exist."

    def drop(self,command):
        if command.wordList[0]==None:
                return "Drop what?"
        else:
            for value in self.inventory:
                itemToDrop = self.inventory[self.inventory.index(value)]
                if itemToDrop.name.lower().split() == command.wordList.lower():
                    self.inventory.remove(itemToDrop)
                    self.currentRoom.items.append(itemToDrop)
                    return "you have dropped the " + itemToDrop.name
            return "This item is not in your inventory."

    def getInventory(self,command):
        if len(self.inventory)>0:
            printStr="Inventory:\n"
            for item in self.inventory:
                printStr+="   "+item.name
        else:
            printStr="There is nothing in your inventory."
        return printStr

    def takeDamage(self,damage):
        self.hp-=damage
            
    def use(self, command):
        if command.wordList[0]==None:
            return "Use what?"
        else:
            for value in self.inventory:
                itemToUse = self.inventory[self.inventory.index(value)]
                if itemToUse.name.lower().split() == command.wordList.lower():
                    self.inventory.remove(itemToUse)
                    itemToUse.use()
                    return "you have used the " + itemToUse.name
            return "This item is not in your inventory."

    def equip(self,command):
        if command.wordList[0]==None:
            return "Equip what?"
        else:
            for value in self.inventory:
                itemToEquip = self.inventory[self.inventory.index(value)]
                if itemToEquip.name.lower().split() == command.wordList.lower():
                    if itemToEquip.type==0:
                        self.equipped=itemToEquip
                        return "you have equipped the " + itemToEquip.name
                    else:
                        return "you cannot equip that, as it is not a weapon."
            return "This item is not in your inventory."
    
    def inspect(self,command):
        if command.wordList[0]==None:
            return "inspect what?"
        else:
            for value in self.inventory:
                itemToInspect = self.inventory[self.inventory.index(value)]
                if itemToEquip.name.split() == command.wordList:
                    return itemToEquip.description
            return "This item is not in your inventory."
    



class Command:
    def __init__(self,wordList):
        self.commandWord = wordList[0]
        self.wordList = wordList[1:]
        
    def isUnknown(self):
        return (self.commandWord == None)
        
    def hasOtherWords(self):
        return (self.wordList[1] != None)
        
        

class CommandWords:
    validCommands=["quit","look","go","take","drop","inventory","talk","inspect","use","equip"]
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
        try:
            if self.commands.checkCommand(wordList[0]):
                return Command(wordList)
            else:
                return Command[None, None]
        except:
            return Command([None, None])



inBattle=False

def battle(npc):
    if npc.enemy:
        inBattle=False
        print("Upon entering the room, you see a person named "+npc.name+".")
        line = ""
        if npc.repeat==False:
            line+=npc.line
        else:
            line+=npc.repeatLine
        npc.repeat = True
        print(npc.name+" says to you,\n\""+line+"\"")
        print("You are in battle. The enemy has "+str(npc.hp)+" hp. You must either defeat the enemy or run away.")
        answer = True
        while answer == True:
            choice = input("Would you like to [r]un away or [f]ight?")
            if choice.lower()[0]=="r":
                rand = random.randint(0,1)
                if rand == 0:
                    answer = False
                    print("You have successfully run away, you may now exit the room.")
                    return 0
                elif rand == 1:
                    print("You have failed and taken 5 damage.")
                    player.takeDamage(5)
                    choice = "f"
            if choice.lower()[0] == "f":
                inBattle=True
                answer = False
                
                print("The enemy sees you and you engage in combat.")
                run = True
                while run:
                    damageDealt=random.randint(0,npc.weapon.damage)
                    if damageDealt == 0:
                        print("The enemy missed you! Wow, you're lucky!")
                    else:
                        print("The enemy hit you! It dealt "+damageDealt+" damage!")
                        player.takeDamage(damageDealt)
                    damageDealt=random.randint(player.equipped.damage/2,player.equipped.damage)
                    if damageDealt == player.equipped.damage/2:
                        print("You missed the enemy! Wow, you really need to work on your aim!")
                    else:
                        print("You hit the enemy! You dealt "+damageDealt+" damage!")
                        npc.takeDamage(damageDealt)
                    if player.hp <= 0:
                        inBattle=False
                        print("You have lost, game over...")
                        sys.exit(0)
                    if npc.hp <= 0:
                        inBattle=False
                        print("You have beaten this enemy. Good job.")
                        run = False
                        player.currentRoom.npcs.remove(npc)
                        if npc.hasKey:
                            player.addItem(Item(itemList[-1].name,itemList[-1].description,itemList[-1].type,itemList[-1].value))
                            print("You found a "+itemList[-1].description+" in the enemy's pocket!")
                        return 1
            else:
                print("This is not a valid answer.\n")
    else:
        return 2

def randomNPC():
    if timePeriod == "colonial":
        health = random.randint(25,50)
    elif timePeriod == "1940s":
        health = random.randint(50,100)
    elif timePeriod == "1980s":
        health = random.randint(65,100)
    weapon = random.randint(0,2)
    enemy = random.randint(0,2)
    if enemy == 0:
        isEnemy = True
    else:
        isEnemy = False
    if isEnemy:
        linePossibilities=["You're new around here. Be careful who you bump into.","You never should have come here!","Let's see what you're made of.","You're walking around like you own the place.","If you just turn around, no one will get hurt."]
        repeatLinePossibilities=["I'm itching to fight you.","Back for more?","You know, you should never back down from a fight.","Time to put you in your place!","Someone doesn't know how to listen."]
    else:
        linePossibilities = ["Hello, traveler.","Greetings, stranger.","Who are you?","You're not from around here, are you?","What's with your funny looking clothes?"]
        repeatLinePossibilities = ["Hello again, traveler.","Hello again, stranger.","I still don't entirely trust you.","Now stay on your best behavior.","Now I'm not sure I can believe anything you say."]
    line = random.randint(0,4)
    return NPC.NPC(timePeriod,linePossibilities[line],repeatLinePossibilities[line],health,itemList[weapon],isEnemy,False)

player=Player()
parser=Parser()
def createRooms():
    centerRoom=Room()
    southRoom=Room()
    northRoom=Room()
    lessNorthRoom=Room()
    eastRoom=Room()
    northEastRoom=Room()
    southEastRoom=Room()
    southWestRoom=Room()
    centerRoom.addExit(lessNorthRoom,False,"north")
    centerRoom.addExit(southRoom,False,"south")
    centerRoom.addExit(eastRoom,False,"east")
    eastRoom.addExit(centerRoom,False,"west")
    southRoom.addExit(centerRoom,False,"north")
    southRoom.addExit(southEastRoom,False,"east")
    southRoom.addExit(southWestRoom,True,"west")
    southEastRoom.addExit(southRoom,False,"west")
    southWestRoom.addExit(southRoom,True,"east")
    eastRoom.addExit(northEastRoom,False,"north")
    northEastRoom.addExit(eastRoom,False,"south")
    northRoom.addExit(lessNorthRoom,False,"south")
    lessNorthRoom.addExit(northRoom,False,"north")
    lessNorthRoom.addExit(centerRoom,False,"south")
    rooms=[southRoom,northRoom,lessNorthRoom,eastRoom,northEastRoom,southEastRoom]
    player.setCurrentRoom(centerRoom)
    if timePeriod=="1980s":
        centerRoom.setDescription("in the middle of the road, where you should try not to get hit by a car.")
        southRoom.setDescription("in the Watergate Hotel which is lavish and fancy with many fancy amenities.")
        northRoom.setDescription("in the police station accross from the Watergate hotel monitoring for suspicious activity.")
        lessNorthRoom.setDescription("in the parking lot in front of the police station where numerous Ford Mustangs are parked. There is a Hot Rod parked in the lot.")
        eastRoom.setDescription("in the Watergate office building, where numerous offices such as the Democratic Party's office is located.")
        northEastRoom.setDescription("in a gas station, in which you can fill up your car. You are next to the police station and Watergate office bulding.")
        southEastRoom.setDescription("in the building east of the Watergate hotel.")
        southWestRoom.setDescription("in the building west of the Watergate hotel.")
    elif timePeriod=="1940s":
        centerRoom.setDescription("in the middle square of the hollywood studio where everyone gathers and is the central hub of the studio.")
        southRoom.setDescription("in the main entrance of the studio, this has heavy studio to protect our actors, if you get here at a good time you might even catch a peek at an actor.")
        northRoom.setDescription("in the main studio where all the movies are filmed and the biggest space in the hollywood studio.")
        lessNorthRoom.setDescription("in the room where all the cameras and equipment are housed. Be carefull, this stuff ain't cheep.")
        eastRoom.setDescription("in the room where all the actors get ready for shooting their scenes.")
        northEastRoom.setDescription("in the closet where all the makeup and equipment is stored to get the actors ready.")
        southEastRoom.setDescription("in the place where all the cars are parked for the day. Contains lots of fancy cars from all the rich producers and actors.")
        southWestRoom.setDescription("in the shed where all the props are stored.")
    elif timePeriod=="colonial":
        centerRoom.setDescription("in a small clearing in a forest, where a road travels north to a small Native American village and south to a small town of colonists.")
        southRoom.setDescription("in a town filled with primarily sick and tired residents. You see most out tending to farms and working other jobs.")
        northRoom.setDescription("in a small Native American village that has the air of impending doom covering it like a blanket. You can feel the tensions between the two factions rising.")
        lessNorthRoom.setDescription("in an outside wall going into the Native American tribe. You can see some weapons with blood splattering every inch, and others collecting dust.")
        eastRoom.setDescription("in a dark and gloomy forest, with the sun's warm rays being blocked by the dense leaves of the treese above. Birds sing their songs and wildlife scurries at your feet.")
        northEastRoom.setDescription("in a clearing. It looks as if a massacre has taken place as the body of a deer is being held up by a bloodied colonial soldier.")
        southEastRoom.setDescription("in the eastmost part of the town, where the butcher's shop resides. The area smells of death and you can see the butcher standing outside.")
        southWestRoom.setDescription("in an area near a small building. People are gathering near the town hall as tensions rise concerning the Native American threat that looms on the other side of the forest. Inside, the mayor sits at his table with his head in his hands.")
    for room in rooms:
        num = random.randint(0, 3)
        for times in range(num):
            room.addNPC(randomNPC())
    randRoom=random.randint(0,len(rooms)-1)
    rooms[randRoom].addNPC(NPC.NPC(timePeriod,"Greetings, time traveler. I have been looking for you. Are you ready to die?","You come again time traveler. Face me.",90,Item(itemList[2].name,itemList[2].description,itemList[2].type,itemList[2].value),True,True))
    for room in rooms:
        for n in range(3):
            r=random.randint(0,len(itemList)-2)
            room.addItem(itemList[r])



def intro():
    print("You are a time traveler who is stuck in the " + timePeriod + " time period.")
    print("You must interact with the important people from this time to get your time machine working again and get back home.")
    if timePeriod=="1980s":
        print("You have been stranded in the 1980s, in the middle of the Watergate scandal.")
    elif timePeriod=="1940s":
        print("You are stuck in the 1940s, in the center of a burgeoning Hollywood.")
    elif timePeriod=="colonial":
        print("You find yourself in colonial America in the heat of debate between the local Native American tribe and newcome settlers of the area.")
    print("Equip a weapon to have it at the ready! Food heals you! Now... go!")
    print(player.currentRoom.fullDescription())

def play():
    intro()
    finished = False
    while finished == False:
        for i in range(len(player.currentRoom.npcs)):
            outcome=battle(player.currentRoom.npcs[i])
            if outcome == 0:
                tempRoom=player.currentRoom
                player.currentRoom=player.previousRoom
                player.previousRoom=tempRoom
                player.currentRoom.fullDescription()
            elif outcome==1:
                player.currentRoom.fullDescription()
        command = parser.getCommand()
        finished = processCommand(command)
    if finished == True:
        if player.currentRoom() == "southWestRoom":
            print("You have found the time machine. Good job bro you can go back home. Just be careful and don't hit the red button. Oh no you hit the red button, I guess were going to talk to dinosaurs. Come on man you did the one thing I told you not to do. Oh well.")
        print("bye bye")
    else:
        print("Big problem, blame elliot")

def interact(command):
    if command.wordList[0]==None:
            return "Talk to whom?"
    else:
        for npc in player.currentRoom.npcs:
            npcToTalk = npc
            newWordList = []
            for items in command.wordList:
                newWordList.append(items.lower())
            if npcToTalk.name.lower().split() == newWordList:
                line = ""
                if npc.repeat==False:
                    line+=npc.line
                else:
                    line+=npc.repeatLine
                npc.repeat = True
                return npc.name+" says to you,\n\""+line+"\""
        return "There is no "+" ".join(command.wordList).title()+" here."

def processCommand(command):
    wantToQuit=False
    if command.isUnknown():
        print("That command is unknown.")
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
    elif commandWord in CommandWords.allSynonyms["drop"]:
        print(player.drop(command))
    elif commandWord in CommandWords.allSynonyms["talk"]:
        print(interact(command))
    elif commandWord in CommandWords.allSynonyms["use"]:
        print(player.use(command))
    elif commandWord in CommandWords.allSynonyms["inspect"]:
        print(player.inspect(command))
    elif commandWord in CommandWords.allSynonyms["equip"]:
        print(player.equip(command))
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