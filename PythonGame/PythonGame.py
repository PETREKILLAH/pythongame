import keyboard
import string
import time
import math
from os import system
gameOn = True
shouldMapUpdate = True
currentRoom = 0
#↑ ↓ ↖ ↗ ↘ ↙
#system('modecon: cols= lines= ')
def distance(x1,y1,x2,y2):#Returns the distance between two points
    return math.sqrt( (x2-x1) ** 2 ) + ( (y2-y1) ** 2 )

class Config:
    DirectionEnabled = True
    DiagonalDirection = True
    DiagonalMovement = True
    WrapScreen = False
projectile = {} 
class Projectile:
    id = 0
    def __init__(self,x,y,maxHealth,moveDelay,direction,id,owner):
        self.x = x
        self.y = y
        self.maxHealth = maxHealth
        self.health = maxHealth
        self.moveDelay = moveDelay
        self.moveCounter = 0
        self.direction = direction
        self.id = id
        self.owner = owner
        
    def Act(self):
        if self.moveCounter > 0:
            self.moveCounter -= 1
        if self.x <= roomLen - 1 and self.y <= roomWid - 1 and self.x >= 0 and self.y >= 0:
            if self.direction == 0: #right
                moveObject(self,1,0)
            elif self.direction == 180:#left
                moveObject(self,-1,0)
            elif self.direction == 90: #up
                moveObject(self,0,-1)
            elif self.direction == 270: #down
                moveObject(self,0,1)
            elif self.direction == 135: #up left
                moveObject(self,-1,-1)
            elif self.direction == 45: #up right
                moveObject(self,1,-1)
            elif self.direction == 225: #down left
                moveObject(self,-1,1)
            elif self.direction == 315: #down right
                moveObject(self,1,1)
            else:
                pass# you should not have gotten here
        else:
            del projectile[self.id]
            del self


class Player:
    def __init__(self,x,y,maxHealth,moveDelay = 2,shootDelay = 4):
        self.x = x
        self.y = y
        self.maxHealth = maxHealth
        self.health = self.maxHealth
        self.moveDelay = moveDelay
        self.moveCounter = 0
        self.direction = 0
        self.shootDelay = shootDelay;
        self.shootCoolDown = 0;

    def CreateProjectile(self,x,y,maxHealth,moveDelay,direction):
        projectile[Projectile.id] =  Projectile(x,y,maxHealth,moveDelay,direction,Projectile.id,self)
        Projectile.id += 1        

    def Shoot(self):
        if self.shootCoolDown < 1:
            self.CreateProjectile(self.x,self.y,1,3,self.direction)
            self.shootCoolDown = self.shootDelay
    
    def Act(self):
        if self.moveCounter > 0:
            self.moveCounter -= 1
        if self.shootCoolDown > 0:
            self.shootCoolDown -= 1
    
            

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
    def Act(self):
        if self.moveCounter > 0:
            self.moveCounter -= 1
        if self.disposition == "HATE":
            if distance(player.x,player.y,self.x,self.y) < self.agro:
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

player = Player(20,10,100,5)
player.shootCoolDown = 0
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

    
    if object.moveCounter == 0:#Are we allowed to move according to cooldown?(Yup)

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
        temp[player.x] = "@"
        row[player.y] = "".join(temp)

    
    for mob in npc[currentRoom]:
        if mob.x <= roomLen - 1 and mob.y <= roomWid - 1 and mob.x >= 0 and mob.y >= 0:
            temp = list(row[mob.y])
            temp[mob.x] = "#"
            row[mob.y] = "".join(temp)
    
    for key,value in projectile.items():
        if value.x <= roomLen - 1 and value.y <= roomWid - 1 and value.x >= 0 and value.y >= 0:
            temp = list(row[value.y])
            temp[value.x] = "+"
            row[value.y] = "".join(temp)
        
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
            moveObject(player,0,-1)#up
            player.direction = 90

    elif keyboard.is_pressed('s'):#down
        if keyboard.is_pressed('a'):#down left
            moveObject(player,-1,1)
            player.direction = 225
        elif keyboard.is_pressed('d'):#down right
            moveObject(player,1,1)
            player.direction = 315
        else:
            moveObject(player,0,1)#down
            player.direction = 270

    elif keyboard.is_pressed('a'):#left
        moveObject(player,-1,0)
        player.direction = 180

    elif keyboard.is_pressed('d'):#right
        moveObject(player,1,0)
        player.direction = 0

    if keyboard.is_pressed('esc'):#escape
        gameOn = False

    if keyboard.is_pressed('spacebar'):
        player.Shoot()




while(gameOn):
    
    if shouldMapUpdate == True:
        system('cls') #This is how you clear the screen
        
        renderMap()
        shouldMapUpdate = False
        #print(player.x,player.y)

    catchPlayerInput()

    for mob in npc[currentRoom]:
        mob.Act()
    
    projectiles = list(projectile.items())
    for key,value in projectiles:
        value.Act()
    player.Act()
    
    #Game Speed(The lower it is, the faster)
    time.sleep(0.005)

    #THE WAY THAT MOVE DELAY WORKS NOW SUCKS. FOR THE MOVE COUNTER TO COUNT DOWN, YOU HAVE TO ACTIVELY BE HITTING THE BUTTON.
    #MAKE A MEMBER FUNCTION FOR ALL THINGS THAT MOVE THAT GETS CALLED EVERY TICK THAT TICKS DOWN THE TIMER BY ONE EACH TIME.
    #THEN,  IMPLEMENT THAT SAME SYSTEM FOR PROJECTILE SHOOTING COOL DOWN. I SUSPECT THE REASON WHY PROJECTILES ARE LAGGING IS
    #BECAUSE TOO MANY OF THEM ARE BEING MADE AT A TIME AND THEY ARE JUST OCCUPYING THE SAME SPACE TAKE UP RESOURCES.