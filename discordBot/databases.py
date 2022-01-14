import os
import sqlite3 as sql

dir = os.path.dirname(os.path.realpath(__file__))
databasePath = dir + "/seeds.db"
if os.path.exists(databasePath) == False:
    conn = sql.connect(databasePath)
    conn.execute('CREATE TABLE seeds (user TEXT NOT NULL, seed TEXT NOT NULL, name TEXT NOT NULL, CONSTRAINT user_info UNIQUE (user, seed, name))')
    conn.execute('CREATE TABLE defaults (user TEXT NOT NULL, seed TEXT NOT NULL, name TEXT NOT NULL, UNIQUE (user))')
    conn.execute('CREATE TABLE security (user TEXT NOT NULL, level INT, UNIQUE (user))')
    conn.close()





def newseed(user, seed, name):
    try:
        with sql.connect(databasePath) as con:
            cur = con.cursor()

            cur.execute("SELECT * from seeds WHERE seed = (?) and user = (?)", (str(seed), str(user)))
            if cur.fetchone() != None:
                cur.execute("SELECT name from seeds WHERE seed = (?)", (str(seed),))
                return f"Seed ist schon in benutzung! Name: {cur.fetchone()[0]}"

            cur.execute("SELECT * from seeds WHERE name = (?) and user = (?)", (str(name), str(user)))
            if cur.fetchone() != None:
                cur.execute("SELECT seed from seeds WHERE name = (?)", (str(name)))
                return f"Name ist schon in benutzung! Mit Seed: {cur.fetchone()[0]}"

            cur.execute("SELECT * from seeds WHERE user = (?)", (str(user), ))
            if len(cur.fetchall()) >= 50:
                return f"Du hast dein Limit von 50 erreicht! Benutze !delseed um seeds zu entfernen."




            cur.execute("INSERT INTO seeds (user, seed, name) VALUES (?, ?, ?)",(str(user), str(seed), str(name)))
        return "Erfolgreich hinzugefügt!"
    except:
        return "Es ist ein Fehler aufgetreten!"

def removeseed(user, name):
    try:
        with sql.connect(databasePath) as con:
           cur = con.cursor()
           cur.execute("DELETE FROM seeds WHERE user = (?) and name = (?);",(str(user), str(name)))
           cur.execute("DELETE FROM defaults WHERE user = (?) and name = (?);",(str(user), str(name)))
        return "Succes"
    except:
        return "Error"

def removeallseeds(user):
    try:
        with sql.connect(databasePath) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM seeds WHERE user = (?);",(str(user), ))
            cur.execute("DELETE FROM defaults WHERE user = (?);",(str(user), ))
        return "Succes"
    except:
        return "Error"

def getSeed(user, name):
    with sql.connect(databasePath) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM seeds WHERE user = (?) and name = (?);",(str(user), str(name)))
        result = cur.fetchall()
        if result == []:
            return None
        return "("+"  |  ".join(result[0][1:])+")"

def listSeeds(user):
    try:
        with sql.connect(databasePath) as con:
            cur = con.cursor()

            cur.execute("SELECT * FROM defaults WHERE user = (?) ORDER BY name ASC;",(str(user),))
            outList = ["Default: \n"]
            result = cur.fetchall()
            if result == []:
                outList.append(str("    None\n"))
            for i in result:
                outList.append(str("    "+"  |  ".join(i[1:]))+"\n")

            cur = con.cursor()
            outList.append("\nSaved: \n")


        cur.execute("SELECT * FROM seeds WHERE user = (?) ORDER BY name ASC;",(str(user),))

        result = cur.fetchall()
        if result == []:
            outList.append(str("    None\n"))
        try:
            for i in result:
                outList.append(str("    "+"  |  ".join(i[1:]))+"\n")
            return "".join(outList)
        except:
            pass
        try:
            return "  |  ".join(result[0])
        except:
            try:
                return result
            except:
                return "error"
    except:
        return "Error"

def addStandard(user, name):
    try:
        with sql.connect(databasePath) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM defaults WHERE user = (?);",(str(user), ))
            cur.execute("SELECT seed from seeds WHERE user = (?) and name = (?)", (str(user), str(name)))
            cur.execute("INSERT INTO defaults (user, seed, name) VALUES (?, ?, ?)",(str(user), str(cur.fetchone()[0]), str(name)))
        return "Succes"
    except:
        return "error"

def delStandard(user):
    try:
        with sql.connect(databasePath) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM defaults WHERE user = (?);",(str(user),))
        return "Succes"
    except:
        return "Error"

def hasDefault(user):
    with sql.connect(databasePath) as con:
        cur = con.cursor()
        cur.execute("SELECT seed FROM defaults WHERE user = (?) ORDER BY name ASC;",(str(user),))
        result = cur.fetchone()
        if result == [] or result == "" or result == None:
            return str(None)
        else:
            return str(result[0])

def setSecurity(user, level):
    try:
        with sql.connect(databasePath) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM security WHERE user = (?);",(str(user), ))
            cur.execute("INSERT INTO security (user, level) VALUES (?, ?)",(str(user), level))
        return "Succes"
    except:
        return "error"

def getSecurity(user):
    #try:
    with sql.connect(databasePath) as con:
        cur = con.cursor()
        cur.execute("SELECT level FROM security WHERE user = (?);",(str(user),))
        result = cur.fetchone()
        if result == [] or result == "" or result == None:
            return str(None)
        else:
            return str(result[0])

    #except:
        #return None
