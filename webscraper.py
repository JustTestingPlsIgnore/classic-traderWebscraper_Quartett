import requests
from bs4 import BeautifulSoup
import re
import pandas

carlist=[]
base_url = "https://www.classic-trader.com/de/automobile/suche"#fuer suchattribute einfach url der gewuenschten suche hier einfuegen
#bsp: https://www.classic-trader.com/de/automobile/suche?priceMax=7500     

pages= 786 #muss fuer zukuenftige nutzung angepasst werden
#Laufzeit fuer 786 seiten etwa 29 Minuten (Ryzen 5 3600, 32GB RAM)



for page in range(0,pages):
    r=requests.get(base_url+str(f"?page={page}"))
    cont=r.content

    soup=BeautifulSoup(cont,"html.parser")


    cars=soup.find_all("div",{"class":"grid h-full grid-flow-dense p-1 pr-4 pb-3 transition-all duration-100"})
    len(cars)

    
   

    for car in cars:
        #stats erfasst 3-4 wrapper_grids mit 
        #karosserieform, kilometerstand, leitung, manchmal baureihe 
        stats=car.find_all("div",{"class":"data_wrapper_grid"})

        #properties erfasst 'astro-island' buchstabensuppe, enthaellt alle daten zum auto, aber schlechter zu extrahieren
        properties=car.find("astro-island")#
        dict = {}


        #   pattern suchen jahr, name
        pattern = re.compile(r'\b(\d{4}) \| ([A-z\s\d\-\ä\ö\ü\ë]+)\b')
        match = pattern.search(str(properties))
    
        if match:
            year = match.group(1)  
            name = match.group(2)  
            
            dict["baujahr"] = int(year)
            dict["name"] = name
            

    
        price=car.find("span",{"class":"whitespace-nowrap text-xl font-semibold leading-tight lg:text-2xl"})
        price = (price.text)
    
        dict["preis"] = price

        attr = []
        for stat in stats:
                attr.append(stat.text)
        
        if len(attr) == 3:
            dict["baureihe"] = 0
            dict["karosserieform"] = attr[0]
            dict["kilometerstand"] = attr[1]
            dict["leistung"] = attr[2]
        if len(attr) == 4:
            dict["baureihe"] = attr[0]
            dict["karosserieform"] = attr[1]
            dict["kilometerstand"] = attr[2]
            dict["leistung"] = attr[3]

        #in 'astro-island' nach gewichtsangabe suchen und zahl extrahieren
        #kann kopiert und angepasst werden um andere daten zu erfassen:
            #bsp Hubraum:
            #mit inspect element auf website den großen "astro-island" text eines bel. autos finden
            #den zugehoerigen text zum attribut herausfinden (fuer hubraum: "cubicCapacity&quot;:[0,xxxx]")
            #Chatgpt nach einem regex pattern fragen, welches die nummern aus der eckigen klammer extrahiert
            #pattern in unten stehenden code einsetzen, "patternW" und "gewicht" durch andere attributnamen erstzen
            #wenn attribut keine ganzzahlige nummer ist, int() durch float() für kommazahlen ersetzen oder weglassen
        patternW = re.compile(r'weightInKg&quot;:\[.*?,(\d+)\]')
        match = patternW.search(str(properties))
        if match:
            gewicht = match.group(1)  
            dict["gewicht"] = int(gewicht)
        else: dict["gewicht"] = 0




        #unnoetige zeichen aus daten entfernen und ggf datentyp aendern
        if dict["baureihe"] != 0:
            patternB = re.compile(r'Baureihe')
            bdirty = dict["baureihe"]
            bclean = re.sub(patternB, '', bdirty)
            dict["baureihe"] = bclean
        else: dict["baureihe"] = None

        patternK = re.compile(r'Karosserieform')
        kdirty = dict["karosserieform"]
        kclean = re.sub(patternK, '', kdirty)
        dict["karosserieform"] = kclean

        try:
            patternP = re.compile(r'\xa0€')
            pdirty = dict["preis"]
            pclean = re.sub(patternP, '', pdirty)
            dict["preis"] = "{:0.3f}".format(float(pclean))
        except: dict["preis"] = "Auf Anfrage"

        patternL = re.compile(r'Tachostand (abgelesen)')
        ldirty = dict["kilometerstand"]
        lclean = re.sub(patternL, '', ldirty)
        patternL2 = re.compile(r'(\d+\.\d+) (km|mls)')
        match = patternL2.search(str(lclean))
        if match:
            distance = float(match.group(1))  
            unit = match.group(2)  # wenn meilen angegeben, in klm umrechnen
            if unit == 'mls':
                distance *= 1.60934  
            dict["kilometerstand"] = "{:0.3f}".format(distance)
        else: dict["kilometerstand"] = 0

        try:
            patternKW = re.compile(r'\b\d+\b$')
           
            kwdirty = dict["leistung"]
           
            match = patternKW.search(kwdirty)
            if match:
                kwclean = match.group()  
            dict["leistung"] = int(kwclean)
        except: dict["leistung"] = 0
       

        
             
        carlist.append(dict)
       
Autos = pandas.DataFrame(carlist)
print(Autos)
Autos.to_csv("Autos.csv")#daten als csv exportieren

#um daten aus bereits vorhandenem csv zu filtern (in neuem .py file ausfuehren)
"""
import pandas


autos = pandas.read_csv("Autos.csv")
temp_Autos = autos[autos['preis'] != "Auf Anfrage"]#preis auf anfrage ausfiltern
autos_neu = temp_Autos[temp_Autos["gewicht"] != 0]#autos ohne gewichtsangabe ausfiltern
#print(autos_neu)
autos_neu.to_csv("AutosNeu.csv", index=False)


 """


