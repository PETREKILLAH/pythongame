import keyboard
import string
import time
from os import system
gameOn = True
shouldMapUpdate = True
currentRoom = 0

class Player:
    def __init__(self,x,y,maxHealth,moveDelay = 2):
        self.x = x
        self.y = y
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.moveDelay = moveDelay
        self.moveCounter = 0
class NPC:
    def __init__(self,x,y,maxHealth,moveDelay = 2,disposition = "HATE"):#I WANT TO IMPORT AND FIGURE OUT ENUMS REEEEEEEEEEEEEEE
        self.x = x
        self.y = y
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.moveDelay = moveDelay
        self.moveCounter = 0
        self.disposition = disposition
    
  #NOTE TO SELF WHEN EDITING AGAIN: I LAST LEFT OFF EDITING THE COLLISION. THINGS ARE COLLIDING, BUT ONLY APPROACHING FROM LEFT AND RIGHT
  #ITS BECAUSE I NEED TO CHECK ACROSS ROWS WHICH IS REALLY A PAIN IN THE DICK
player = Player(20,10,100,7)
npc0 = NPC(40,10,100)
room = {
    0:"""
--------------------------------------------------------------------
--------------------------------------------------------------------
------------------------------█-------------------------------------
------------------------------█-------------------------------------
------------------------------█-------------------------------------
------------------------------███████-------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
--------------------------------------------------------------------
    """,
    1:"""

"""
}

def getRoomLen(room):#REMINDER THAT THIS FUNCTION MUST BE RUN EVERYTIME WE CHANGE ROOMS
    
    room = room.lstrip("\n")
    return room.find("\n")

roomLen = getRoomLen(room[currentRoom])


def checkCollision(x,y):
    localRoom = room[currentRoom]
    localRoom = localRoom.replace("\n","")
    return localRoom[x+y*roomLen]#THIS FORMULA NEEDS TO BE FIXED FOR LEAVING THROUGH THE SOUTH AND TOWARDS THE ORIGIN


def moveObject(object,x,y):
    global shouldMapUpdate
    localRoom = room[currentRoom]
    if object.moveCounter > 0: #Are we allowed to move by according to cooldown?(No)
        object.moveCounter -= 1
    else:#Are we allowed to move according to cooldown?(Yup)

        if checkCollision(object.x + x, object.y + y) == "-":#Will we be hitting anything if we move there?(No)

            #start count down for move delay
            object.moveCounter = object.moveDelay

            #move to new coords
            object.x += x
            object.y += y
            shouldMapUpdate = True
        

def renderMap():
    localRoom = room[currentRoom]
    row = localRoom.split("\n")
    row.pop(0)

    #Draw Player
    temp = list(row[player.y])
    if player.x < len(temp) and player.x > -1:
        temp[player.x] = "@"
        row[player.y] = "".join(temp)

    #Draw Enemy (TO DO THIS, I NEED TO MAKE A SYTEM OF STORING ENEMIES IN ROOMS AND HAVING THEM DELETE WHEN THEY DIE)
    #I WILL MOST LIKELY HAVE MAKE ROOMS STORED IN AN ARRAY INSIDE OF THE DICTIONARY CONTAINING ALL OF THEIR POSITIONS,
    #HEALTH VALUES, ETC)
    localRoom = "\n".join(row)
    print(localRoom)

def catchPlayerInput():
    global gameOn
    if keyboard.is_pressed('w'):#up
        if keyboard.is_pressed('a'):
            moveObject(player,-1,-1)
        elif keyboard.is_pressed('d'):
            moveObject(player,1,-1)
        else:
            moveObject(player,0,-1)
    elif keyboard.is_pressed('s'):#down
        if keyboard.is_pressed('a'):
            moveObject(player,-1,1)
        elif keyboard.is_pressed('d'):
            moveObject(player,1,1)
        else:
            moveObject(player,0,1)
    elif keyboard.is_pressed('a'):#left
        moveObject(player,-1,0)
    elif keyboard.is_pressed('d'):#right
        moveObject(player,1,0)
    if keyboard.is_pressed('esc'):#escape
        gameOn = False


#checkCollsion(0,1)
#print(getRoomLen(room[0]))
#time.sleep(10)
while(gameOn):
    
    if shouldMapUpdate == True:
        system('cls') #This is how you clear the screen
        renderMap()
        shouldMapUpdate = False
        #print(player.x,player.y)
    catchPlayerInput()

    
    #Game Speed(The lower it is, the faster)
    time.sleep(0.005)