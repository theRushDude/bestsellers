import re, pprint, requests, openpyxl, os
os.chdir(r"C:\Users\Jhube\PycharmProjects\pythonProject")


# Bookmark = Buecherat
# Number = Spiegelde
# Buchstabe = Schwarzer

#ALL VARIABLES USED IN BUECHERAT ; NAMESSACH AND BELL 2 MAL WEIL: SEE STRING SYNTAX BOOKMARK

BuecheratrankBell = []
BuecheratnamesBell = []
BuecheratnamesBell2 = []
BuecherattitleBell = []
BuecheratrankSach = []
BuecheratnamesSach = []
BuecheratnamesSach2 = []
BuecherattitleSach = []


#ALL VARIABLES USED IN SPIEGELDE
SpiegelnamesSach = []
SpiegeltitleSach = []
SpiegelrankSach = []

SpiegelnamesBell = []
SpiegeltitleBell = []
SpiegelrankBell = []


#ALL VARIABLES USED IN SCHWARZER

Schwarzerrank = []                            #GENEREL NAMES USED IN RE - UNSORTED
Schwarzernames = []
Schwarzertitle = []
Schwarzernames2 = []                          # NameList after string formatiing to vorname, nachname


SchwarzerrankBell = []                          #VARIABLES AFTER SORTED INTO BELL AND SACH / STRING FORMATTING
SchwarzernamesBell = []
SchwarzertitleBell = []

SchwarzerrankSach = []
SchwarzernamesSach = []
SchwarzertitleSach = []


#REGULAR EXPRESSION FOR BUECHART
buecheratRE= re.compile(r"""
(\d+?)\.             #Zahl
(</strong>\s\S+\)\s?)?           # neu alte Zahl...
(.+)         #Vorname und Nachname
(:\s?<strong>)
(.+)   #Buchtitel
(</strong>)
""", re.VERBOSE)                        #REbuecherat


 #REGULAR EXPRESSION FOR SPIELGEL.DE
Spiegeltitlere= re.compile(r"""                                                            
(<span\sclass="align-middle">\s)
(.+)                                                                # title
(\s</span>)
""", re.VERBOSE)


Spiegelnamesre= re.compile(r"""
(items-center">\s<li\sclass="mr-8\sflex\sitems-center">\s<p>)
(.+)                                               #names
(</p>\s</li>)
""", re.VERBOSE)


#REGULAR EXPRESSION FOR SCHWARZER
schwarzerre= re.compile(r"""                                # schwarzer titel + autor 3 kategorien rank 1 - 3
(\srel="noopener\snoreferrer">)
(.+)
(:\s)                                                      
(.+)
(</a>.*<br\s/)

""", re.VERBOSE)                ## schwarzer titel + autor 3 kategorien rank 1 - 3



schwarzerre2 = re.compile(r"""                              #SCHWARZER TITEL + AUTOR § KATEGORIEN RANK 4 - 10

(<h3>(<b>)?(<strong>)?)
(.+)
(:\s)
(.+)
((</b>)?<br\s/>)

""", re.VERBOSE)


#FUNKTION FÜR BUECHERAT BELL - GET AND APPEND
def buecherBell(URL):
    BuecheratnamesBell.clear()
    buecherat = requests.get(URL)

    m = buecheratRE.findall(buecherat.text)

    for tupl in m:                  #m = m.group()
        if "&#8211;" in tupl[4]:
            tuplx = tupl[4].replace("&#8211;", "-")
            BuecheratrankBell.append(int(tupl[0]))
            BuecheratnamesBell.append(tupl[2])
            BuecherattitleBell.append(tuplx)
        else:
            BuecheratrankBell.append(int(tupl[0]))
            BuecheratnamesBell.append(tupl[2])
            BuecherattitleBell.append(tupl[4])
            continue

    # STRING SYNTAX FÜR BUECHERAT BELL - TAKES NAMES AND FLIPPS THEM WITH ",", WORK ON MORE NAMES AND SINGLE NAMES "UBUNTU"
    for name in BuecheratnamesBell:
        name = name.split(",")

        s = ""
        for valuea in name:
            valuea = valuea.lstrip()
            f = valuea.split()
            if " " not in valuea:
                s = s + str(f[-1] + "; ")
            else:
                s = s + str(f[-1] + ", " + " ".join(f[0:-1]) + "; ")

        s = s[0:-2]
        BuecheratnamesBell2.append(s)


