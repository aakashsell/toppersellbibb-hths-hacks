from nltk.corpus import wordnet
from bs4 import BeautifulSoup as bs
import urllib.request
import random
'''
To Do: 
 - taking player text and reacting
 - generating personality
'''



class NPC:
    def __init__(self, timePeriod,line,repeatLine,hp,weapon,enemy,hasKey):
        self.timePeriod = timePeriod
        self.setNames()
        self.name=random.choice(self.namesChoice)
        self.line=line
        self.repeat=False
        self.repeatLine=repeatLine
        self.hp=hp
        self.weapon=weapon
        self.enemy=enemy
        self.hasKey=hasKey
    
    def clean(self, test_str):
        ret = ''
        skip1c = 0
        skip2c = 0
        for i in test_str:
            if i == '(':
                skip2c += 1
            elif i == ')'and skip2c > 0:
                skip2c -= 1
            elif skip1c == 0 and skip2c == 0:
                ret += i
        return ret

    def setNames(self):
        if self.timePeriod=="1940s":
            response=urllib.request.urlopen("https://en.wikipedia.org/wiki/1940s#Actors_/_Entertainers")
            html=response.read()
            soup=bs(html,"html5lib")
            self.names=soup.find_all("a",title=True)
            self.namesChoice=[]
            for name in self.names:
                if name.parent.name=="li" and name.parent.parent.name=="ul" and name.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.parent.parent.name=="div":
                    self.namesChoice.append(name.getText())
        elif self.timePeriod=="1980s":
            response=urllib.request.urlopen("https://en.wikipedia.org/wiki/1980s")
            html=response.read()
            soup=bs(html,"html5lib")
            self.names=soup.find_all("a",title=True)
            self.namesChoice=[]
            for name in self.names:
                if name.parent.name=="p" and name.parent.parent.name=="div" and name.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.name=="li" and name.parent.parent.parent.parent.parent.name=="ul":
                    self.namesChoice.append(name.getText())
            self.namesChoice = self.namesChoice[:-32]
        elif self.timePeriod=="colonial":
            response=urllib.request.urlopen("https://en.wikipedia.org/wiki/Category:People_of_colonial_New_Jersey")
            html=response.read()
            soup=bs(html,"html5lib")
            self.names=soup.find_all("a",title=True)
            self.namesChoice=[]
            for name in self.names:
                if name.parent.name=="li" and name.parent.parent.name=="ul" and name.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.parent.parent.parent.parent.name=="div" and name.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.name=="div":
                    # x=0
                    # run = True
                    # while run:
                    #     print(name.getText())
                    #     for char in name.getText():
                    #         if char=="(":
                    #             run=False
                    #             name=name.getText()[0:x]
                    #         x+=1ewqcfedfdsacease
                    #     run=False
                    newName = self.clean(name.getText())
                    self.namesChoice.append(newName)
                    
    def randomName(self):
        tempList = []
        for item in self.namesChoice:
            tempList.append(item)
        return tempList

    # def urlFormat(self):
    #     name=self.name.replace(" ","+")
    #     self.personalityURL = "https://www.google.com/search?q=" + name + "+personality"
    #     print(self.personalityURL)

    # def personality(self):
    #     self.urlFormat()
    #     response=urllib.request.urlopen(self.personalityURL)
    #     html=response.read()
    #     soup=bs(html,"html5lib")
    #     self.personality=soup.find_all('span',class_="e24Kjd")
    #     print(self.personality)

    def takeDamage(self, damage):
        self.hp-=damage