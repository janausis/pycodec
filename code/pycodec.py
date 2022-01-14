import secrets
import random
import time
import argparse
import requests
import cpuinfo
import os

global Table
global LAST

# See method below
# defaults to Level 3
securityLevel = 4


# Class to write with colors
os.system("")
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


def security(var):  # Sets values for the various security level, simply add "elif" statements for additional levels
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

    UserSeed = secrets.token_hex(int(lange / 2))
    return UserSeed


def generateSeed():  # generate a new, secure, seed, or hash

    global seed
    length = security("sl")
    seed = secrets.token_hex(length)
    return seed


def generator():  # Random "Noise" between the real identifiers. Isn't currently used in this version of the script
    letters = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K",
               "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u",
               "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Ö",
               "ö", "Ü", "ü", "Ä", "ä", ".", ",", "!", "?", "+", "-", "@", "&", "%", "(", ")", "=", "ß", "/", ":", ";",
               "<", ">", "[", "]", "^", "{", "}"]
    return secrets.choice(letters)


def generateCharacter(ListLen, length):  # Random Letters for the Table.json files, generates the values to en- or decode
    random.seed(seed)
    letters = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J", "j", "K",
               "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s", "T", "t", "U", "u",
               "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Ö",
               "ö", "Ü", "ü", "Ä", "ä", ".", ",", "!", "?", "+", "-", "@", "&", "%", "(", ")", "=", "ß", "/", ":", ";",
               "<", ">", "[", "]", "^", "{", "}"]
    Lettercode = list(
        "".join([random.choice(letters) for _ in range(0, random.randint(length, length))]) for _ in range(0, ListLen))
    return Lettercode


def delTable():  # delete a table from /lang
    global Table
    Table = {}


def generateTableJson(seed):  # generate a en-decode table from a seed
    for attempt in range(0, 10):

        # Generates the file. "LetterList" represents possible Letter and Symbols, that are translatable
        LetterList = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h", "I", "i", "J",
                      "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r", "S", "s",
                      "T", "t", "U", "u", "V", "v", "W", "w", "X", "x", "Y", "y", "Z", "z", "0", "1", "2", "3", "4",
                      "5", "6", "7", "8", "9", "Ö", "ö", "Ü", "ü", "Ä", "ä", "*", "_", ".", ",", "!", "?", "+", "-",
                      "@", "&", "%", "(", ")", "=", "ß", "/", ":", ";", "<", ">", "[", "]", "^", "{", "}", "'", "\""]
        TableChar = {}

        random.seed(seed)
        newTable = generateCharacter(len(LetterList), random.randint(security("idl") - 2, security("idl") + 3))
        l = 0
        for Letter in LetterList:
            TableChar[Letter] = newTable[l]
            l = l + 1

        global Table
        Table = TableChar

        return


