import pandas
import random
import time
import sys

all_cars = pandas.read_csv("AutosNeu.csv")

# evtl vor spiel abfragen
quartettgroesse = 32

sleep = 3
# karten auswaehlen:
kartenset = all_cars.sample(n=quartettgroesse)

spieler = kartenset.iloc[:(int(quartettgroesse/2))]  # stapel in mitte teilen
computer = kartenset.iloc[(int(quartettgroesse/2)):]  

attributreihenfolge= ["name", "baujahr", "karosserieform", "preis", "kilometerstand", "leistung", "gewicht"]




#momentane Probleme: keine,
#jahr, preis kilometerstand implementieren, ausgabe verschoenern

def gverliertKarte(spieler, computer):
    print("computer verliert karte")
    
    computer_karte = (computer.iloc[0].to_dict()) #erste karte des computers nehmen
    tempdf = pandas.DataFrame([computer_karte])# dataframe mit dieser karte erstellen, append gibts aus irgend nem grund net
    spieler = pandas.concat([spieler, tempdf], ignore_index=True)# concat als erstaz nutzen um tempdf an spieler anzuhaengen 
    computer = computer.drop(computer.index[0])#computer die karte wegnehmen
    computer = computer.reset_index(drop=True)#reset zur sicherheit

    spieler_karte = (spieler.iloc[0].to_dict()) #erste karte des spielers ans ende tun
    tempdf2 = pandas.DataFrame([spieler_karte])
    spieler = pandas.concat([spieler, tempdf2], ignore_index=True)
    spieler = spieler.drop(spieler.index[0])

    
    spieler = spieler.reset_index(drop=True)
    print(f"karten spieler: {len(spieler)}")
    print(f"karten computer: {len(computer)}")
    #print()
    print("------------------------------------------------")
    print()

    play_game(spieler, computer, True)

def sverliertKarte(spieler, computer):
    print("spieler verliert karte")
    spieler_karte = spieler.iloc[0].to_dict()
    tempdf = pandas.DataFrame([spieler_karte])
    computer = pandas.concat([computer, tempdf], ignore_index=True)
    spieler = spieler.drop(spieler.index[0])
    spieler = spieler.reset_index(drop=True)
    

    computer_karte = computer.iloc[0].to_dict()
    tempdf2 = pandas.DataFrame([computer_karte])
    computer = pandas.concat([computer, tempdf2], ignore_index=True)
    computer = computer.drop(computer.index[0]) 

    
    computer = computer.reset_index(drop=True)
    print(f"karten spieler: {len(spieler)}")
    print(f"karten computer: {len(computer)}")
    #print()
    print("------------------------------------------------")
    print()

    play_game(spieler, computer, False)



def vergleichG(spieler, computer):
    sgewicht = spieler.loc[0,"gewicht"]
    ggewicht = computer.loc[0,"gewicht"]
    print(f"dein Gewicht: {sgewicht}")
    print(f"Gewicht Gegner: {ggewicht}")
    if sgewicht > ggewicht :
        sverliertKarte(spieler, computer)
    if sgewicht < ggewicht:
        gverliertKarte(spieler, computer)
    else: 
        print("gleichstand, vergleiche Leistung")
        vergleichL(spieler, computer)
    


def vergleichL(spieler, computer):
    sleistung = spieler.loc[0,"leistung"]
    gleistung = computer.loc[0,"leistung"]
    print(f"deine PS: {sleistung}")
    print(f"PS des Gegners: {gleistung}")
    if sleistung < gleistung :
        sverliertKarte(spieler, computer)
    if sleistung > gleistung:
        gverliertKarte(spieler, computer)
    else: 
        print("gleichstand, vergleiche Baujahr")
        vergleichJ(spieler, computer)

