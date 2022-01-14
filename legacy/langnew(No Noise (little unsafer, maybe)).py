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


# 1: Seed length(8), letterlength(7)  , identifierLength(4)
# 2: Seed length(16), letterlength(10), identifierLength(5)
# 3: Seed length(32), letterlength(15), identifierLength(6)
securityLevel = 2
# defaults to Level 2




def security(var):
    if securityLevel == 1:
        seedLegth = 8
        IDLen = 8
    elif securityLevel == 2:
        seedLegth = 16
        IDLen = 10
    elif securityLevel == 3:
        seedLegth = 32
        IDLen = 15
    else:
        seedLegth = 16
        IDLen = 10

    if var.lower() == "sl":
        return seedLegth
    elif var.lower() == "idl":
        return IDLen# Sets values for the various security level, simply add "if" statements for additional levels

def generateSeed():

    global seed
    seed = secrets.token_hex(security("sl"))
    return seed# generate a new, secure, seed, or hash

def generator():
    letters = ["A","a","B","b","C","c","D","d","E","e","f","F","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","ö","Ö","Ü","ü","ä","Ä","!","?",".","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
    return secrets.choice(letters) # Random "Noise" inbetween the real identifiers# Isn't currently used in this version of the script, see "lang(with noise)"

def generateCharacter(ListLen, seed, len):
    random.seed(seed)
    letters = ["A","a","B","b","C","c","D","d","E","e","f","F","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","ö","Ö","Ü","ü","ä","Ä","!","?",".","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
    Lettercode = list("".join([random.choice(letters) for _ in range(0, random.randint(len, len))]) for _ in range(0, ListLen))
    return Lettercode# Random Letters for the Table.json files# generate the values to en- or decode

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

def delTable(String):
    os.remove(langPath + String + '.json')# delete a table from /lang

def generateTableJson(name, seed):
    for i in range(0, 10):


        #Generates the file. "LetterList" represents possible Letter and Symbols, that are translatable
        LetterList = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","Ö","ö","Ü","ü","Ä","ä","ß",".",",","*","!","?","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
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
        return# generate a en-decode table from a seed


def decode(String):
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
    generateTableJson("temp", seed)

    output = decode(String).replace("*", " ").strip() #.replace("*", " ").replace("  ", " ")
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

def encodePrep(String):
    generateTableJson("temp", generateSeed())


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
    return "".join(endlist)







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
