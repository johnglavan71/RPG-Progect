import msvcrt
from Player import Player
from worldMap import WorldMap
from os import system
from time import sleep

# [ kbhit, getch ]
Hit = msvcrt.kbhit
Get = msvcrt.getch

class Listener:
    def __init__(self):
        self.__key = None
    def run(self):
        hit = Hit()
        if hit: self.__key = Get()
        else: self.__key = None
        return self.__key

def GameLoop():
    # Initialize
    listener = Listener()
    
    # TODO: Load save
    #if False: #if not save found
    name = input("What is your name?\n: ")
    classchoice = input('Please choose your class.\n\
                        Mage : Uses magic to slay your foes in mysterious ways.\n\
                        Barbarian : All you know is how to fight.\n\
                        Knight : You MUST protect the others.\n\
                        Rogue : Stealth and steal is what your best at.\n: ')
    p = Player(name, classchoice)
    room = WorldMap(p)
    oldOutput = ""
    room.loadregion()
    room.updateMenu()
    room.resetCharacter()
    #else: pass #save found
    
    # Start Loop
    while True:
        key = listener.run()
        up, left, down, right, use, back, dig = False, False, False, False, False, False, False
        
        if key is not None:
            key = key.decode('utf-8')
            if key == 'w': up = True
            if key == 'a': left = True
            if key == 's': down = True
            if key == 'd': right = True
            if key == 'e': use = True
            if key == 'q': back = True #will open the menu or go back
            if key == ' ': dig = True

        if type(room) is WorldMap:
            if up or down or left or right:
                room.testcollision([up, down, left, right])
            if use:
                room.use()
            output = room.getOutput()
            if output != oldOutput:
                system("cls")
                print(output)
                oldOutput = output
            sleep(0.1)
            

GameLoop()
