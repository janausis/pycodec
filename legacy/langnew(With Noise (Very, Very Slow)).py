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
securityLevel = 3
# defaults to Level 2




def security(var):
    if securityLevel == 1:
        letterlength = 8
        seedLegth = 8
        IDLen = 4
    elif securityLevel == 3:
        letterlength = 15
        seedLegth = 32
        IDLen = 7
    else:
        letterlength = 12
        seedLegth = 16
        IDLen = 5

    if var.lower() == "sl":
        return seedLegth
    elif var.lower() == "ll":
        return letterlength
    elif var.lower() == "idl":
        return IDLen

def generateSeed():

    global seed
    seed = secrets.token_hex(security("sl"))
    return seed

def generator():
    letters = ["A","a","B","b","C","c","D","d","E","e","f","F","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","ö","Ö","Ü","ü","ä","Ä","!","?",".","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
    return secrets.choice(letters) # Random "Noise" inbetween the real identifiers

def generateCharacter(ListLen, seed, len):
    random.seed(seed)
    letters = ["A","a","B","b","C","c","D","d","E","e","f","F","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","ö","Ö","Ü","ü","ä","Ä","!","?",".","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
    Lettercode = list("".join([random.choice(letters) for _ in range(0, random.randint(len, len))]) for _ in range(0, ListLen))
    return Lettercode# Random Letters for the Table.json files

def getTables(): # Returns all .jsons in /lang except index.json
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
    os.remove(langPath + String + '.json')

def generateTableJson(name, seed):
    for i in range(0, 10):


        output = False
        if seed == 0: # if the seed is unspecified generate a new one
            output = True
            generateSeed()



        #Generates the file. "LetterList" represents possible Letter and Symbols, that are translatable
        LetterList = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h","I","i","J","j","K","k","L","l","M","m","N","n","O","o","P","p","Q","q","R","r","S","s","T","t","U","u","V","v","W","w","X","x","Y","y","Z","z","0","1","2","3","4","5","6","7","8","9","Ö","ö","Ü","ü","Ä","ä","ß",".",",","*","!","?","+","-","@","&","%","(",")","=","ß","/","\\",":",";","<",">","[","]","^","_","~","{","}"]
        TableChar = {}




        newTable = generateCharacter(len(LetterList), seed, security("idl"))
        I = 0
        for Letter in LetterList:
            TableChar[Letter] = newTable[I]
            I = I + 1

        with open(langPath + 'temp.json', 'w', encoding="utf-8") as jsonFile:
            json.dump(TableChar, jsonFile)



        # Prints a Test string for the new Table
        String = """AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789ÖöÜüÄäß., !?+-@&%()=/\\"':;<>[]^_~{}"""
        if decode(encode(String)) != String:
            continue
        else:
            return



def decode(String):
    with open(langPath + 'temp.json', encoding="utf-8") as json_file:
        data = json.load(json_file)





    WordList = []
    random.seed(seed)
    while True:

        split = random.randint(security("idl") + 3, security("ll"))
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

    output = decode(String)#.replace("*", " ").replace("  ", " ")
    delTable("temp")
    return output


def encode(String):
    returnList = []
    secretsGenerator = secrets.SystemRandom()
    with open(langPath + 'temp.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    String=list(String)




    while True:
        charLenListList = []
        random.seed(seed)
        for item in String:
            charLenListList.append(list(range(0, random.randint(security("idl") + 3, security("ll")))))


        returnList = []
        x = 0
        for item in String:
            try:
                code = data[item]
            except:
                return ""


            codeList = list(code)

            charLenList = charLenListList[x]
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

            x = x +1
        if decode(str("".join(returnList))).replace(" ","")!= str(String).replace(" ",""): #Generates a new String until it matches the decoding result, to prevent accidental Letter overlapping
            return str("".join(returnList))

def encodePrep(String):
    generateTableJson("temp", generateSeed())


    secretsGenerator = secrets.SystemRandom()


    String = str(String).replace(" ","*") #Convert spaces to * so json and Pythons list() can handle it

    if len(String) < 5:
        StringForm = list(String)
    elif len(String) >= 5:
        StringForm = String.split(" ")
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



word = "igwvoeqgbvoüiuvbwüäoi8vbouüvbüuovüvuiOWVBÖBJDHSÖGISHDOILNKÖOHLINGlöoiughbnöoighbnöoiugbh3658416+9741763874eatrjhartj685746385974atjatj638574638574ratjartgjzafgjt"
word = "Hallo wie geht es dir?"
print(f'----- encode -----: {word}')
out = None
while out == None or decodePrep(out, seed) != word:
    out = encodePrep(word)
    print(decodePrep(out, seed))


print(f"Secret: {out}")
print(f"\nSeed: {seed}")
print("----- decode -----")
print(decodePrep(out, seed))
