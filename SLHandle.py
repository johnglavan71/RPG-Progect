from os import mkdir,remove
from os.path import isdir,exists
from json import dump
from json import load as jload

def pathfind(path: str):
    if not isdir(path):
        pathlist = path.split("\\")
        for i in range(len(pathlist)):
            if pathlist[i] == "": pathlist.pop(i)
        toVerify = ""
        for j in pathlist:
            toVerify += j + "\\"
            if not isdir(toVerify):
                mkdir(toVerify)
                print(f"Created directory \"{toVerify}\" successfully.")

def save(filedata:str, filename: str, *filepath: str):
    if len(filepath) > 0:
        path = filepath[0]
        pathfind(path)
    else: path = "."
    save_file = open(path+"\\"+filename,"w")
    save_file.write(filedata)
    save_file.close()
    print(f"File \"{path}\\{filename}\" saved successfully.")

def load(filename: str, *filepath: str):
    if len(filepath) > 0: path = filepath[0]
    else: path = "."
    if not isdir(path): print(f"The path \"{path}\" is invalid.")
    elif not exists(path+"\\"+filename): print(f"The file \"{path}\\{filename}\" does not exist.")
    else: return open(path+"\\"+filename,"r").read()

def saveJSON(filedata:str, filename: str, *filepath: str):
    if len(filepath) > 0:
        path = filepath[0]
        pathfind(path)
    else: path = "."
    with open(path+"\\"+filename,"w") as file:
        dump(filedata, file)
    print(f"File \"{path}\\{filename}\" saved successfully.")

def loadJSON(filename: str, *filepath: str):
    if len(filepath) > 0: path = filepath[0]
    else: path = "."
    if not isdir(path): print(f"The path \"{path}\" is invalid.")
    elif not exists(path+"\\"+filename): print(f"The file \"{path}\\{filename}\" does not exist.")
    else: 
        with open(path+"\\"+filename,"r") as file:
            return jload(file)

def delete(filename: str, *filepath: str):
    if len(filepath) > 0: path = filepath[0]
    else: path = "."
    if not isdir(path): print(f"The path \"{path}\" is invalid.")
    elif not exists(path+"\\"+filename): print(f"The file \"{path}\\{filename}\" does not exist.")
    else:
        remove(path+"\\"+filename)
        print(f"File \"{path}\\{filename}\" successfully deleted.")