#FUNKTION FÜR BUECHERAT SACH - GET AND APPEND
def buecherSach(URL):
    BuecheratnamesSach.clear()
    buecherat = requests.get(URL)

    m = buecheratRE.findall(buecherat.text)

    for tupl in m:                 #m = m.group()
        #check if "&#8211;" - weird stuff in the title - if yes - replace it with "-"
        if "&#8211;" in str(tupl[4]):
            tuplx = tupl[4].replace("&#8211;", "-")

            BuecheratnamesSach.append(tupl[2])
            BuecheratrankSach.append(int(tupl[0]))
            BuecherattitleSach.append(tuplx)
        else:
            BuecheratnamesSach.append(tupl[2])
            BuecheratrankSach.append(int(tupl[0]))
            BuecherattitleSach.append(tupl[4])
            continue


    # STRING SYNTAX FÜR BUECHERAT SACH - TAKES NAMES AND FLIPPS THEM WITH ",", WORK ON MORE NAMES AND SINGLE NAMES "UBUNTU"
    for name in BuecheratnamesSach:  # formatting names syntax
        name = name.split(",")

        s = ""
        for valuea in name:
            valuea = valuea.lstrip()
            f = valuea.split()
            if " " not in valuea:
                s = s + str(f[-1] + "; ")
            else:
                s = s + str(f[-1] + ", " + " ".join(f[0:-1]) + "; ")

        s = s[0:-2]
        BuecheratnamesSach2.append(s)




#FUNKTION FÜR SPIEGEL:DE - GET AND APPEND ************* RANK JUST APPEND NUMBERS FROM 1-10, gets 10 names/titles anyway
def SpiegelSach(URL):                                                                       # Spiegel def
    Spiegelde = requests.get(URL)

    n = Spiegelnamesre.findall(Spiegelde.text)
    print(n)
    for tupl in n[0:10]:  # m = m.group()
        SpiegelnamesSach.append(tupl[1])

    t = Spiegeltitlere.findall(Spiegelde.text)
    for tupl in t[0:10]:  # m = m.group()
        SpiegeltitleSach.append(tupl[1])

    for i in range(1,11):
        SpiegelrankSach.append(i)

#FUNKTION FÜR SPIEGEL:DE - GET AND APPEND********* RANK JUST APPEND NUMBERS FROM 1-10, gets 10 names/titles anyway
def SpiegelBell(URL):                                                                       # Spiegel def
    Spiegelde = requests.get(URL)

    n = Spiegelnamesre.findall(Spiegelde.text)
    print(n)
    for tupl in n[0:10]:  # m = m.group()
        SpiegelnamesBell.append(tupl[1])

    t = Spiegeltitlere.findall(Spiegelde.text)
    for tupl in t[0:10]:  # m = m.group()
        SpiegeltitleBell.append(tupl[1])

    for i in range(1,11):
        SpiegelrankBell.append(i)



#FUNKTION FÜR SPIEGEL:DE - GET AND APPEND ************* RANK JUST APPEND NUMBERS FROM 1-10, gets 10 names/titles anyway

def schwarzer(URL):                                         #FIND AND APPEND / TITLE / NAME / RANK TO LIST
    buecherat = requests.get(URL)

    m = schwarzerre.findall(buecherat.text)                 # RE GET rank 1-3
    for tupl in m[0:9]:                  #m = m.group()
        if "</b>" in tupl[3]:
            tuplx = tupl[3].replace("</b>", "")             #CHECK TITLE FOR WEIRD SYNTAX </b> AND REMOVES
            Schwarzernames.append(tupl[1])
            Schwarzertitle.append(tuplx)
        else:
            Schwarzernames.append(tupl[1])
            Schwarzertitle.append(tupl[3])
            continue

    for i in range(3):
        for i in range(1,4):
            Schwarzerrank.append(i)

    m = schwarzerre2.findall(buecherat.text)                    #rank 4-10
    for tupl in m[0:21]:  # m = m.group()
        if "</b>" in tupl[5]:
            tuplx = tupl[5].replace("</b>", "")                 #CHECK TITLE FOR WEIRD SYNTAX </b> AND REMOVES
            Schwarzernames.append(tupl[3])
            Schwarzertitle.append(tuplx)
        else:
            Schwarzernames.append(tupl[3])
            Schwarzertitle.append(tupl[5])
            continue
    for i in range(7):
        for i in range(4,11):
            Schwarzerrank.append(i)



        # STRING SYNTAX FÜR SCHWARZER BELL + SACH - TAKES NAMES AND FLIPPS THEM WITH ",", WORK ON MORE NAMES AND SINGLE NAMES "UBUNTU"
        for name in Schwarzernames:
            name = name.split(",")

            s = ""
            for valuea in name:
                valuea = valuea.lstrip()
                f = valuea.split()
                if " " not in valuea:
                    s = s + str(f[-1] + "; ")
                else:
                    s = s + str(f[-1] + ", " + " ".join(f[0:-1]) + "; ")

            s = s[0:-2]
            Schwarzernames2.append(s)





