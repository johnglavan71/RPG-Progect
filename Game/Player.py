class player:
    def __init__(self, CLASS, HP=5, DEF=0, STR=20, DEX=1, GOLD=5):
        self.CLASS = CLASS
        self.HP = HP
        self.DEF = DEF
        self.STR = STR
        self.ATK = self.STR // 4
        self.DEX = DEX
        self.GOLD = GOLD
        self.ELEM_RESIS = {}
        self.INV = []
        self.CARRY = 0
        self.EQUIP = {
            "Main Hand": None,
            "Offhand": None,
            "Helmet": None,
            "Chestplate": None,
            "Pauldrons": None,
            "Bracers": None,
            "Gloves": None,
            "Leggings": None,
            "Boots": None,
            "Circlet": None,
            "Right Ring": None,
            "Left Ring": None,
            "Bracelet": None,
            "Necklace": None
        }
    def add_item(self, item):
        if item[list(item.keys())[0]]['Weight'] + self.CARRY > self.STR:
            print('You are too overburdened.')
            return False
        if 'Unstackable' in item:
            self.INV.append(item)
            print(f'Added {list(item.keys())[0]} to Inventory.')
            return True
        else:
            for i in self.INV:
                if list(i.keys())[0] == list(item.keys())[0]:
                    i[list(i.keys())[0]]['Quantity'] += item[list(item.keys())[0]]['Quantity']
                    print(f"Added {list(item.keys())[0]} \u00d7 {item[list(item.keys())[0]]['Quantity']} to Inventory.")
                    return True
    def equip_item(self, itemindex):
        item = self.INV[itemindex]
        slot = item[list(item.keys())[0]]['Slot']
        if self.EQUIP[slot[0]] == None:
            self.EQUIP[slot[0]] = item
            print(f'You have equipped {list(item.keys())[0]} to {slot[0]} ')
            self.INV.pop(itemindex)
            return
        elif len(slot) > 1:
            if self.EQUIP[slot[1]] == None:
                self.EQUIP[slot[1]] = item
                print(f'You have equipped {list(item.keys())[0]} to {slot[1]}')
                self.INV.pop(itemindex)
                return

        # All slots for this item are filled.
        # Show the slots, the items in those slots, and the stats of those items.
        print("Choose a slot to replace:")
        for s in slot:
            s_itemName = list(self.EQUIP[s].keys())[0]
            print(f"{s}: {s_itemName}")
            for t, v in self.EQUIP[s][s_itemName].items():
                print(f"    {t}: {v}")
        itemName = list(item.keys())[0]
        print(f"(Inventory): {itemName}")
        for t, v in item[itemName].items():
            print(f"    {t}: {v}")
        rpSlot = input("> ")
        self.INV.append(self.EQUIP[rpSlot])
        self.EQUIP[rpSlot] = item
        print(f'You have equipped {list(item.keys())[0]} to {rpSlot}')
        self.INV.pop(itemindex)
        return





# p = player(None)
#
# p.INV = [{"test1": {"Slot": ["Main Hand", "Offhand"], "Atk": 5, "Coolness": 69}},
# {"test2": {"Slot": ["Main Hand"], "Def": 3, "Astrophysics": 420}},
# {"test3": {"Slot": ["Main Hand", "Offhand"], "Def": 4, "Atk": 19, "bullshitVariable": 1337}}]
#
# p.equip_item(0)
# p.equip_item(0)
# p.equip_item(1)
# p.equip_item(0)