def decode(String, test=False):
    String = str(String)
    global Table
    data = Table

    WordList = []

    if not test:
        SplitList = []
        random.seed(seed)
        for element in list(range(round(float(len(String)) // float(security("idl"))))):
            code1 = random.randint(security("idl"), security("idl") + 4)
            SplitList.append(random.randint(code1 + 6, code1 + 8))
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


def decodePrep(String, DecodeSeed, Test=False):
    global seed
    seed = DecodeSeed
    generateTableJson(seed)
    output = decode(String, Test).replace("*", " ") # Replace space placeholder
    delTable()
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

            if decode("".join(TempList), True) != str(item):
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
        generateTableJson(seed)

    else:
        generateTableJson(Defseed)
        seed = Defseed

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
            SplitList.append(random.randint(code1 + 6, code1 + 8))

    i = 0
    for item in StringForm:
        out = encode(item, seed, SplitList[i:i + len(list(item))])
        endlist.append(out)
        i = i + len(item)

    delTable()
    global LAST
    LAST = "".join(endlist)
    return seed, "".join(endlist)


def percentage(max, current): # calc. percentage
    return round(current/max*100)


def progress(max, current, divider=4, reverse=False): # generate progress bar
    if divider <= 0:
        divider = 1

    if reverse:
        return str(f"[{style.RED}{round(percentage(max, current)/divider)*'#'}") + str(f"{style.GREEN}{(round(100/divider) - round(percentage(max, current)/divider))*'#'}{style.RESET}]  ")

    else:
        return str(f"[{style.GREEN}{round(percentage(max, current)/divider)*'#'}") + str(f"{style.RED}{(round(100/divider) - round(percentage(max, current)/divider))*'#'}{style.RESET}]  ")


def unifyNumberLength(number): # add 0's to make all numbers match in length after comma
    if "." not in str(number):
        number = str(number) + ".    "

    number1 = str(number).split(".")[-1]
    number2 = str(number).split(".")[-2]

    while len(number1) < 4:
        number1 += " "
    return style.YELLOW + number2 + style.RESET + "." + style.YELLOW + number1 + style.RESET


def output(startenc_time, am, i): # log
    print(
        f"\rPass: {style.YELLOW}{i + 1}{style.RESET}, Time: {unifyNumberLength(round(time.time() - startenc_time, 4))}"
        f", per Pass: {unifyNumberLength(round(float(time.time() - startenc_time) / float(i + 1), 4))} "
        f"{progress(am, i+1)}", end="")


def BSleep(am: int): # wait function between
    print("\n\n\n")
    factor = 10
    am = am*factor
    for i in range(am):
        print(f"Waiting: {progress(am, i + 1, 2)}{round((i+1)/factor, 1)}/{round(am/factor)}s", end="\r")
        time.sleep(1/factor)

    print(79*" ", end="\r")


def easyBench(word, am, seed):
    startenc_time = time.time()
    print(f"\n\n\n------------------------------- Encoding ------------------------------- \n")
    for i in range(am):
        out = encodePrep(word, seed)
        output(startenc_time, am, i)

    endtimeenc = time.time() - startenc_time

    BSleep(5)

    startdec_time = time.time()
    print(f"------------------------------- Decoding ------------------------------- \n")
    for i in range(am):
        dec = decodePrep(out[1], seed)
        output(startdec_time, am, i)

    endtimedec = time.time() - startdec_time

    BSleep(5)

    start_time = time.time()
    print(f"------------------------------- Combined ------------------------------- \n")
    for i in range(am):
        out = encodePrep(word, seed)
        dec = decodePrep(out[1], seed)
        output(start_time, am, i)

    endtime = time.time() - start_time

    return endtime, endtimeenc, endtimedec


def hardBench(word, am, seed):
    startenc_time = time.time()
    print(f"\n\n\n---------------------------- Encoding: Hard ---------------------------- \n")
    for i in range(am):
        out = encodePrep(word, seed)
        output(startenc_time, am, i)

    Hardendtimeenc = time.time() - startenc_time

    BSleep(5)

    startdec_time = time.time()
    print(f"---------------------------- Decoding: Hard ---------------------------- \n")
    for i in range(am):
        dec = decodePrep(out[1], seed)
        output(startdec_time, am, i)

    Hardendtimedec = time.time() - startdec_time

    BSleep(5)

    start_time = time.time()
    print(f"---------------------------- Combined: Hard ---------------------------- \n")
    for i in range(am):
        out = encodePrep(word, seed)
        dec = decodePrep(out[1], seed)
        output(start_time, am, i)

    Hardendtime = time.time() - start_time

    return Hardendtime, Hardendtimeenc, Hardendtimedec

def printHelpText():
    print("\nDer Benchmark Modus kann einen groben Einblick in die Single-Core Performance ermöglichen.\n"
          "In den Modi 1: Leicht, 2: Schwer, 3: Kombiniert, werden deine Zeiten mit anderen verglichen.\n"
          "Der Standard Test lässt 1000-mal Encoden, 1000-mal Decoden und 1000-mal En- und Decoden.\n"
          f"Es muss stets der Seed '{BenchmarkSeed}' verwendet werden wenn die Ergebniss verglichen werden sollen.\n"
          "Das liegt daran das jeder Seed sich anders verhält!"
          "Wenn aber alle den selben Seed verwenden gibt es keine Ungleichheiten,\n"
          "denn bei 1000 runs gleicht sich das Glück aus und die Werte bleiben stabil.\n")


def printWarnText():
    print(f"\n{style.RED}You're now in the \"Advanced Benchmark Mode\".\n{style.RESET}")


def Bench(autostart):
    global seed, am, word, BenchmarkSeed

    word = None
    am = None

    if autostart:
        am = 1000
        seed = BenchmarkSeed

    else:
        printWarnText()
        seed = input("Seed (Leave empty for default): ")
        if seed == "":
            seed = BenchmarkSeed

    if word is None and not autostart:
        word = str(input(f"{style.RESET}Text (Leave empty for comparable Benchmark): "))


    if word == "" or autostart:
        word1 = "Wie nennt man eine französische Militärparade? Eine Massenevakuierung!"
        word2 = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt " \
               "ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo " \
               "dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit " \
               "amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor " \
               "invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et " \
               "justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum " \
               "dolor sit amet."



    print(style.RESET, end="\r")
    if am is None and not autostart:
        while True:
            am = input(f"{style.RESET}Runs (Leer: 1000): ")
            if am == "":
                am = 1000
                break
            else:
                try:
                    am = int(am)
                    break

                except:
                    continue
        print(style.RESET, end="\r")

    seed = "mySeed"  # changing the seed may impact performance!

    mode = input(f"{style.RESET}Choose Difficulty ("
                 f"{style.GREEN  }1{ style.RESET}: {style.GREEN  }Easy{ style.RESET }, "
                 f"{style.RED    }2{ style.RESET}: {style.RED    }Hard{ style.RESET }, "
                 f"{style.YELLOW }3{ style.RESET}: {style.YELLOW }Both{ style.RESET }) "
                 f"Defaults to {style.GREEN}1{style.RESET}: ")

    if mode not in ["1", "2", "3"]:
        mode = 1
    else:
        try:
            mode = int(mode)
        except:
            mode = 1

    input(f"{style.RESET}Press {style.YELLOW}Enter{style.RESET} to begin... ")

    if mode == 1:
        endtime, endtimeenc, endtimedec = easyBench(word1, am, seed)
        print(
            f"\n\n\n\n-------------------------------- Results ------------------------------- \n"
            f"\nCombined Time: {unifyNumberLength(round(endtimeenc + endtimedec + endtime, 4))}, per Pass: {unifyNumberLength(round(float(endtimeenc + endtimedec + endtime) / float(am), 4))}\n\n\n")


    elif mode == 2:
        Hardendtime, Hardendtimeenc, Hardendtimedec = hardBench(word2, am, seed)
        print(
            f"\n\n\n\n-------------------------------- Results ------------------------------- \n"
            f"\nCombined Time: {unifyNumberLength(round(Hardendtimeenc + Hardendtimedec + Hardendtime, 4))}, per Pass: {unifyNumberLength(round(float(Hardendtimeenc + Hardendtimedec + Hardendtime) / float(am), 4))}\n\n\n")


    else:
        endtime, endtimeenc, endtimedec = easyBench(word1, am, seed)
        BSleep(10)
        Hardendtime, Hardendtimeenc, Hardendtimedec = hardBench(word2, am, seed)

        print(
            f"\n\n\n\n----------------------------- Results: Easy ---------------------------- \n"
            f"\nEncoding: {unifyNumberLength(round(endtimeenc, 4))}, per Pass: {unifyNumberLength(round(float(endtimeenc) / float(am), 4))}\n"
            f"Decoding: {unifyNumberLength(round(endtimedec, 4))}, per Pass: {unifyNumberLength(round(float(endtimedec) / float(am), 4))}\n"
            f"Combined: {unifyNumberLength(round(endtime, 4))}, per Pass: {unifyNumberLength(round(float(endtime) / float(am), 4))}\n"
            f"\nCombined Time: {unifyNumberLength(round(endtimeenc + endtimedec + endtime, 4))}, per Pass: {unifyNumberLength(round(float(endtimeenc + endtimedec + endtime) / float(am), 4))}\n\n\n")

        print(
            f"\n----------------------------- Results: Hard ---------------------------- \n"
            f"\nEncoding: {unifyNumberLength(round(Hardendtimeenc, 4))}, per Pass: {unifyNumberLength(round(float(Hardendtimeenc) / float(am), 4))}\n"
            f"Decoding: {unifyNumberLength(round(Hardendtimedec, 4))}, per Pass: {unifyNumberLength(round(float(Hardendtimedec) / float(am), 4))}\n"
            f"Combined: {unifyNumberLength(round(Hardendtime, 4))}, per Pass: {unifyNumberLength(round(float(Hardendtime) / float(am), 4))}\n"
            f"\nCombined Time: {unifyNumberLength(round(Hardendtimeenc + Hardendtimedec + Hardendtime, 4))}, per Pass: {unifyNumberLength(round(float(Hardendtimeenc + Hardendtimedec + Hardendtime) / float(am), 4))}\n\n\n")

        print(
            f"\n--------------------------- Results: Combined -------------------------- \n"
            f"\nCombined Time: {unifyNumberLength(round(Hardendtimeenc + Hardendtimedec + Hardendtime + endtimeenc + endtimedec + endtime, 4))}"
            f", per Pass: {unifyNumberLength(round(float(Hardendtimeenc + Hardendtimedec + Hardendtime + endtimeenc + endtimedec + endtime) / float(am), 4))}\n\n\n\n")

    input(f"\n\n {style.RESET}Press {style.YELLOW}Enter{style.RESET} to return... ")

def GUI():
    print("GUI not here yet!")


if __name__ == '__main__':
    BenchmarkSeed = "mySeed"
    word = None
    am = None

    parser = argparse.ArgumentParser(description='Codec by Jannis Martensen')
    parser.add_argument("-e", type=str, default=None, help='Encrypt a message')
    parser.add_argument("-d", type=str, default=None, help='Decrypt a message')
    parser.add_argument("-s", type=str, default=None, help='Set the seed to use')
    parser.add_argument("-b", action='store_true', help='Benchmark Mode')
    parser.add_argument("-ab", action='store_true', help='Advanced Benchmark Mode')
    parser.add_argument("-g", action='store_true', help='GUI Mode')

    args = parser.parse_args()
    ArgsSeed = args.s
    benchmark = args.b
    AdvancedBenchmark = args.ab

    guiMode = args.g
    con = False
    if args.e is None and args.d is None and not args.b and not args.ab and not args.g:
        con = True

    if args.e is not None:
        enc = args.e
    else:
        enc = None

    if args.d is not None:
        dec = args.d
    else:
        dec = None

    if benchmark or AdvancedBenchmark:
        #printHelpText()
        Bench(not AdvancedBenchmark)


    elif guiMode:
        GUI()


    elif con:

        while True:
            print("\n\n\n------------------------------------------ Actions -----------------------------------------\n")
            action = input(f"What do you want to do? ({style.BLUE}e{style.RESET}: {style.BLUE}Encrypt{style.RESET} | {style.GREEN}d{style.RESET}: {style.GREEN}Decrypt{style.RESET} | {style.YELLOW}b{style.RESET}: {style.YELLOW}Benchmark{style.RESET} | {style.RED}exit{style.RESET}: {style.RED}Exit{style.RESET}): ")
            if action.lower() == "d":

                if ArgsSeed is None:
                    seed = input("Seed: ")
                else:
                    seed = ArgsSeed
                inp = input("Text: ")
                print("\n\n")
                print(decodePrep(inp, seed))

            elif action.lower() == "e":
                if ArgsSeed is None:
                    seed = input("Seed: ")
                else:
                    seed = ArgsSeed

                inp = input("Text: ")
                print("\n\n")
                print(encodePrep(inp, seed)[1])

            elif action.lower() == "b":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                #printHelpText()
                Bench(not AdvancedBenchmark)
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

            elif action.lower() == "exit":
                break

    elif enc:
        print("\n\n")
        seed = ArgsSeed
        print(encodePrep(enc, seed)[1])
        input(f"{style.RESET}Press {style.YELLOW}Enter{style.RESET} to return... ")

    elif dec:
        print("\n\n")
        seed = ArgsSeed
        print(decodePrep(dec, seed))
        input(f"{style.RESET}Press {style.YELLOW}Enter{style.RESET} to return... ")