#******************************************BUECHERATLINKS***************************************************************
buecherBell("https://www.buecher.at/bestseller-belletristik/")
buecherSach("https://www.buecher.at/bestseller-sachbuch/")
buecherSach("https://www.buecher.at/bestseller-ratgeber/")
buecherBell("https://www.buecher.at/bestseller-belletristik-tb/")
buecherSach("https://www.buecher.at/bestseller-sachbuch-tb/")



#******************************************SPIEGELLINKS***************************************************************
SpiegelSach("https://www.spiegel.de/kultur/literatur/spiegel-bestseller-hardcover-a-1025428.html")
SpiegelSach("https://www.spiegel.de/kultur/literatur/bestseller-paperback-sachbuch-a-dd0efe3f-eaf1-47f7-b5a4-f5cdf0a6da3a")
SpiegelSach("https://www.spiegel.de/kultur/literatur/bestseller-taschenbuch-sachbuch-a-4ce7bbd7-b8a5-41f6-ba72-f1e95cd06fe3")
SpiegelSach("https://www.spiegel.de/kultur/literatur/spiegel-bestseller-ratgeber-leben-gesundheit-essen-trinken-a-1253537.html")
SpiegelSach("https://www.spiegel.de/kultur/literatur/bestseller-ratgeber-essen-trinken-a-64e8b7ac-612b-406b-8654-93ac329560ba")
SpiegelSach("https://www.spiegel.de/kultur/literatur/spiegel-bestseller-ratgeber-natur-garten-hobby-kreativitaet-a-1253538.html")
SpiegelSach("https://www.spiegel.de/kultur/literatur/bestseller-ratgeber-hobby-kreativitaet-a-b6b7aebf-8dd0-47b9-8d49-ad8c502092a4")


SpiegelBell("https://www.spiegel.de/kultur/bestseller-buecher-belletristik-sachbuch-auf-spiegel-liste-a-458623.html")
SpiegelBell("https://www.spiegel.de/kultur/literatur/spiegel-bestseller-paperback-a-1025444.html")
SpiegelBell("https://www.spiegel.de/kultur/literatur/spiegel-bestseller-taschenbuecher-a-1025518.html")

#******************************************SCHWARZERLINK***************************************************************
schwarzer("https://www.schwarzer.at/bestseller/")




# SORT Sach adn Bell into INTO BELL - LIST TILL NOW GOES 123,123,123,45678910.... now it goes 12345678910 NICE!
SchwarzernamesBell.append(Schwarzernames2[0:3] + Schwarzernames2[9:16] + Schwarzernames2[6:9] + Schwarzernames2[23:30])
SchwarzertitleBell.append(Schwarzertitle[0:3] + Schwarzertitle[9:16] + Schwarzertitle[6:9] + Schwarzertitle[23:30])
SchwarzerrankBell.append(Schwarzerrank[0:3] + Schwarzerrank[9:16] + Schwarzerrank[6:9] + Schwarzerrank[23:30])

#append list to list makes list of lists - so just take the 0 element for correct list not lists of list of list of list
SchwarzernamesBell = SchwarzernamesBell[0]
SchwarzertitleBell = SchwarzertitleBell[0]
SchwarzerrankBell = SchwarzerrankBell[0]

# SORT Sach adn Bell into INTO SACH - LIST TILL NOW GOES 123,123,123,45678910.... now it goes 12345678910 NICE!
SchwarzernamesSach.append(Schwarzernames2[3:6] + Schwarzernames2[16:23])
SchwarzertitleSach.append(Schwarzertitle[3:6] + Schwarzertitle[16:23])
SchwarzerrankSach.append(Schwarzerrank[3:6] + Schwarzerrank[16:23])
# append list to list makes list of lists - so just take the 0 element for correct list not lists of list of list of list
SchwarzernamesSach = SchwarzernamesSach[0]
SchwarzertitleSach = SchwarzertitleSach[0]
SchwarzerrankSach = SchwarzerrankSach[0]






#**********************************LOAD EXCEL DATEI AND DEFINE SHEET******************************************************
workbook = openpyxl.load_workbook("Bestsellerxxx.xlsx")
sheetBell = workbook["Bell"]
sheetSach = workbook["Sach"]
print(workbook.sheetnames)




#+++++++++++++++++++++++++++++++++++++++++++BUECHERAT APPEND IN EXCEL+++++++++++++++++++++++++++++++++++++++++++++++++++
pprint.pprint(BuecheratnamesBell2)
pprint.pprint(BuecheratnamesSach2)

