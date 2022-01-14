import secrets
import random
import json
import string
import time
import os


dir = os.path.dirname(os.path.realpath(__file__))
langPath = dir + "/lang/"

print(os.path.exists(langPath))
print(os.path.exists(langPath + "index.json"))

if os.path.exists(langPath) == False:
    os.mkdir(langPath)

if os.path.exists(langPath + "index.json") == False:
    f = open(langPath + "index.json", "x")
    f.write('{"decode" : {}, "encode" : {}}')
    f.close()



curTable = "standard"
#Generates a secrets Letter or Number, except F,H and U, because these are used to seperate individual Letters
def generator():
    letters = ["A","a","B","b","C","c","D","d","E","e","f","G","g","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","ö","Ö","Ü","ü","ä","Ä","!","?",".","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
    return secrets.choice(letters)


def generateCharacter(ListLen, seed):
    random.seed(seed)
    letters = ["A","a","B","b","C","c","D","d","E","e","f","G","g","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","ö","Ö","Ü","ü","ä","Ä","!","?",".","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
    Lettercode = list("".join([random.choice(letters) for _ in range(0, random.randint(5,8))]) for _ in range(0, ListLen))
    return Lettercode


def getTables():
    FilesList = []
    for file in os.listdir(langPath):
        if file.endswith(".json"):
            if file != "index.json":
                filelist = []
                for i in list(file):
                    if i == ".":
                        break
                    filelist.append(i)
                FilesList.append("".join(filelist))
    return FilesList


def decode(String, NoPrint, file):
    with open(langPath + file + '.json', encoding="utf-8") as json_file:
        code = json.load(json_file)

    String= String.replace("F"," ")
    String= String.replace("H"," ")
    String= String.replace("U"," ")
    StringList = String.split()
    String=list(String)


    returnList = []
    codeList = list(code)
    k = 0
    for it in StringList:
        String=list(StringList[k])
        for item in code: #Iterates over all Keys and if the Value matches the Letter gets appended to the output list
            i = iter(String)
            if all(any(v == ch for v in i) for ch in code[item]):
                returnList.append(item)
        k = k + 1

    return "".join(returnList)


def encode(String, file):

    returnList = []
    secretsGenerator = secrets.SystemRandom()
    with open(langPath + file + '.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    String=list(String)

    while True:
        returnList = []
        for item in String:
            try:
                code = data[item]
            except:
                return ""


            codeList = list(code)
            charLenList = list(range(0, secretsGenerator.randint(len(code) + 3, 17))) #Length of Character
            charLen = len(charLenList)


            codeChar = 0
            for char in charLenList:

                if secretsGenerator.randint(0,2) == 0 or (charLen - char) <= codeChar:    #By secrets or if the end of the letter is near, insert a letter from the identifier code
                    if 0 <= codeChar < len(codeList):
                        returnList.append(codeList[codeChar])
                        codeChar = codeChar + 1
                    else:
                        returnList.append(generator())

                else:
                    returnList.append(generator())

            sequence = ["F", "H", "U"] #Letters between words
            returnList.append(secrets.choice(sequence))

        if decode("".join(returnList), "True", file).replace(" ","")== str("".join(String)).replace(" ",""): #Generates a new String until it matches the decoding result, to prevent accidental Letter overlapping

            return str("".join(returnList))

def delTable(inp):
    # Deletion from index.json
    with open(langPath + 'index.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    data["decode"].pop(data["encode"][inp], None)
    data["encode"].pop(inp, None)

    with open(langPath + 'index.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)

    os.remove(langPath + inp + '.json')



def generateTableJson(name, seed):
    for i in range(0, 10):
        #Creates index in index.json for the Table identifier
        with open(langPath + 'index.json', encoding='utf-8') as json_file:
            data = json.load(json_file)

        data.pop(name, None)
        for id in list(data["decode"]):
            if data["decode"][id] == name:
                data["decode"].pop(id, None)

        output = False
        if seed == 0: # if the seed is unspecified generate a new one
            output = True
            id = []
            for i in range(0, 7):
                id.append(generator())

            while "".join(id) in data["decode"]:
                id = []
                for i in range(0, 5):
                    id.append(generator())

            seed = "".join(id)

        data["decode"][seed] = name
        data["encode"][name] = seed



        #Generates the file. "LetterList" represents possible Letter and Symbols, that are translatable
        LetterList = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","Ö","ö","Ü","ü","Ä","ä","ß",".",",","*","!","?","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
        TableChar = {}

        newTable = generateCharacter(len(LetterList), seed)
        I = 0
        for Letter in LetterList:
            TableChar[Letter] = newTable[I]
            I = I + 1

        with open(langPath + name + '.json', 'w', encoding="utf-8") as jsonFile:
            json.dump(TableChar, jsonFile)


        with open(langPath + 'index.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file)

        if output == True:
            # Prints a Test string for the new Table
            String = """AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789ÖöÜüÄäß., !?+-@&%()=/\\"':;<>[]^_~{}"""
            if decodePrep(encodePrep(String)) != String:
                continue
            else:
                return





def encodePrep(String):
    if getTables() == []:
        generateTableJson("standard", 0)


    secretsGenerator = secrets.SystemRandom()
    curTable = getTables()[secretsGenerator.randint(0, len(getTables())- 1)]


    String = str(String).replace(" ","*") #Convert spaces to * so json and Pythons list() can handle it
    endlist = []
    StringForm = list(String)
    with open(langPath + 'index.json', encoding='utf-8') as json_file:  #Add Table identifier to Output
        data = json.load(json_file)
        endlist.append(data["encode"][curTable])

    for item in StringForm:
        endlist.append(encode(item, curTable))


    global LAST
    LAST = "".join(endlist)
    return "".join(endlist)

def decodePrep(inp):
    with open(langPath + 'index.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    try:
        table = data["decode"][inp[0:7]]
    except:
        name = "1"
        while name in getTables():
            name = int(name)
            name = name + 1
            name = str(name)

        generateTableJson(str(name), inp[0:7])

        with open(langPath + 'index.json', encoding='utf-8') as json_file:
            data = json.load(json_file)

        succes = decode((inp[7:]),"False", data["decode"][inp[0:7]]).replace("*", " ").replace("  ", " ")
        if succes.isspace() == True or succes == "":
            delTable(data["decode"][inp[0:7]])
            return


    try:
        table = data["decode"][inp[0:7]]
        inp = inp[7:]

        return decode((inp),"False", table).replace("*", " ").replace("  ", " ")

    except:
        return









def commands(dencode):
    global curTable
    dencode = dencode.lower()
    if dencode.lower() == "v":    # Encode a String given by user
        print(encodePrep(input("Text: ")))


    elif dencode.lower() == "e" or dencode.lower() == "l":  #decode a string given by the user
        if dencode.lower() == "e":
            inp = str(input("Text: "))
            if inp == "stop":
                return
        elif dencode.lower() == "l":
            inp = LAST

        print(decodePrep(inp))




    elif dencode.lower() == "n" or dencode.lower() == "new":
        inp = str(input("Name: "))
        if inp == "stop":
            return
        while inp == "index":
            print("Index.json ist ein verbotener Name.")
            inp = str(input("Name: "))
            if inp == "stop":
                return

        generateTableJson(inp, 0)


    elif dencode.lower() == "ls":
        print(", ".join(getTables()))


    elif dencode.lower() == "del":
        inp = str(input("Name: "))
        if inp == "stop":
            return
        while inp == "index":
            print("Index.json ist ein verbotener Name.")
            inp = str(input("Name: "))
            if inp == "stop":
                return

        while inp not in getTables():
            print("Existiert nicht!")
            inp = str(input("Name: "))
            if inp == "stop":
                return

        delTable(inp)

    elif dencode == "exit" or dencode == "exit()":
        exit()


def UI():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Dieses Programm übersetzt in eine komische Sprache")
    while True:
        print("\n\n+----------------------------------------------------------------------------------------------------------------+\n")
        dencode = input("Tabellenliste: ls, Neue Tabelle: N, Tabelle löschen: del, Entschlüsseln: E, Verschlüsseln: V: ")
        commands(dencode)


def run(mode, arguments):
    if mode == 1:
        UI()
    if mode == 0:
        commands(arguments)






# Mode 1 is with user interface, Mode 0 is for applications that use this script
run(0, "Hallo")
#run(1, None)
