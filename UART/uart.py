import random

alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

n = 2
wort = input("Wort:d")
print(wort)
verschoben = str()

def verschiebung(buch):
    def Eingabe_prufen():
        if buch in alphabet:
            return alphabet.index(buch)
        else:
            print("Eingabe nicht richtig")

    index = Eingabe_prufen()

    def verschieben(i): 
        neu = i + n
        while neu > len(alphabet)-1:
            neu = neu -len(alphabet)
        return neu
    
    def anzeigen(neuu):
        print(alphabet[neuu])
        global verschoben 
        verschoben = verschoben.__add__(alphabet[neuu])
        
    anzeigen(verschieben(index))

for i in range (len(wort)):
    verschiebung(wort[i])