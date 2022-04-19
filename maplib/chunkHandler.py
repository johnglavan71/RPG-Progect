from ast import literal_eval
from random import randrange, choice
from lib.col import col

class chunkHandler:
    def __init__(self):
        self.world = {}
        self.region = {}
        self.chunksize = 12
        self.chunk = [0, 0, 0]
        self.chunk_label = f"{self.chunk[0]}, {self.chunk[1]}, {self.chunk[2]}"
        self.char_location = [self.chunksize//2, self.chunksize//2]

        file = open("data\\tiles.json","r")
        tiles = {
'character': "\u263B",
'empty': {
	"Dirt": f"{col.CF4}.{col.RES}",
	"Grass": f"{col.CFA},{col.RES}",
	"Dust": ".",
	"Rubble": ","
	},
'item': {
	"Wood": f"{col.CF6}/{col.RES}",
	"Stone": "*",
	"Iron": f"{col.CF8}\u2261{col.RES}",
	"Diamond": f"{col.CFB}♦{col.RES}"
	},
'wall': {
	"Tree": f"{col.CF6}O{col.RES}",
	"Cut Tree": f"{col.CF6}o{col.RES}",
	"Stump": f"{col.CF6}n{col.RES}",
	"Wood Wall": f"{col.CF6}\u2588{col.RES}",
	"Stone": "\u2588",
	"Scratched Stone": "\u2593",
	"Cracked Stone": "\u2592",
	"Crumbling Stone": "\u2591",
	"Hematite": f"{col.CBF}{col.CF8}%{col.RES}",
	"Scratched Hematite": f"{col.CB7}{col.CF0}\u2593{col.RES}",
	"Cracked Hematite": f"{col.CB7}{col.CF0}\u2592{col.RES}",
	"Crumbling Hematite": f"{col.CB7}{col.CF0}\u2591{col.RES}",
	"Kimberlite": f"{col.CBF}{col.CFB}*{col.RES}",
	"Scratched Kimberlite": f"{col.CBB}{col.CF0}\u2593{col.RES}",
	"Cracked Kimberlite": f"{col.CBB}{col.CF0}\u2592{col.RES}",
	"Crumbling Kimberlite": f"{col.CBB}{col.CF0}\u2591{col.RES}",
	"Water": f"{col.CF1}\u2248{col.RES}",
	"Stone Wall": f"{col.CFF}\u2588{col.RES}",
	"Iron Wall": f"{col.CF8}\u2588{col.RES}",
	"Diamond Wall": f"{col.CFB}\u2588{col.RES}"
	},
'tile': {
	"Down Stair": "v",
	"Up Stair": "^"
	}
}
        file.close()

        self.character = tiles['character']
        self.empty = tiles['empty']
        self.item = tiles['item']
        self.wall = tiles['wall']
        self.tile = tiles['tile']
        
    def loadregion(self):
        self.region["cen"] = self.loadchunk(self.chunk[0], self.chunk[1], self.chunk[2])
        self.region["nw"] = self.loadchunk(self.chunk[0]-1, self.chunk[1]-1, self.chunk[2])
        self.region["n"] = self.loadchunk(self.chunk[0], self.chunk[1]-1, self.chunk[2])
        self.region["ne"] = self.loadchunk(self.chunk[0]+1, self.chunk[1]-1, self.chunk[2])
        self.region["w"] = self.loadchunk(self.chunk[0]-1, self.chunk[1], self.chunk[2])
        self.region["e"] = self.loadchunk(self.chunk[0]+1, self.chunk[1], self.chunk[2])
        self.region["sw"] = self.loadchunk(self.chunk[0]-1, self.chunk[1]+1, self.chunk[2])
        self.region["s"] = self.loadchunk(self.chunk[0], self.chunk[1]+1, self.chunk[2])
        self.region["se"] = self.loadchunk(self.chunk[0]+1, self.chunk[1]+1, self.chunk[2])

    def saveregion(self):
        self.world[f"{chunk[0]}, {chunk[1]}, {chunk[2]}"] = self.region["cen"]
        self.world[f"{chunk[0]-1}, {chunk[1]-1}, {chunk[2]}"] = self.region["nw"]
        self.world[f"{chunk[0]}, {chunk[1]-1}, {chunk[2]}"] = self.region["n"]
        self.world[f"{chunk[0]+1}, {chunk[1]-1}, {chunk[2]}"] = self.region["ne"]
        self.world[f"{chunk[0]-1}, {chunk[1]}, {chunk[2]}"] = self.region["w"]
        self.world[f"{chunk[0]+1}, {chunk[1]}, {chunk[2]}"] = self.region["e"]
        self.world[f"{chunk[0]-1}, {chunk[1]+1}, {chunk[2]}"] = self.region["sw"]
        self.world[f"{chunk[0]}, {chunk[1]+1}, {chunk[2]}"] = self.region["s"]
        self.world[f"{chunk[0]+1}, {chunk[1]+1}, {chunk[2]}"] = self.region["se"]

    def loadchunk(self, px, py, pz):
        if f"{px}, {py}, {pz}" not in self.world:
            this_chunk = {}
            if pz == 0:
                pondchance = randrange(3)
                for y in range(self.chunksize):
                    this_chunk[y] = []
                    for x in range(self.chunksize):
                        if pondchance == 1 and [px,py] != [0,0]:
                            this_chunk[y].append([self.wall["Water"]])
                        else:
                            wallchance = randrange(10)
                            this_chunk[y].append(choice([[self.empty["Grass"]], [self.empty["Dirt"]]]))
                            if wallchance == 5:
                                this_chunk[y][x].append(self.wall["Tree"])
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
                        if this_chunk[y][x][-1] in wall.values():
                            if diamondchance == 1:
                                this_chunk[y][x][1] = self.wall["Kimberlite"]
                            if ironchance == 1:
                                this_chunk[y][x][1] = self.wall["Hematite"]
                        
        else:
            this_chunk = self.world[f"{px}, {py}, {pz}"]
        return this_chunk
