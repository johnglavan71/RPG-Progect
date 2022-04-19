import time
#import curses
from os import system
from maplib.col import col
from random import randrange, choice

#stdscr = curses.initscr()

class WorldMap:
    def __init__(self, player):
        self.p = player
        
        self.world = {}
        self.region = {}
        self.chunksize = 10

        self.chunk_label = f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"
        self.menu = ["WASD - Move", "Spacebar - Break", "E - Dig/Use Stairs"]
        
        self.collision = False
        self.space = False #DEBUG: Flag for the spacebar.
        
        self.character = "\u263B" #character for your character lmao

        #static tiles
        self.empty = {"Dirt": f"{col.CF4}.{col.RES}",
                 "Grass": f"{col.CFA},{col.RES}",
                 "Sand": f"{col.CFE}\u2591{col.RES}",
                 "Yellow Flower": f"{col.CFE}*{col.RES}",
                 "Red Flower": f"{col.CFC}*{col.RES}",
                 "Dust": ".",
                 "Rubble": ",",
                 "Road": "\u259A"}
        self.item = {"Wood": f"{col.CF6}/{col.RES}",
                "Stone": "*",
                "Iron": f"{col.CF8}\u2261{col.RES}",
                "Diamond": f"{col.CFB}♦{col.RES}"}
        self.wall = {"Oak Tree": f"{col.CF2}♣{col.RES}",
                "Pine Tree": f"{col.CF2}♠{col.RES}",
                "Cut Tree": f"{col.CF6}o{col.RES}",
                "Stump": f"{col.CF6}n{col.RES}",
                "Wood Wall": f"{col.CF6}\u2588{col.RES}",
        \
                "Stone": "\u2588",
                "Scratched Stone": "\u2593",
                "Cracked Stone": "\u2592",
                "Crumbling Stone": "\u2591",
        \
                "Hematite": f"{col.CBF}{col.CF8}%{col.RES}",
                "Scratched Hematite": f"{col.CB7}{col.CF0}\u2593{col.RES}",
                "Cracked Hematite": f"{col.CB7}{col.CF0}\u2592{col.RES}",
                "Crumbling Hematite": f"{col.CB7}{col.CF0}\u2591{col.RES}",
        \
                "Kimberlite": f"{col.CBF}{col.CFB}*{col.RES}",
                "Scratched Kimberlite": f"{col.CBB}{col.CF0}\u2593{col.RES}",
                "Cracked Kimberlite": f"{col.CBB}{col.CF0}\u2592{col.RES}",
                "Crumbling Kimberlite": f"{col.CBB}{col.CF0}\u2591{col.RES}",
        \
                "Stone Wall": f"{col.CFF}\u2588{col.RES}",
                "Iron Wall": f"{col.CF8}\u2588{col.RES}",
                "Diamond Wall": f"{col.CFB}\u2588{col.RES}"}
        self.tile = {"Down Stair": "v",
                "Up Stair": "^",
                "Trigger": " ",
                "Water": f"{col.CF1}\u2248{col.RES}"}

        #when a static tile is damaged, this tells what it will turn into
        self.breakpath = {self.wall["Oak Tree"]: self.wall["Cut Tree"],
                     self.wall["Pine Tree"]: self.wall["Cut Tree"],
                     self.wall["Cut Tree"]: self.wall["Stump"],
                     self.wall["Stump"]: self.item["Wood"],
                     self.wall["Stone"]: self.wall["Scratched Stone"],
                     self.wall["Scratched Stone"]: self.wall["Cracked Stone"],
                     self.wall["Cracked Stone"]: self.wall["Crumbling Stone"],
                     self.wall["Crumbling Stone"]: self.item["Stone"],
                     self.wall["Hematite"]: self.wall["Scratched Hematite"],
                     self.wall["Scratched Hematite"]: self.wall["Cracked Hematite"],
                     self.wall["Cracked Hematite"]: self.wall["Crumbling Hematite"],
                     self.wall["Crumbling Hematite"]: self.item["Iron"],
                     self.wall["Kimberlite"]: self.wall["Scratched Kimberlite"],
                     self.wall["Scratched Kimberlite"]: self.wall["Cracked Kimberlite"],
                     self.wall["Cracked Kimberlite"]: self.wall["Crumbling Kimberlite"],
                     self.wall["Crumbling Kimberlite"]: self.item["Diamond"],}

        self.chunkmap = ["^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
                         "^≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈#    ╔════════════   ^",
                         "^≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈####    ║  ^^^^^^^^^^^^^^",
                         "^≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈P#^^^^^  ╚═══════════╗   ^",
                         "^≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈##^###RR^^^M              ║   ^",
                         "^≈≈≈≈≈############## ^^^^RR^^^^^^^^^^^^^^^^^^W^^^^",
                         "^######      ♠║♠♠♠♠♠♠^^^^^║^^                ║   ^",
                         "^       ╔═════╩═F══╗♠^    ║      ♠♠♠         ║   ^",
                         "^ Y╗    ║   ♠♠♠♠♠♠♠║♠^    ╚══╦════╦══════════╝   ^",
                         "^  ╠════╣    ♠♠♠♠♠♠║♠^  ╔════╝  ♠♠║♠♠            ^",
                         "^  ║    ║      ╔═══╩════╝       ♠♠║♠♠            ^",
                         "^ *║*   V      ║      ^^^^^^^^  ♠♠║♠♠            ^",
                         "^**║**  ║      ║    ^^╔═══════════F══════D       ^",
                         "^**G*** ╚══════Z══════╝^^^^^^^ ♠♠♠♠♠♠♠           ^",
                         "^*******             ^^       ♠♠♠♠♠♠♠♠♠          ^",
                         "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"]

        ##              MAP KEY
        ##              ^ Mountain
        ##              * Flowers
        ##              ♠ Trees
        ##              # Beach
        ##              ≈ Sea
        ##
        ##              V Village
        ##              Y Yggdrasil
        ##              G Garden
        ##              F Forest
        ##              P Port
        ##              Z Maze
        ##              R Castle
        ##              D Graveyard
        ##              W Watch Tower
        ##              M Mines

    def loadregion(self): #Loads the nine chunks around the player
        self.region["cen"] = self.loadchunk(self.p.CHUNK[0], self.p.CHUNK[1], self.p.CHUNK[2])
        self.region["nw"] = self.loadchunk(self.p.CHUNK[0]-1, self.p.CHUNK[1]-1, self.p.CHUNK[2])
        self.region["n"] = self.loadchunk(self.p.CHUNK[0], self.p.CHUNK[1]-1, self.p.CHUNK[2])
        self.region["ne"] = self.loadchunk(self.p.CHUNK[0]+1, self.p.CHUNK[1]-1, self.p.CHUNK[2])
        self.region["w"] = self.loadchunk(self.p.CHUNK[0]-1, self.p.CHUNK[1], self.p.CHUNK[2])
        self.region["e"] = self.loadchunk(self.p.CHUNK[0]+1, self.p.CHUNK[1], self.p.CHUNK[2])
        self.region["sw"] = self.loadchunk(self.p.CHUNK[0]-1, self.p.CHUNK[1]+1, self.p.CHUNK[2])
        self.region["s"] = self.loadchunk(self.p.CHUNK[0], self.p.CHUNK[1]+1, self.p.CHUNK[2])
        self.region["se"] = self.loadchunk(self.p.CHUNK[0]+1, self.p.CHUNK[1]+1, self.p.CHUNK[2])

    def saveregion(self): #Unloads the nine chunks around the player
        self.world[f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"] = self.region["cen"]
        self.world[f"{self.p.CHUNK[0]-1}, {self.p.CHUNK[1]-1}, {self.p.CHUNK[2]}"] = self.region["nw"]
        self.world[f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]-1}, {self.p.CHUNK[2]}"] = self.region["n"]
        self.world[f"{self.p.CHUNK[0]+1}, {self.p.CHUNK[1]-1}, {self.p.CHUNK[2]}"] = self.region["ne"]
        self.world[f"{self.p.CHUNK[0]-1}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"] = self.region["w"]
        self.world[f"{self.p.CHUNK[0]+1}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"] = self.region["e"]
        self.world[f"{self.p.CHUNK[0]-1}, {self.p.CHUNK[1]+1}, {self.p.CHUNK[2]}"] = self.region["sw"]
        self.world[f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]+1}, {self.p.CHUNK[2]}"] = self.region["s"]
        self.world[f"{self.p.CHUNK[0]+1}, {self.p.CHUNK[1]+1}, {self.p.CHUNK[2]}"] = self.region["se"]

    def loadchunk(self, px, py, pz): #Loads an individual chunk. Will read chunkmap if the chunk doesn't exist.
        if f"{px}, {py}, {pz}" not in self.world:
            char = self.chunkmap[py][px]
            this_chunk = {}
            if pz == 0:
                for y in range(self.chunksize):
                    this_chunk[y] = []
                    for x in range(self.chunksize):
                        if char == "≈": this_chunk[y].append([self.tile["Water"]]) #sea
                        elif char == "#": this_chunk[y].append([self.empty["Sand"]]) #beach
                        elif char == "^": this_chunk[y].append([self.wall["Stone"]]) #mountains
                        elif char == "♠": #forest
                            wallchance = randrange(5)
                            this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                            if wallchance == 1: this_chunk[y][x].append(choice([self.wall["Oak Tree"], self.wall["Pine Tree"]]))
                        elif char == "*": this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Red Flower"]], [self.empty["Yellow Flower"]]])) #flowers
                        elif char == " ": this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]])) #plains
                        elif char in "═║╔╗╚╝╩╦╠╣": # roads
                            if y in range(self.chunksize//2-2, self.chunksize//2+2) and x in range(self.chunksize//2-2, self.chunksize//2+2):
                                this_chunk[y].append([self.empty["Road"]])
                            elif y in range(0, self.chunksize//2-2) and x in range(self.chunksize//2-2, self.chunksize//2+2):
                                if char in "║╚╝╩╠╣": this_chunk[y].append([self.empty["Road"]]) #north
                                else: this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                            elif y in range(self.chunksize//2-2, self.chunksize//2+2) and x in range(0, self.chunksize//2-2):
                                if char in "═╗╝╩╦╣": this_chunk[y].append([self.empty["Road"]]) #east
                                else: this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                            elif y in range(self.chunksize//2-2, self.chunksize//2+2) and x in range(self.chunksize//2+2, self.chunksize):
                                if char in "═╔╚╩╦╠": this_chunk[y].append([self.empty["Road"]]) #west
                                else: this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                            elif y in range(self.chunksize//2+2, self.chunksize) and x in range(self.chunksize//2-2, self.chunksize//2+2):
                                if char in "║╔╗╦╠╣": this_chunk[y].append([self.empty["Road"]]) #south
                                else: this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                            else: this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                        elif char == "M": #mine
                            if y in range(0, self.chunksize//2-2) or y in range(self.chunksize//2+2, self.chunksize): this_chunk[y].append([self.wall["Stone"]])
                            else:
                                if x in range(0, self.chunksize//2): this_chunk[y].append([self.wall["Stone"]])
                                elif y in range(self.chunksize//2-1, self.chunksize//2+1) and x in range(self.chunksize//2+2, self.chunksize//2+4): this_chunk[y].append([self.tile["Down Stair"]])
                                else: this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                        elif char == "V": #village
                            if y in [0, self.chunksize-1]:
                                if x not in range(self.chunksize//2-1, self.chunksize//2+1): this_chunk[y].append([self.wall["Wood Wall"]])
                                else: this_chunk[y].append([self.empty["Road"]])
                            else:
                                if x in [0, self.chunksize-1]: this_chunk[y].append([self.wall["Wood Wall"]])
                                elif y in [2, 3, self.chunksize-4, self.chunksize-3]:
                                    if x in [2, 3, self.chunksize-4, self.chunksize-3]: this_chunk[y].append([self.wall["Wood Wall"]])
                                    else: this_chunk[y].append([self.empty["Road"]])
                                else: this_chunk[y].append([self.empty["Road"]])
                            this_chunk[y][x].append(self.tile["Trigger"])
                        else: this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                                    
            elif pz < 0:
                cavechance = randrange(5)
                for y in range(self.chunksize):
                    this_chunk[y] = []
                    for x in range(self.chunksize):
                        ironchance = randrange(max(200-pz, 20))
                        diamondchance = randrange(max(1000-5*pz, 100))
                        if cavechance != 1:
                            this_chunk[y].append([choice([self.empty["Dust"], self.empty["Rubble"]]), self.wall["Stone"]])
                        else:
                            this_chunk[y].append(choice([[self.empty["Dust"]], [self.empty["Rubble"]]]))
                        if this_chunk[y][x][-1] in self.wall.values():
                            if diamondchance == 1:
                                this_chunk[y][x][1] = self.wall["Kimberlite"]
                            if ironchance == 1:
                                this_chunk[y][x][1] = self.wall["Hematite"]
                        
        else:
            this_chunk = self.world[f"{px}, {py}, {pz}"]
        return this_chunk

    def removeObject(self, targetChunk, x, y, obj): # Removes an object from a tile stack
        self.region[targetChunk][y][x].remove(obj)

    def moveCharacterInChunk(self,dx,dy): # Moves character from one tile stack to another
        self.removeObject("cen", self.p.COORDS[0], self.p.COORDS[1], self.character)
        self.p.COORDS[0] += dx
        self.p.COORDS[1] += dy
        self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]] += self.character

    def moveCharacterBetweenChunks(self,dx,dy): # Moves character from one chunk to another
        destinationChunk = ""
        destinationX, destinationY = self.p.COORDS[0], self.p.COORDS[1]
        if self.p.COORDS[1] == 0 and dy == -1:
            destinationChunk += "n"
            destinationY = self.chunksize-1
        elif self.p.COORDS[1] == self.chunksize-1 and dy == 1:
            destinationChunk += "s"
            destinationY = 0
        if self.p.COORDS[0] == 0 and dx == -1:
            destinationChunk += "w"
            destinationX = self.chunksize-1
        elif self.p.COORDS[0] == self.chunksize-1 and dx == 1:
            destinationChunk += "e"
            destinationX = 0
        if destinationChunk == "":
            return
        self.collision = False
        if self.region[destinationChunk][destinationY][destinationX][-1] in self.wall.values(): self.collision = True
        if self.tile["Water"] in self.region[destinationChunk][destinationY][destinationX] and not playerHasBoat: collision = True
        if not self.collision:
            self.removeObject("cen", self.p.COORDS[0], self.p.COORDS[1], self.character)
            self.p.COORDS = [destinationX, destinationY]
            self.saveregion()
            if "e" in destinationChunk or "w" in destinationChunk:
                self.p.CHUNK[0] += dx
            if "n" in destinationChunk or "s" in destinationChunk:
                self.p.CHUNK[1] += dy
            self.chunk_label = f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"
            self.loadregion()
            self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]] += self.character
        else:
            if self.space: self.breakTile(destinationChunk, destinationX, destinationY)
            
    def testcollision(self, controls:list): # Looks for anything preventing the player from moving
        playerHasBoat = False #DEBUG: Remove this variable once boats are added!
        up, down, left, right = controls[0], controls[1], controls[2], controls[3], 
        dy = down - up
        dx = right - left
        if 0 <= self.p.COORDS[1]+dy <= self.chunksize-1 and 0 <= self.p.COORDS[0]+dx <= self.chunksize-1:
            #if player is trying to move to a new tile in this chunk
            self.collision = False
            if self.region["cen"][self.p.COORDS[1]+dy][self.p.COORDS[0]+dx][-1] in self.wall.values(): self.collision = True
            elif self.tile["Water"] in self.region["cen"][self.p.COORDS[1]+dy][self.p.COORDS[0]+dx] and not playerHasBoat: self.collision = True
            if not self.collision: self.moveCharacterInChunk(dx,dy)
            else:
                if self.space: self.breakTile("cen", self.p.COORDS[0]+dx, self.p.COORDS[1]+dy)
        else:
            #if player is trying to move to a tile in a new chunk
            self.moveCharacterBetweenChunks(dx,dy)
        if self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][-2] in self.item.values():
            #pickup item on ground
            self.pickupItem("cen", self.p.COORDS[0], self.p.COORDS[1])
        if self.tile["Trigger"] in self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]]:
            pass #TODO: pass chunk coordinates of trigger to menu

    def breakTile(self, targetChunk, x, y): # Damages the tile the player is walking into
        for key in self.breakpath:
            if key in self.region[targetChunk][y][x]:
                self.removeObject(targetChunk, x, y, key)
                self.region[targetChunk][y][x].append(self.breakpath[key])
                return

    def pickupItem(self, targetChunk, x, y): # Picks up an item lying on the ground. May be deprecated.
        for key in self.item:
            if self.item[key] in self.region[targetChunk][y][x]:
                inventory[key] += 1
                self.removeObject(targetChunk, x, y, self.item[key])
                self.updateMenu()

    def updateMenu(self): # Updates the menu on the side.
        cursor = 1
        #TODO: Put the strips of the chunkmap on the menu.
        self.menu = ["WASD - Move", "Spacebar - Break", "Q - does nothing yet :/", "E - Dig/Use Stairs"]

    def resetCharacter(self): #Places the character.
        self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]] += self.character

    def use(self): # The Use Function(TM)
        if self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][0] == self.tile["Down Stair"]:
            #use down stairs
            self.removeObject("cen", self.p.COORDS[0], self.p.COORDS[1], self.character)
            self.saveregion()
            self.p.CHUNK[2] -= 1
            self.chunk_label = f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"
            self.loadregion()
            self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]].append(self.character)
            if self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][1] != self.tile["Up Stair"]:
                self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][1] = self.tile["Up Stair"]
        elif self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][1] == self.tile["Up Stair"]:
            #use up stairs
            self.removeObject("cen", self.p.COORDS[0], self.p.COORDS[1], self.character)
            self.saveregion()
            self.p.CHUNK[2] += 1
            self.chunk_label = f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"
            self.loadregion()
            self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]].append(self.character)
        elif self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][-2] not in self.wall.values() and self.p.CHUNK[2] < 0:
            #diggy diggy hole (only used in the mines)
            self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][0] = self.tile["Down Stair"]
            self.removeObject("cen", self.p.COORDS[0], self.p.COORDS[1], self.character)
            self.saveregion()
            self.p.CHUNK[2] -= 1
            self.chunk_label = f"{self.p.CHUNK[0]}, {self.p.CHUNK[1]}, {self.p.CHUNK[2]}"
            self.loadregion()
            if self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][-1] not in self.wall.values():
                self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]].append(self.tile["Up Stair"])
            else:
                self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]][1] = self.tile["Up Stair"]
            self.region["cen"][self.p.COORDS[1]][self.p.COORDS[0]].append(self.character)

    def getOutput(self):
    ##    try:
            #preparing grid for display
                
            output = f"{self.p.COORDS[0]}, {self.p.COORDS[1]} in chunk {self.chunk_label}\n"
            for y in range(self.chunksize):
                for x in self.region["nw"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                for x in self.region["n"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                for x in self.region["ne"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                try:
                    output += f"     {self.menu[y]}\n"
                except Exception:
                    output += "\n"
            for y in range(self.chunksize):
                for x in self.region["w"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                for x in self.region["cen"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                for x in self.region["e"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                try:
                    output += f"     {self.menu[y+self.chunksize]}\n"
                except Exception:
                    output += "\n"
            for y in range(self.chunksize):
                for x in self.region["sw"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                for x in self.region["s"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                for x in self.region["se"][y]:
                    if x[-1] != " ": output += x[-1]
                    else: output += x[-2]
                try:
                    output += f"     {self.menu[y+self.chunksize*2]}\n"
                except Exception:
                    output += "\n"
            return output
    ##    except Exception:
    ##        print(Exception)
    ##        input()
