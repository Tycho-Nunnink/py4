#---------------------------------------------------------------------
from os import system, listdir
from time import sleep
from random import choice
#---------------------------------------------------------------------

def scherm(inhoud):
    SCHERMBREEDTE = 80
    SCHERMHOOGTE = 20
    print(f"{'='*SCHERMBREEDTE}\n|{' '*(SCHERMBREEDTE-2)}|")
    it = iter(inhoud)
    for i in range(SCHERMHOOGTE-4):
        print(f"| {str(next(it, '')):<{SCHERMBREEDTE-3}}|")
    print(f"|{' '*(SCHERMBREEDTE-2)}|\n{'='*SCHERMBREEDTE}")

def langscherm(inhoud):
    SCHERMBREEDTE = 80
    print(f"{'='*SCHERMBREEDTE}\n|{' '*(SCHERMBREEDTE-2)}|")
    for i in inhoud:
        print(f"| {str(i):<{SCHERMBREEDTE-3}}|")
    print(f"|{' '*(SCHERMBREEDTE-2)}|\n{'='*SCHERMBREEDTE}")

def dictmaker(lijstnaam):
    dictionary = {}
    with open(lijstnaam + ".wrd", "r") as file:
        for i in file:
            woord1, woord2 = i.strip("\n").split("\t")
            dictionary[woord1] = woord2
    return dictionary

def pauze():
    input("druk enter om verder te gaan")

def afscheid():
    scherm(["doei, doei!"])
    sleep(1)

#---------------------------------------------------------------------

def overhoren(flijst, fclr):#niet nu doe ik als laatste
    fkeuze = ""
    while fkeuze != "q":
        system(fclr)
        randomwoord = choice(list(flijst.keys()))
        scherm(["vertaal:",f"    {randomwoord}"])
        fkeuze = input("raad het woord: ")
        system(fclr)
        if fkeuze == flijst[randomwoord]:
            printlijst = ["dat is correct!",f"{randomwoord} betekent inderdaad {flijst[randomwoord]}!"]
        else:
            printlijst = ["jammer, dat is fout,",f"{randomwoord} betekent {flijst[randomwoord]}."]
        scherm(printlijst + ["","kies:","    •d om het woord te verwijderen","    •q om te stoppen","    •of druk enter om verder te gaan"])
        fkeuze = input("kies een optie: ")
        if fkeuze == "d":
            flijst = verwijder(randomwoord, flijst)     
    return flijst

def vertaal(naam, flijst):
    if naam in flijst:
        scherm([f"{naam} betekent {flijst[naam]}"])
        pauze()
    else:
        scherm([f"{naam} heeft geen vertaling"])
        sleep(1)

def lijstprint(flijst):
    langscherm(["de geselecteerde lijst bevat:"] + [f"    •{x[0]} = {x[1]}" for x in flijst.items()])
    pauze()

def lijstlijstprint(flijstlijst):
    langscherm(["je hebt keuze uit:"] + [f"    •{x}" for x in flijstlijst])
    pauze()

def kies(fkeuze, flijstlijst, fcurrent_lijst, flijst):#werkt nog niet moet lijstlijst nog maken
    if fkeuze in flijstlijst:
        fcurrent_lijst = fkeuze
        func_lijst = dictmaker(fkeuze)
        return fcurrent_lijst, func_lijst
    else:
        scherm(["die lijst bestaat niet!"])
        sleep(1)
        return fcurrent_lijst, flijst

def toevoegen(woord, vertaling, flijst):
    if woord in flijst:
        scherm([f"{woord} heeft al een vertaling, wil je het vervangen? j/n"])
        c = input("kies een optie: ") 
        if c == "j" or c == "ja":
            flijst[woord] = vertaling
    else:
        flijst[woord] = vertaling
    return flijst

def verwijder(woord, flijst):
    if woord in flijst:
        del flijst[woord]
        return flijst
    else:
        scherm([f"{woord} heeft geen vertaling"])
        sleep(1)

def opslaan(flijst, naam):
    if len(flijst) > 0:
        savestring = ""
        for key, value in flijst.items():
            savestring += f"{key}\t{value}\n"
        savestring = savestring.rstrip("\n")
        with open(naam+".wrd", "w") as file:
            file.write(savestring)
        return True, [x.split(".")[0] for x in listdir() if "." in x and x.split(".")[1] == "wrd"]
    else:
        scherm(["kan geen lege lijst opslaan"])
        sleep(1)

#---------------------------------------------------------------------

def main():
    with open("kies-lijst.txt", "r") as file:
        current_lijst = file.read()
    lijstlijst = [x.split(".")[0] for x in listdir() if "." in x and x.split(".")[1] == "wrd"]
    saved = True
    keuze = [1,2,3]
    lijst = dictmaker(current_lijst)
    CLR = "cls" #verander dit als je apple hebt naar "clear"
    menu = lambda : ["geselecteerde lijst:",f"    {current_lijst}","","kies:","    •o om jouw lijst te overhoren","    •v <woord> om een woord te vertalen","    •l om jouw lijst te tonen","    •ll voor een lijst van lijsten","    •k <naam> om een lijst te kiezen","    •n <naam> voor een nieuwe lijst","    •t <woord> <vetaling> om woorden toe te voegen aan je lijst","    •d <woord> om een woord te verwijderen" ,"    •s om je lijst op te slaan","    •q om het programma af te sluiten"]
    while keuze[0] != "q":
        system(CLR)
        if keuze[0] == "o":#overhoren
            lijst = overhoren(lijst, CLR)
        elif keuze[0] == "v" and len(keuze) > 1:#vertaal
            vertaal(keuze[1], lijst)
        elif keuze[0] == "l":#lijst tonen
            lijstprint(lijst)
        elif keuze[0] == "ll":#lijsten tonen
            lijstlijstprint(lijstlijst)
        elif keuze[0] == "k" and len(keuze) > 1:#lijst kiezen
            current_lijst, lijst = kies(keuze[1], lijstlijst, current_lijst, lijst)
        elif keuze[0] == "n" and len(keuze) > 1:#nieuwe lijst
            current_lijst, lijst, saved = keuze[1], {}, True
        elif keuze[0] == "t" and len(keuze) > 2:#toevoegen
            lijst = toevoegen(keuze[1], keuze[2], lijst)
        elif keuze[0] == "d" and len(keuze) > 1:#delete
            lijst = verwijder(keuze[1], lijst)
        elif keuze[0] == "s":#save
            saved, lijstlijst = opslaan(lijst, current_lijst)
        elif keuze[0] == "26951":#geheimpje en eigenlijk niet meer in gebruik door l
            scherm(lijst.items())
            pauze()
        elif keuze != [1,2,3] and keuze != [""] and keuze != ["q"]:
            scherm(["dat is geen optie"])
            sleep(1)

        
        system(CLR)
        scherm(menu())
        keuze = input("kies een optie: ").split(" ")
    system(CLR)
    afscheid()
    system(CLR)
    if saved:#zodat het geen lijst probeert te kiezen die niet bestaat
        file = open("kies-lijst.txt", "w")
        file.write(current_lijst)
        file.close()

main()