def vergleichJ(spieler, computer):
    sbaujahr = spieler.loc[0,"baujahr"]
    gbaujahr = computer.loc[0,"baujahr"]
    print(f"Baujahr deines Autos: {sbaujahr}")
    print(f"Baujahr Auto des Gegners: {gbaujahr}")
    if sbaujahr > gbaujahr :
        sverliertKarte(spieler, computer)
    if sbaujahr < gbaujahr:
        gverliertKarte(spieler, computer)
    else: 
        print("gleichstand, vergleiche Preis")
        vergleichP(spieler, computer)

def vergleichP(spieler, computer):
    spreis = spieler.loc[0,"preis"]
    gpreis = computer.loc[0,"preis"]
    print(f"Preis deines Autos: {spreis}")
    print(f"Preis Auto des Gegners: {gpreis}")
    if spreis < gpreis :
        sverliertKarte(spieler, computer)
    if spreis > gpreis:
        gverliertKarte(spieler, computer)
    else: 
        print("gleichstand, vergleiche Kilometerstand")
        vergleichK(spieler, computer)

def vergleichK(spieler, computer):
    skilometerstand = spieler.loc[0,"kilometerstand"]
    gkilometerstand = computer.loc[0,"kilometerstand"]
    print(f"Kilometerstand deines Autos: {skilometerstand}")
    print(f"Kilometerstand Auto des Gegners: {gkilometerstand}")
    if skilometerstand > gkilometerstand :
        sverliertKarte(spieler, computer)
    if skilometerstand < gkilometerstand:
        gverliertKarte(spieler, computer)
    else: 
        print("gleichstand, vergleiche Leistung")
        vergleichL(spieler, computer)

    



def play_game(spieler, computer, istSpielerDran):
    if istSpielerDran == True:
        if spieler.empty == False and computer.empty == False:
            spieler.reset_index(drop=True, inplace=True)
            computer.reset_index(drop=True, inplace=True)

      
            print("Deine Karte:")
            print(spieler.iloc[0][attributreihenfolge])
            
            
            print()
            attribut = input("waehle 1 attribut: (g - gewicht | l - leistung | j - jahr | p - preis | k - kilometerstand)\n")
            if attribut == "g":
                vergleichG(spieler, computer)
                
            if attribut == "l":
                vergleichL(spieler, computer)
                
            if attribut == "j":
                vergleichJ(spieler, computer)
                
            if attribut == "p":
                vergleichP(spieler, computer)
                
            if attribut == "k":
                vergleichK(spieler, computer)
                
            if attribut == "exit":
                print("Spiel beendet")
                sys.exit()
            else: print("Gib ein valides zeichen ein, oder 'exit' zum beenden")
            play_game(spieler, computer, True)
        elif spieler.empty: 
            print("Du hast verloren")
            sys.exit()
        else: 
            print("Du hast gewonnen")
            sys.exit()

    else:#Gegner ist dran
        if spieler.empty == False and computer.empty == False:
            spieler.reset_index(drop=True, inplace=True)
            computer.reset_index(drop=True, inplace=True)

          
            print("Deine Karte:")
            print(spieler.iloc[0][attributreihenfolge])
            

            time.sleep(sleep)
            
            print("Computer ist dran!")
            
            
            auswahl = ["g","k","p","j","l"]
            attribut = auswahl[random.randint(0,4)]# computer waehlt attribut (semi-)zufaellig
            if attribut == "g":
                print("computer waehlt Gewicht!")
                time.sleep(sleep)
                vergleichG(spieler, computer)
                
            if attribut == "l":
                print("computer waehlt Leistung!")
                time.sleep(sleep)
                vergleichL(spieler, computer)
                
            if attribut == "j":
                print("computer waehlt Baujahr!")
                time.sleep(sleep)
                vergleichJ(spieler, computer)
                
            if attribut == "p":
                print("computer waehlt Preis!")
                time.sleep(sleep)
                vergleichP(spieler, computer)
               
            if attribut == "k":
                print("computer waehlt Kilometerstand!")
                time.sleep(sleep)
                vergleichK(spieler, computer)
                
        elif spieler.empty: 
            print("Du hast verloren")
            sys.exit()

        else: 
            print("Du hast gewonnen")
            sys.exit()

play_game(spieler,computer, True)
