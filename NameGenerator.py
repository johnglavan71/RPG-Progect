from random import choice,randrange

#1.0: Letters are added randomly from a string that contains every letter.
#2.0: Letters are now added randomly from a list of consonants and a list of vowels, formed blocks [consonant, vowel], to fix long strings of consonants or vowels making unpronounceable names. Additionally, multiple letters can count as a consonant or vowel, like "qu" or "ai".
#2.1: Certain letters are made redundant in the lists, to reduce the number of "high scrabble score" names. Names can now end with a vowel. Also, names will now be generated with a more consistent length of 2-5 blocks.
#3.0: Letter distribution changed to further reduce the number of "high scrabble score" names, improving the quality of names markedly. Additionally, names are now generated as a first name, consisting of 2-4 blocks, and last name, of 2-5 blocks.
#3.1: Names can now start with a vowel, the side effect being that names with as few as three letters [vowel, consonant, vowel] are now possible.


# This is the old distribution, saved in case I want to enable it with a setting later.
#consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "qu", "r",
#              "s", "t", "v", "w", "x", "y", "z", "ch", "th", "sh"]
#vowels = ["a", "a", "a", "e", "e", "e", "i", "i", "i", "o", "o", "o", "u", "u", "u",
#          "ee", "oo", "y", "ae", "ea", "ie", "ue", "ei", "ai"]

consonants = []
vowels = []

def addToBag(bag:list,string:str,count:int):
    for i in range(count):
        bag.append(string)
    return bag

consonants = addToBag(consonants, "r", 38)
consonants = addToBag(consonants, "t", 35)
consonants = addToBag(consonants, "n", 33)
consonants = addToBag(consonants, "s", 29)
consonants = addToBag(consonants, "l", 27)
consonants = addToBag(consonants, "c", 23)
consonants = addToBag(consonants, "d", 17)
consonants = addToBag(consonants, "p", 16)
consonants = addToBag(consonants, "m", 15)
consonants = addToBag(consonants, "h", 15)
consonants = addToBag(consonants, "g", 12)
consonants = addToBag(consonants, "b", 10)
consonants = addToBag(consonants, "f", 9)
consonants = addToBag(consonants, "y", 9)
consonants = addToBag(consonants, "w", 6)
consonants = addToBag(consonants, "k", 5)
consonants = addToBag(consonants, "v", 5)
consonants = addToBag(consonants, "x", 1)
consonants = addToBag(consonants, "z", 1)
consonants = addToBag(consonants, "j", 1)
consonants = addToBag(consonants, "qu", 1)

vowels = addToBag(vowels, "a", 43)
vowels = addToBag(vowels, "e", 56)
vowels = addToBag(vowels, "i", 38)
vowels = addToBag(vowels, "o", 36)
vowels = addToBag(vowels, "u", 18)
vowels = addToBag(vowels, "y", 9)
vowels = addToBag(vowels, "ee", 3)
vowels = addToBag(vowels, "oo", 3)
vowels = addToBag(vowels, "ae", 2)
vowels = addToBag(vowels, "ea", 2)
vowels = addToBag(vowels, "ie", 1)
vowels = addToBag(vowels, "ue", 1)
vowels = addToBag(vowels, "ei", 1)
vowels = addToBag(vowels, "ai", 1)

def nameGenerator(minBlocks,randAddedBlocks):
    boolean = choice([True, False])
    newName = ""
    if boolean: newName += choice(consonants) # start name with consonant
    newName += choice(vowels) # start name with vowel or finish first block
    minBlocks -= 1
    blocks = randrange(randAddedBlocks)+minBlocks
    for i in range(blocks):
        newName += choice(consonants) + choice(vowels)
    boolean = choice([True, False])
    if boolean: newName += choice(consonants)
    return newName
