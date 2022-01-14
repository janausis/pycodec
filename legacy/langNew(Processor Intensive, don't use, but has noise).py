import secrets
import random
import json
import os
import time

dir = os.path.dirname(os.path.realpath(__file__))
langPath = dir + "/lang/"

if not os.path.exists(langPath):
    os.mkdir(langPath)

securityLevel = 4


# defaults to Level 3


def security(var):  # Sets values for the various security level, simply add "if" statements for additional levels
    if securityLevel == 1:
        seedLength = 16
        IDLen = 4
    elif securityLevel == 2:
        seedLength = 32
        IDLen = 4
    elif securityLevel == 3:
        seedLength = 16
        IDLen = 6
    elif securityLevel == 4:
        seedLength = 32
        IDLen = 6
    elif securityLevel == 5:
        seedLength = 32
        IDLen = 10
    else:
        seedLength = 16
        IDLen = 10

    if var.lower() == "sl":
        return int(round(seedLength / 2, 0))
    elif var.lower() == "idl":
        return IDLen


def OnlyGenerateSeed(lange):  # generate a new, secure, seed, or hash

    seed = secrets.token_hex(int(lange / 2))
    return seed


def generateSeed():  # generate a new, secure, seed, or hash

    global seed
    length = security("sl")
    seed = secrets.token_hex(length)
    return seed


def generator():  # Random "Noise" inbetween the real identifiers. Isn't currently used in this version of the
    # script, see "lang(with noise)"
    letters = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K",
               "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u",
               "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Ö",
               "ö", "Ü", "ü", "Ä", "ä", ".", ",", "!", "?", "+", "-", "@", "&", "%", "(", ")", "=", "ß", "/", ":", ";",
               "<", ">", "[", "]", "^", "{", "}"]
    return secrets.choice(letters)


def generateCharacter(ListLen, seed,
                      len):  # Random Letters for the Table.json files, generates the values to en- or decode
    random.seed(seed)
    letters = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K",
               "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u",
               "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Ö",
               "ö", "Ü", "ü", "Ä", "ä", ".", ",", "!", "?", "+", "-", "@", "&", "%", "(", ")", "=", "ß", "/", ":", ";",
               "<", ">", "[", "]", "^", "{", "}"]
    Lettercode = list(
        "".join([random.choice(letters) for _ in range(0, random.randint(len, len))]) for _ in range(0, ListLen))
    return Lettercode


def getTables():  # Returns all .jsons in /lang except index.json. Isn't currently used in this version of the script, see "lang(with noise)"
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


def delTable(String):  # delete a table from /lang
    os.remove(langPath + String + '.json')


def generateTableJson(name, seed):  # generate a en-decode table from a seed
    for i in range(0, 10):

        # Generates the file. "LetterList" represents possible Letter and Symbols, that are translatable
        LetterList = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J",
                      "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s",
                      "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "0", "1", "2", "3", "4",
                      "5", "6", "7", "8", "9", "Ö", "ö", "Ü", "ü", "Ä", "ä", "*", "_", ".", ",", "!", "?", "+", "-",
                      "@", "&", "%", "(", ")", "=", "ß", "/", ":", ";", "<", ">", "[", "]", "^", "{", "}"]
        TableChar = {}

        random.seed(seed)
        newTable = generateCharacter(len(LetterList), seed, random.randint(security("idl") - 2, security("idl") + 3))
        I = 0
        for Letter in LetterList:
            TableChar[Letter] = newTable[I]
            I = I + 1

        with open(langPath + 'temp.json', 'w', encoding="utf-8") as jsonFile:
            json.dump(TableChar, jsonFile)

        # Prints a Test string for the new Table
        String = """AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789ÖöÜüÄäß., !?+-@&%()=/\\"':;<>[]^_~{}"""
        # if decode(encode(String)) != String:
        # continue
        # else:
        return


