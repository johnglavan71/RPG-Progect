
class Menu:
    def __init__(self, menuList:list):
        self.menuList = menuList
        self.cursor = 0

    def printmenu(self):
        mlist = self.menuList
        for i, val in enumerate(mlist):
            if self.cursor == i:
                print("[" + str(i+1).center(3) + "]",":", val)
            else:
                print(str(i+1).center(5),":", val)
    def move_cursor(self, input):
        if input == "up":
            self.cursor = max(self.cursor-1,0)
        elif input == "down":
            self.cursor = min(self.cursor+1,len(self.menuList)-1)
        elif input == 'select':
            return self.cursor

# from time import sleep
# forestmenu = ['tree', 'bark', 'stones', 'etc', 'test']
# forestItemsMenu = menu(['tree', 'bark', 'stones', 'etc', 'test'])
# forestItemsMenu.printmenu()
# forestItemsMenu.move_cursor('up')
# sleep(2)
# forestItemsMenu.move_cursor('down')
# sleep(2)
# forestItemsMenu.move_cursor('down')
# sleep(2)
# forestItemsMenu.move_cursor('down')
# sleep(2)
# forestItemsMenu.move_cursor('down')
# sleep(2)
# forestItemsMenu.move_cursor('down')
# sleep(2)
# forestItemsMenu.move_cursor('down')
# sleep(2)
# forestItemsMenu.move_cursor('up')
# sleep(2)
# forestItemsMenu.move_cursor('up')
# sleep(2)
# q = forestItemsMenu.move_cursor('select')
# print(forestmenu[q])
