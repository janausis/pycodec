import secrets
import random
import time

global Table

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
        IDLen = 5
    elif securityLevel == 4:
        seedLength = 32
        IDLen = 5
    elif securityLevel == 5:
        seedLength = 32
        IDLen = 8
    else:
        seedLength = 16
        IDLen = 5

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


def delTable(String):  # delete a table from /lang
    global Table
    Table = {}


def generateTableJson(name, seed):  # generate a en-decode table from a seed
    for i in range(0, 10):

        # Generates the file. "LetterList" represents possible Letter and Symbols, that are translatable
        LetterList = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J",
                      "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s",
                      "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "0", "1", "2", "3", "4",
                      "5", "6", "7", "8", "9", "Ö", "ö", "Ü", "ü", "Ä", "ä", "*", "_", ".", ",", "!", "?", "+", "-",
                      "@", "&", "%", "(", ")", "=", "ß", "/", ":", ";", "<", ">", "[", "]", "^", "{", "}", "'", "\""]
        TableChar = {}

        random.seed(seed)
        newTable = generateCharacter(len(LetterList), seed, random.randint(security("idl") - 2, security("idl") + 3))
        I = 0
        for Letter in LetterList:
            TableChar[Letter] = newTable[I]
            I = I + 1

        global Table
        Table = TableChar

        return


def decode(String, seed, test=False):
    String = str(String)
    global Table
    data = Table

    WordList = []

    if not test:
        SplitList = []
        random.seed(seed)
        for item in list(range(round(float(len(String)) // float(security("idl"))))):
            code1 = random.randint(security("idl"), security("idl") + 4)
            SplitList.append(random.randint(code1 + 4, code1 + 6))
    else:
        SplitList = [len(String) - 1]

    random.seed(seed)
    split = 0
    while True:

        try:
            word = String[:SplitList[split]]
        except IndexError:
            break

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


def decodePrep(String, seed, Test=False):
    generateTableJson("temp", seed)  # O6NPl4\\}
    output = decode(String, seed, Test).replace("*", " ")  # .strip() #.replace("*", " ").replace("  ", " ")
    delTable("temp")
    return output


def encode(String, seed, WordLengthList):
    secretsGenerator = secrets.SystemRandom()

    global Table
    data = Table

    returnList = []
    WLList = []
    i = 0
    random.seed(seed)
    for item in String:
        WordLength = WordLengthList[i]

        WLList.append(WordLength)
        try:
            code = data[item]
        except KeyError:
            print("Illegal Letter")
            return

        codeList = list(code)
        charLen = len(list(range(WordLength)))
        while True:
            codeChar = 0
            TempList = []
            for char in range(WordLength):

                if (charLen - char) <= codeChar or secretsGenerator.randint(0, 2) == 0:

                    if 0 <= codeChar < len(codeList):
                        TempList.append(codeList[codeChar])
                        codeChar = codeChar + 1
                    else:
                        TempList.append(generator())

                else:
                    TempList.append(generator())

            if decode("".join(TempList), seed, True) != str(item):
                continue
            else:
                returnList.append("".join(TempList))
                i = i + 1
                break

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

    endlist = []
    SplitList = []
    random.seed(seed)
    for item in StringForm:
        for i in list(item):
            code1 = random.randint(security("idl"), security("idl") + 4)
            SplitList.append(random.randint(code1 + 4, code1 + 6))

    i = 0
    for item in StringForm:
        out = encode(item, seed, SplitList[i:i + len(list(item))])
        endlist.append(out)
        i = i + len(item)

    delTable("temp")
    global LAST
    LAST = "".join(endlist)
    return seed, "".join(endlist)