def decode(String, seed):
    with open(langPath + 'temp.json', encoding="utf-8") as json_file:
        data = json.load(json_file)

    WordList = []
    SplitList = []
    random.seed(seed)
    for item in list(range(round(float(len(String)) // float(security("idl"))))):
        code1 = random.randint(security("idl"), security("idl") + 4)
        SplitList.append(random.randint(code1 + 6, code1 + 8))

    random.seed(seed)
    split = 0
    while True:

        word = String[:SplitList[split]]
        if word.isspace() or word == "" or word is None:
            break

        WordList.append(word)
        String = String[SplitList[split]:]
        split = split + 1

    returnList = []
    codeList = list(data)
    k = 0
    for it in WordList:
        String = list(WordList[k])
        for item in data:  # Iterates over all Keys and if the Value matches the Letter gets appended to the output list
            i = iter(String)
            if all(any(v == ch for v in i) for ch in data[item]):
                returnList.append(item)

        k = k + 1

    return "".join(returnList)


def decodePrep(String, seed):
    generateTableJson("temp", seed)  # O6NPl4\\}
    output = decode(String, seed).replace("*", " ")  # .strip() #.replace("*", " ").replace("  ", " ")
    delTable("temp")
    return output


def encode(String, seed, WordLengthList):
    secretsGenerator = secrets.SystemRandom()
    with open(langPath + 'temp.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

    while True:
        returnList = []
        i = 0
        random.seed(seed)
        for item in String:
            WordLength = WordLengthList[i]
            TempList = []
            code = data[item]

            codeList = list(code)
            charLen = len(list(range(WordLength)))
            codeChar = 0
            for char in list(range(WordLength)):

                if secretsGenerator.randint(0, 2) == 0 or (charLen - char) <= codeChar:

                    if 0 <= codeChar < len(codeList):
                        TempList.append(codeList[codeChar])
                        codeChar = codeChar + 1
                    else:
                        TempList.append(generator())

                else:
                    TempList.append(generator())
            returnList.append("".join(TempList))
            i = i + 1

        return "".join(returnList)


def encodePrep(String, Defseed):
    global seed

    if Defseed is None or Defseed == "None":
        seed = generateSeed()
        generateTableJson("temp", seed)

    else:
        generateTableJson("temp", Defseed)
        seed = Defseed
    secretsGenerator = secrets.SystemRandom()

    String = str(String).replace(" ", "*")  # Convert spaces to * so json and Pythons list() can handle it

    if len(String) < 5:
        StringForm = list(String)
    elif len(String) >= 5:
        d = "*"
        StringForm = [e + d for e in String.split(d) if e]

        for i in StringForm:
            if len(i) > 10:
                StringForm = [String[i:i + 10] for i in range(0, len(String), 10)]
                break
    else:
        return "Leeres Wort"

    while True:
        endlist = []
        SplitList = []
        random.seed(seed)
        for item in StringForm:
            for i in list(item):
                code1 = random.randint(security("idl"), security("idl") + 4)
                SplitList.append(random.randint(code1 + 6, code1 + 8))

        i = 0
        for item in StringForm:
            out = encode(item, seed, SplitList[i:i + len(list(item))])
            endlist.append(out)
            i = i + len(item)

        if decode("".join(endlist), seed).replace("*", " ") != str("".join(StringForm)).replace("*", " "):
            continue
        else:
            break

    delTable("temp")
    global LAST
    LAST = "".join(endlist)
    return seed, "".join(endlist)


""" if __name__ == '__main__':
    while True:
        word = input("word: ")
        am = int(input("Runs: "))
        seed = "mySeed"

        start_time = time.time()
        for i in range(am):
            out = encodePrep(word, seed)
            print(out)
            dec = decodePrep(out[1], seed)
            print(dec)

        endtime = time.time() - start_time
        print(f"\n\n\n----- Time ----- \nEs dauerte: {round(endtime, 4)} Sekunden, {am}-mal den Satz {word} zu ver- und "
              f"entschlüsseln. ({round(float(endtime) / float(am), 4)} Sekunden pro run)")

        out = encodePrep(word, seed)
    
        print(f'\n\n\n\n\n----- encode -----: {word}\n')
        print(f"Secret: {out}")
        print(f"\nSeed: {seed}")
        print("\n----- decode -----\n\n")
    
       
        print(decodePrep(out[1], seed))
        print(word.strip() == decodePrep(out[1], seed))
        print(f"SecrLevel: {securityLevel}")"""
