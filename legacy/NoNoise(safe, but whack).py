import secrets
import random
import json
import string
import time
import os


dir = os.path.dirname(os.path.realpath(__file__))
langPath = dir + "/lang/"

if os.path.exists(langPath) == False:
    os.mkdir(langPath)


securityLevel = 4
# defaults to Level 3




def security(var): # Sets values for the various security level, simply add "if" statements for additional levels
    if securityLevel == 1:
        seedLength = 16
        IDLen = 8
    elif securityLevel == 2:
        seedLength = 32
        IDLen = 8
    elif securityLevel == 3:
        seedLength = 16
        IDLen = 10
    elif securityLevel == 4:
        seedLength = 32
        IDLen = 10
    elif securityLevel == 5:
        seedLength = 32
        IDLen = 15
    else:
        seedLength = 16
        IDLen = 10

    if var.lower() == "sl":
        return int(round(seedLength / 2, 0))
    elif var.lower() == "idl":
        return IDLen



def OnlyGenerateSeed(länge): # generate a new, secure, seed, or hash

    seed = secrets.token_hex(int(länge / 2))
    return seed


def generateSeed(): # generate a new, secure, seed, or hash

    global seed
    length = security("sl")
    seed = secrets.token_hex(length)
    return seed

def generator(): # Random "Noise" inbetween the real identifiers. Isn't currently used in this version of the script, see "lang(with noise)"
    letters = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","Ö","ö","Ü","ü","Ä","ä",".",",","!","?","+","-","@","&","%","(",")","=","ß","/",":",";","<",">","[","]","^","{","}"]
    return secrets.choice(letters)

def generateCharacter(ListLen, seed, len): # Random Letters for the Table.json files, generates the values to en- or decode
    random.seed(seed)
    letters = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","Ö","ö","Ü","ü","Ä","ä",".",",","!","?","+","-","@","&","%","(",")","=","ß","/",":",";","<",">","[","]","^","{","}"]
    Lettercode = list("".join([random.choice(letters) for _ in range(0, random.randint(len, len))]) for _ in range(0, ListLen))
    return Lettercode

def getTables(): # Returns all .jsons in /lang except index.json. Isn't currently used in this version of the script, see "lang(with noise)"
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

def delTable(String): # delete a table from /lang
    os.remove(langPath + String + '.json')

def generateTableJson(name, seed): # generate a en-decode table from a seed
    for i in range(0, 10):


        #Generates the file. "LetterList" represents possible Letter and Symbols, that are translatable
        LetterList = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","Ö","ö","Ü","ü","Ä","ä","*","_",".",",","!","?","+","-","@","&","%","(",")","=","ß","/",":",";","<",">","[","]","^","{","}"]
        TableChar = {}



        random.seed(seed)
        newTable = generateCharacter(len(LetterList), seed, random.randint(security("idl") - 3, security("idl")))
        I = 0
        for Letter in LetterList:
            TableChar[Letter] = newTable[I]
            I = I + 1

        with open(langPath + 'temp.json', 'w', encoding="utf-8") as jsonFile:
            json.dump(TableChar, jsonFile)



        # Prints a Test string for the new Table
        String = """AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789ÖöÜüÄäß., !?+-@&%()=/\\"':;<>[]^_~{}"""
        #if decode(encode(String)) != String:
            #continue
        #else:
        return


def decode(String, seed):
    with open(langPath + 'temp.json', encoding="utf-8") as json_file:
        data = json.load(json_file)


    WordList = []
    random.seed(seed)
    split = random.randint(security("idl") - 3, security("idl"))
    while True:

        word = String[:split]
        if word.isspace() or word == "" or word == None:
            break

        WordList.append(word)
        String = String[split:]


    returnList = []
    codeList = list(data)
    k = 0
    for it in WordList:
        String=list(WordList[k])
        for item in data: #Iterates over all Keys and if the Value matches the Letter gets appended to the output list
            i = iter(String)
            if all(any(v == ch for v in i) for ch in data[item]):
                returnList.append(item)

        k = k + 1


    return "".join(returnList)

def decodePrep(String, seed):
    generateTableJson("temp", seed)#O6NPl4\\}
    output = decode(String, seed).replace("*", " ")#.strip() #.replace("*", " ").replace("  ", " ")
    delTable("temp")
    return output


def encode(String):
    returnList = []
    secretsGenerator = secrets.SystemRandom()
    with open(langPath + 'temp.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    String=list(String)


    while True:
        returnList = []
        for item in String:
            code = data[item]
            returnList.append(code)


        #if decode(str("".join(returnList))).replace(" ","")!= str(String).replace(" ",""): #Generates a new String until it matches the decoding result, to prevent accidental Letter overlapping
        return "".join(returnList)

def encodePrep(String, Defseed):
    global seed


    if Defseed == None or Defseed == "None":
        seed = generateSeed()
        generateTableJson("temp", seed)

    else:
        generateTableJson("temp", Defseed)
        seed = Defseed
    secretsGenerator = secrets.SystemRandom()

    String = str(String).replace(" ","*") #Convert spaces to * so json and Pythons list() can handle it

    if len(String) < 5:
        StringForm = list(String)
    elif len(String) >= 5:
        d = "*"
        StringForm = [e+d for e in String.split(d) if e]

        for i in StringForm:
            if len(i) > 10:
                StringForm = [String[i:i+10] for i in range(0, len(String), 10)]
                break

    endlist = []
    for item in StringForm:
        out = encode(item)
        endlist.append(out)



    delTable("temp")
    global LAST
    LAST = "".join(endlist)
    return seed, "".join(endlist)






"""
#word = "igwvoeqgbvoüiuvbwüäoi8vbouüvbüuovüvuiOWVBÖBJDHSÖGISHDOILNKÖOHLINGlöoiughbnöoighbnöoiugbh3658416+9741763874eatrjhartj685746385974atjatj638574638574ratjartgjzafgjt"
word = input("word: ")
out = encodePrep(word)
print(f'\n\n\n\n\n----- encode -----: {word}\n')
print(f"Secret: {out}")
print(f"\nSeed: {seed}")
print("\n----- decode -----\n\n")
print(decodePrep(out, seed))
print(word.strip() == decodePrep(out, seed))
print(f"SecrLevel: {securityLevel}")
"""