# BUECHERAT APPEND TO EXCEL BELL
for i in range(1,21):

    for x in range(1, 201):
        if sheetBell.cell(row=x, column=2).value == BuecherattitleBell[int(i) - 1]:
            sheetBell.cell(row=x, column=3).value = BuecheratrankBell[int(i) - 1]
            break

        elif sheetBell.cell(row=x, column=2).value == None:
            sheetBell.cell(row=x, column=1).value = BuecheratnamesBell2[int(i) - 1]
            sheetBell.cell(row=x, column=2).value = BuecherattitleBell[int(i) - 1]
            sheetBell.cell(row=x, column=3).value = BuecheratrankBell[int(i) - 1]

            break


# BUECHERAT APPEND TO EXCEL SACH
for i in range(1,31):

    for x in range(1, 201):
        if sheetSach.cell(row=x, column=2).value == BuecherattitleSach[int(i) - 1]:
            sheetSach.cell(row=x, column=3).value = BuecheratrankSach[int(i) - 1]
            break

        elif sheetSach.cell(row=x, column=2).value == None:
            sheetSach.cell(row=x, column=1).value = BuecheratnamesSach2[int(i) - 1]
            sheetSach.cell(row=x, column=2).value = BuecherattitleSach[int(i) - 1]
            sheetSach.cell(row=x, column=3).value = BuecheratrankSach[int(i) - 1]

            break




## ++++++++++++++++++++++++++++++++++++++++SPIEGELDE APPEND IN EXCEL++++++++++++++++++++++++++++++++++++++++++++++++++++

# SPIEGEL ADD TO EXCEL Sach
for i in range(1,71):

    for x in range(1, 201):
        if sheetSach.cell(row=x, column=2).value == SpiegeltitleSach[int(i) - 1]:
            sheetSach.cell(row=x, column=4).value = SpiegelrankSach[int(i) - 1]
            break

        elif sheetSach.cell(row=x, column=2).value == None:
            sheetSach.cell(row=x, column=1).value = SpiegelnamesSach[int(i) - 1]
            sheetSach.cell(row=x, column=2).value = SpiegeltitleSach[int(i) - 1]
            sheetSach.cell(row=x, column=4).value = SpiegelrankSach[int(i) - 1]

            break


# SPIEGEL ADD TO EXCEL BELL
for i in range(1,31):

    for x in range(1, 201):
        if sheetBell.cell(row=x, column=2).value == SpiegeltitleBell[int(i) - 1]:
            sheetBell.cell(row=x, column=4).value = SpiegelrankBell[int(i) - 1]
            break

        elif sheetBell.cell(row=x, column=2).value == None:
            sheetBell.cell(row=x, column=1).value = SpiegelnamesBell[int(i) - 1]
            sheetBell.cell(row=x, column=2).value = SpiegeltitleBell[int(i) - 1]
            sheetBell.cell(row=x, column=4).value = SpiegelrankBell[int(i) - 1]

            break






#+++++++++++++++++++++++++++++++++++++++++++++++++++++++SCHWARZER EXCEL++++++++++++++++++++++++++++++++++++++++++++++++

#ITERATE THROUGH SHEET BELL CHECK IF TITLE ALLREADY EXISTS IN COL 2 - IF YES ONLY CHANGE RANK - IF NOT GO ON TILL NONE IN COLUMN X AND ADD TITLE NAME AND RANK
for i in range(1,21):
    for x in range(1, 201):
        if sheetBell.cell(row=x, column=2).value == SchwarzertitleBell[int(i) - 1]:

            sheetBell.cell(row=x, column=5).value = SchwarzerrankBell[int(i) - 1]
            break
        elif sheetBell.cell(row=x, column=2).value == None:
            sheetBell.cell(row=x, column=1).value = SchwarzernamesBell[int(i) - 1]
            sheetBell.cell(row=x, column=2).value = SchwarzertitleBell[int(i) - 1]
            sheetBell.cell(row=x, column=5).value = SchwarzerrankBell[int(i) - 1]

            break


#ITERATE THROUGH SHEET SACH CHECK IF TITLE ALLREADY EXISTS IN COL 2 - IF YES ONLY CHANGE RANK - IF NOT GO ON TILL NONE IN COLUMN X AND ADD TITLE NAME AND RANK
for i in range(1,11):
    for x in range(1, 201):
        if sheetSach.cell(row=x, column=2).value == SchwarzertitleSach[int(i) - 1]:
            sheetSach.cell(row=x, column=5).value = SchwarzerrankSach[int(i) - 1]
            break
        elif sheetSach.cell(row=x, column=2).value == None:
            sheetSach.cell(row=x, column=1).value = SchwarzernamesSach[int(i) - 1]
            sheetSach.cell(row=x, column=2).value = SchwarzertitleSach[int(i) - 1]
            sheetSach.cell(row=x, column=5).value = SchwarzerrankSach[int(i) - 1]

            break







#+++++++++++++++++++++++++++++++++++++++++++++++END OF PROGRAMM SAVE WORKBOOK******************************************
workbook.save("Bestsellerxxx.xlsx")


print("u did it")
