from lib.chunkHandler import chunkHandler

class charEngine():
    def __init__(self):
        self.inventory = {}
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False #mine horiz
        self.ctrl = False #place
        self.d = False #mine vert
        self.selected = 1 #inventory
    
    def removeObject(self, chunk, x, y, obj):
        chunkHandler.region[chunk][y][x].remove(obj)

    def moveCharacterInChunk(self,dx,dy):
        removeObject("cen", chunkHandler.char_location[0], chunkHandler.char_location[1], chunkHandler.character)
        chunkHandler.char_location[0] += dx
        chunkHandler.char_location[1] += dy
        chunkHandler.region["cen"][chunkHandler.char_location[1]][chunkHandler.char_location[0]] += character

    def moveCharacterBetweenChunks(self,dx,dy):
        destinationChunk = ""
        destinationX, destinationY = chunkHandler.char_location[0], chunkHandler.char_location[1]
        if chunkHandler.char_location[1] == 0 and dy == -1:
            destinationChunk += "n"
            destinationY = chunkHandler.chunksize-1
        elif chunkHandler.char_location[1] == chunkHandler.chunksize-1 and dy == 1:
            destinationChunk += "s"
            destinationY = 0
        if chunkHandler.char_location[0] == 0 and dx == -1:
            destinationChunk += "w"
            destinationX = chunkHandler.chunksize-1
        elif chunkHandler.char_location[0] == chunkHandler.chunksize-1 and dx == 1:
            destinationChunk += "e"
            destinationX = 0
        if destinationChunk == "":
            return
        if chunkHandler.region[destinationChunk][destinationY][destinationX][-1] not in chunkHandler.wall.values():
            self.removeObject("cen", chunkHandler.char_location[0], chunkHandler.char_location[1], chunkHandler.character)
            chunkHandler.char_location = [destinationX, destinationY]
            chunkHandler.saveregion()
            if "e" in destinationChunk or "w" in destinationChunk:
                chunkHandler.chunk[0] += dx
            if "n" in destinationChunk or "s" in destinationChunk:
                chunkHandler.chunk[1] += dy
            chunkHandler.chunk_label = f"{chunkHandler.chunk[0]}, {chunkHandler.chunk[1]}, {chunkHandler.chunk[2]}"
            chunkHandler.loadregion()
            chunkHandler.region["cen"][chunkHandler.char_location[1]][chunkHandler.char_location[0]] += chunkHandler.character
        else:
            if space:
                self.breakTile(destinationChunk, destinationX, destinationY)
            
    def testcollision(self):
        dy = self.down - self.up
        dx = self.right - self.left
        if 0 <= chunkHandler.char_location[1]+dy <= chunkHandler.chunksize-1 and 0 <= chunkHandler.char_location[0]+dx <= chunkHandler.chunksize-1:
            #if player is trying to move to a new tile in this chunk
            if chunkHandler.region["cen"][chunkHandler.char_location[1]+dy][chunkHandler.char_location[0]+dx][-1] not in chunkHandler.wall.values():
                self.moveCharacterInChunk(dx,dy)
            else:
                if space:
                    self.breakTile("cen", chunkHandler.char_location[0]+dx, chunkHandler.char_location[1]+dy)
        else:
            #if player is trying to move to a tile in a new chunk
            self.moveCharacterBetweenChunks(dx,dy)
        if chunkHandler.region["cen"][chunkHandler.char_location[1]][chunkHandler.char_location[0]][-2] in chunkHandler.item.values():
            #pickup item on ground
            self.pickupItem("cen", chunkHandler.char_location[0], chunkHandler.char_location[1])

    def breakTile(self, targetChunk, x, y):
        for key in breakpath:
            if key in chunkHandler.region[targetChunk][y][x]:
                self.removeObject(targetChunk, x, y, key)
                chunkHandler.region[targetChunk][y][x].append(breakpath[key])
                return

    def pickupItem(self, targetChunk, x, y):
        for key in chunkHandler.item:
            if chunkHandler.item[key] in chunkHandler.region[targetChunk][y][x]:
                self.inventory[key] += 1
                self.removeObject(targetChunk, x, y, chunkHandler.item[key])
                self.updateMenu()

    def buildTile(self, targetChunk, x, y):
        cursor = 1
        if len(chunkHandler.item) == 0:
            return
        for key in self.inventory:
            if cursor != self.selected:
                cursor += 1
                continue
            elif self.inventory[key] > 0 and chunkHandler.region["cen"][chunkHandler.char_location[1]][chunkHandler.char_location[0]][-2] not in \
                 chunkHandler.wall.values() and chunkHandler.region["cen"][chunkHandler.char_location[1]][chunkHandler.char_location[0]][-1] not in chunkHandler.wall.values():
                self.inventory[key] -= 1
                region[targetChunk][y][x].append(buildpath[item[key]])
                self.updateMenu()

    def updateMenu(self):
        global menu,selected
        cursor = 1
        menu = ["WASD - Move", "Spacebar - Break", "Control - Place", "12 - Inventory Select", "E - Dig/Use Stairs", "", "Inventory:"]
        for key in self.inventory:
            if cursor != selected:
                menu.append("   " + f"{self.inventory[key]}".rjust(5) + f"×{key}")
            else:
                menu.append(">> " + f"{self.inventory[key]}".rjust(5) + f"×{key}")
            cursor += 1
            if cursor > len(item):
                break

    def digDown(self):
        global region, char_location, chunk, chunk_label
        if region["cen"][char_location[1]][char_location[0]][0] == tile["Down Stair"]:
            removeObject("cen", char_location[0], char_location[1], character)
            saveregion()
            chunk[2] -= 1
            chunk_label = f"{chunk[0]}, {chunk[1]}, {chunk[2]}"
            loadregion()
            region["cen"][char_location[1]][char_location[0]].append(character)
        elif region["cen"][char_location[1]][char_location[0]][1] == tile["Up Stair"]:
            removeObject("cen", char_location[0], char_location[1], character)
            saveregion()
            chunk[2] += 1
            chunk_label = f"{chunk[0]}, {chunk[1]}, {chunk[2]}"
            loadregion()
            region["cen"][char_location[1]][char_location[0]].append(character)
        elif region["cen"][char_location[1]][char_location[0]][-2] not in wall.values():
            region["cen"][char_location[1]][char_location[0]][0] = tile["Down Stair"]
            removeObject("cen", char_location[0], char_location[1], character)
            saveregion()
            chunk[2] -= 1
            chunk_label = f"{chunk[0]}, {chunk[1]}, {chunk[2]}"
            loadregion()
            if region["cen"][char_location[1]][char_location[0]][-1] not in wall.values():
                region["cen"][char_location[1]][char_location[0]].append(tile["Up Stair"])
            else:
                region["cen"][char_location[1]][char_location[0]][1] = tile["Up Stair"]
            region["cen"][char_location[1]][char_location[0]].append(character)
