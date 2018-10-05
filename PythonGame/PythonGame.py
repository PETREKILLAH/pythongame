import keyboard
import string
import time
import math
from os import system
gameOn = True
shouldMapUpdate = True
currentRoom = 0
#↑ ↓ ↖ ↗ ↘ ↙
def distance(x1,y1,x2,y2):#Returns the distance between two points
    return math.sqrt( (x2-x1) ** 2 ) + ( (y2-y1) ** 2 )
class Config:
    DirectionEnabled = True
    DiagonalDirection = True
    DiagonalMovement = True
    WrapScreen = False
    


class Player:
    def __init__(self,x,y,maxHealth,moveDelay = 2):
        self.x = x
        self.y = y
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.moveDelay = moveDelay
        self.moveCounter = 0
        self.direction = 0

class NPC:
    def __init__(self,x,y,maxHealth,moveDelay = 2,disposition = "HATE"):#I WANT TO IMPORT AND FIGURE OUT ENUMS REEEEEEEEEEEEEEE
        self.x = x
        self.y = y
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.moveDelay = moveDelay
        self.moveCounter = 0
        self.direction = 0
        self.disposition = disposition
        self.agro = 10
    def act(self):
        if self.disposition == "HATE":
            if distance(player.x,player.y,self.x,self.y) < 10:
                if self.x > player.x and self.y > player.y:
                    moveObject(self,-1,-1)
                elif self.x < player.x and self.y < player.y:
                    moveObject(self,1,1)
                elif self.x < player.x and self.y > player.y:
                    moveObject(self,1,-1)
                elif self.x > player.x and self.y < player.y:
                    moveObject(self,-1,1)
                elif self.x > player.x:
                    moveObject(self,-1,0)
                elif self.x < player.x:
                    moveObject(self,1,0)
                elif self.y > player.y:
                    moveObject(self,0,-1)
                elif self.y < player.y:
                    moveObject(self,0,1)
                else:
                    pass # The enemy is on the player

                
            



player = Player(20,10,100,7)
npc0 = NPC(40,9,100,14)
npc1 = NPC(20,9,100,14)
npc = {
    0:[npc0,npc1]
    }
room = {
    0:"""
--------------------------------------------------------------------
--------------------------------------------------------------------
------------------------------█-------------------------------------
------------------------------█-------------------------------------
------------------------------█-------------------------------------
------------------------------███████-------------------------------
------------------------------------█-------------------------------
------------------------------------█-------------------------------
------------------------------------█-------------------------------
------------------------------------█-------------------------------
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

def getRoomDimensions(room):#REMINDER THAT THIS FUNCTION MUST BE RUN EVERYTIME WE CHANGE ROOMS
    
    room = room.lstrip("\n")
    return [room.find("\n"),room.count("\n")]

roomLen = getRoomDimensions(room[currentRoom])[0]
roomWid = getRoomDimensions(room[currentRoom])[1]


def checkCollision(x,y):
    localRoom = room[currentRoom]
    localRoom = localRoom.replace("\n","")
    if x < 0 or y < 0:
        return "-"
    elif x > roomLen-1 or y > roomWid-1:
        return "-"
    else:
        return localRoom[x+y*roomLen]#THIS FORMULA NEEDS TO BE FIXED FOR LEAVING THROUGH THE SOUTH AND TOWARDS THE ORIGIN

def checkForNpc(x,y):
    for mob in npc[currentRoom]:
        if x == mob.x and y == mob.y:
            return False
        else:
            return True

def moveObject(object,x,y):
    global shouldMapUpdate
    localRoom = room[currentRoom]

    if object.moveCounter > 0: #Are we allowed to move by according to cooldown?(No)
        object.moveCounter -= 1

    else:#Are we allowed to move according to cooldown?(Yup)

        if checkCollision(object.x + x, object.y + y) == "-" and checkForNpc(object.x + x, object.y + y):#Will we be hitting anything if we move there?(No)
            
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
    if player.x <= roomLen - 1 and player.y <= roomWid - 1 and player.x >= 0 and player.y >= 0:
        temp = list(row[player.y])
        if player.x < len(temp) and player.x > -1:
            temp[player.x] = "@"
            row[player.y] = "".join(temp)

    for mob in npc[currentRoom]:
        temp = list(row[mob.y])
        temp[mob.x] = "#"
        row[mob.y] = "".join(temp)
        
    localRoom = "\n".join(row)
    print(localRoom)

def catchPlayerInput():
    global gameOn
    if keyboard.is_pressed('w'):#up
        if keyboard.is_pressed('a'):#up left
            moveObject(player,-1,-1)
            player.direction = 135
        elif keyboard.is_pressed('d'):
            moveObject(player,1,-1)#up right
            player.direction = 45
        else:
            moveObject(player,0,-1)
    elif keyboard.is_pressed('s'):#down
        if keyboard.is_pressed('a'):#down left
            moveObject(player,-1,1)
        elif keyboard.is_pressed('d'):#down left
            moveObject(player,1,1)
        else:
            moveObject(player,0,1)
    elif keyboard.is_pressed('a'):#left
        moveObject(player,-1,0)
    elif keyboard.is_pressed('d'):#right
        moveObject(player,1,0)
    if keyboard.is_pressed('esc'):#escape
        gameOn = False




while(gameOn):
    
    if shouldMapUpdate == True:
        system('cls') #This is how you clear the screen
        renderMap()
        shouldMapUpdate = False
        #print(player.x,player.y)

    catchPlayerInput()

    for mob in npc[currentRoom]:
        mob.act()
        
    
    #Game Speed(The lower it is, the faster)
    time.sleep(0.005)