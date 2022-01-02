"""
Denna exempeltenta är uppdelad i två delar, A och B.

För att nå godkänt betyg (3) på tentan krävs 24 poäng, av 32 möjliga, på del A.
Poängen på del B spelar ingen roll om du inte når dessa 24 poäng på del A.

För högre betyg än 3 avgörs betyget av summan på del A och del B; för betyg 4krävs sammanlagt minst 36 poäng, och för betyg 5 krävs sammanlagt minst 48poäng av 60 möjliga totalt.
"""

# ------- DEL A ------- #

""" Uppgift A1: 3p
Förklara med egna ord: Vad är skillnaden mellan en for- och while-loop?
Ge också exempel eller generell tumregel för när de olika kan användas.
"""

""" Svar uppgift A1:
En for-loop är som en specifikt variant av while-loopen. 

for x in range(10):
    print(x)

Ovannämnda loop skulle kunna skrivas som en while-loop genom att modifiera den lite.

x = 0
while x < 10:
    print(x)
    x += 1

En generell tumregel är att när man vet antalet iterationer, t.ex. när man itererar över en lista, så använder man en for-loop medan när man inte vet antalet iterationer som krävs för att uppfylla vilkoret så används en while-loop
"""

def uppgiftA2():
    """
    Uppgift A2: 4p
    Förklara noggrant steg för steg hur variabeln x får det värde som skrivs ut, och vilket värde.
    """
    x = 0
    for a in range(3):
        for b in range(3):
            x += 1
            if b == 1:
                break
    print(x)

""" Svar uppgift A2:
Först tilldelar vi variabeln a värdet 0.
Sedan itererar vi över range(3) vilket motsvarar följande [0,1,2] så a kommer gå från 0 till 1 till 2.
Samma sak händer på raden under fast variabeln är b istället.
På raden under inkrementerar vi x med 1, x += 1 är samma sak som x = x + 1.
Sedan på raden under kollar vi om b är 1 och om det är sant så körs en break vilket kommer avbryta den närmsta loopen vilket i detta fallet är for-loopen med b som variabel. Detta betyder att den loopen egentligen endast itererar över [0,1], den når alltså inte sista värdet i listan då den avbryts tidigare.
Allt detta innebär att x += 1 kommer köras 3*2 gånger, (antalet iterationer på första loopen) * (antalet iterationer på andra loopen), och x kommer därför få värdet 6 när den väl printas ut.
"""

def uppgiftA3():
    """ Uppgift A3: 6p
    Rita en bild som visar variabler, värden, referenser och objekt samt hur dessa
    förhåller sig till varann före anropet av metoden do_it(), och vad som ändras
    av anropet.
    """
    a = A(1)  # Before
    do_it(a)  # The call
    print(a)  # After

def do_it(a):
    a.b.x[a.i] = 7

class A:
    def __init__(self, i):
        self.i = i
        self.b = B(2)

class B:
    def __init__(self, length):
        self.x = [0] * length

""" Svar uppgift A3:
Before:
a = {
    i = 1,
    b = {
        x = [0,0]
    }
}
After:
a = {
    i = 1,
    b = {
        x = [0,7]
    }
}
"""

""" Uppgift A4: 6p
Presentera en algoritm för en funktion as_set(in_list) som returnerar en nylista, där alla element i in_list finns i resultatlistan, men utan att något element duplicerats (dvs gör om listan till en "mängd"). 

Presentera ditt svar som ett flödesschema, eller som pseudo-kod ("kodskiss"),eller som faktisk kod i valfritt (känt) programmeringsspråk.
"""

""" Svar uppgift A4: """
def as_set(in_list):
    set_list = []
    for el in in_list:
        if el not in set_list:
            set_list.append(el)
    return set_list

""" Uppgift A5: 4p
Förklara begreppet funktionell nedbrytning. Beskriv varför och när vi vill görafunktionell nedbrytning, och vad vi vill uppnå. Ge ett konkret exempel.
"""

""" Svar uppgift A5:
Begreppet funktionell nedbrytning betyder att vi lyfter ut kodstycken ur funktioner och gör om det till nya funktioner.
Detta vill vi göra för att öka läsligheten samt göra det lättare att maintaina programmet i framtiden. Ett bra exempel på detta är hur vi gjorde i Pig labben. Man skulle kunna ha all logik liggandes i en och samma funktion men programmet blir betydligt mycket tydligare om vi bryter ut delar så att vi har en funktion vars jobb är att initiera spelara, en funktion som hanterar att man kastar tärningen osv. Det leder till att om vi hittar ett fel i t.ex. hur spelarna initieras så behöver vi inte leta efter felet i en stor funktion på några hundra rader utan man kan lätt gå till just den funktionen vars jobb är att initiera spelarna och felsöka den.
"""

""" Uppgift A6: 5p
Förklara begreppet gränssnitt, och hur vi bör förhålla oss till dessa.
"""

""" Svar uppgift A6:
Ett gränssnitt är en specification av hur någonting ansluter till, och interagerar med, saker utanför.
"""

""" Uppgift A7: 4p
Förklara begreppen supertyp och subtyp, och hur de påverkar varandra.
"""

""" Svar uppgift A7:
Supertyp är 
"""
# Max poäng del A: 32p
# Krav för godkänt betyg: 24p

# ------- DEL B ------- #

def uppgiftB1():
    """ Uppgift B1: 6p
    Förklara noggrant vad som skrivs ut och varför det skrivs ut som det
    gör när följande kod körs:
    """
    z = Z("Run 1")
    z = Z("Run 2")

class X:
    def __init__(self, msg):
        print(msg)

class Y:
    x1 = X("Static in Y")

class Z:
    x1 = X("Static in Z")

    def __init__(self, msg):
        self.x2 = X("Instance in Z")
        self.b1 = Y()
        print("Z is done - " + msg)

uppgiftB1()

""" Svar uppgift B1:
När en instans av klassen X skapas så kommer den printa värden den tar in direkt.
Och när man skapar ett statiskt attribut till en klass så kommer den koden köras när allt läses in då den attributen är samma för alla instanser av den klassen.
Det betyder att det första som kommer printas ut är "Static in Y" följt av "Static in Z".
Sedan skapar vi en instans av Z med argumentet "Run 1" vilket kommer skapa en instans av X med argumentet "Instance in Z" som kommer printas, en instans av Y skapas också men då dess attribut är statiskt så skapas inte den på nytt och inget printas där och slutligen kommer print av "Z is done - " + msg och msg är "Run 1" så den kommer printa "Z is done - Run 1".
Sedan skapas ytterliggare en instans av klassen Z med argumentet "Run 2" så samma som ovan kommer printas med en skillnad i "Z is done - Run 2"

Output:
Static in Y
Static in Z
Instance in Z
Z is done - Run 1
Instance in Z
Z is done - Run 2
"""

""" Uppgift B2: 4p
Förklara vad som menas med att listor har referens-semantik, medan tupler har värde-semantik.
"""

""" Svar uppgift B2:

"""

""" Uppgift B3: 6p
Förklara vad en klass - dvs det vi deklarerar med hjälp av keyword class - är.
Beskriv samtliga aspekter av en klass, och ge exempel på hur vi kan använda oss av dem.
"""

""" Svar uppgift B3:

"""

""" Uppgift B4: 6p
Förklara Principle of Least Astonishment, och vad den säger om hur vi börförhålla oss till funktioner, metoder, och deras argument.
"""

""" Svar uppgift B4:

"""

"""Uppgift B5: 6p
Presentera en algoritm för en funktion 
all_positive_submatrices(the_matrix: List[List[int]], size: int) 
som hittar och returnerar alla sub-matriser av storlek size*size,vars sammanlagda värde på elementen i sub-matrisen är >0. 
Presentera ditt svar som ett eller flera flödesscheman, som pseudo-kod("kodskiss"), eller som faktisk kod i valfritt (känt) programmeringsspråk.
Exempel på körning:
m1 = [[-1,-2,-3],
      [-3,-5, 6],
      [7, 8, 9]]
m2 = [[-1, -2, -3, -4],
      [ 5, 6, -7, -8],
      [-9, 10, -11, -12],
      [-13, 14, 15, -16]]

all_positive_submatrices(m1, 2)
[[[3, 5],[7, 8]], [[5, 6], [8, 9]]]

all_positive_submatrices(m2, 3)
[[[5, 6, -7], [-9, 10, -11], [-13, 14, 15]]]

all_positive_submatrices(m1, 4)
[]
"""

""" Svar uppgift B5: """

def all_positive_submatrices(matrix, size):
    try:
        validate_inputs(matrix, size)
        nr_subs_height, nr_subs_width = determine_nr_of_subs(matrix, size)
        valid_subs = []
        for i in range(nr_subs_height):
            for j in range(nr_subs_width):
                sub = get_sub_matrix(matrix, size, i, j)
                if sum_is_positive(sub):
                    valid_subs.append(sub)
        return valid_subs
    except ValueError as ve:
        print(ve)

def determine_nr_of_subs(matrix, size):
    return (len(matrix) - size + 1), (len(matrix[0]) - size + 1)

def get_sub_matrix(matrix, size, start_row, start_col):
    return [row[start_col:start_col + size]
            for row in matrix[start_row:start_row + size]]

def sum_is_positive(matrix):
    sum = 0
    for row in matrix:
        for val in row:
            sum += val
    return sum > 0

def validate_inputs(matrix, size):
    validate_matrix(matrix)
    validate_size(size, (len(matrix), len(matrix[0])))

def validate_matrix(matrix):
    for row in matrix:
        if len(row) != len(matrix[0]):
            raise ValueError("All rows in the matrix must be the same size")

def validate_size(size, matrix_size):
    if size <= 0:
        raise ValueError("Size must be positive")
    elif size > matrix_size[0] or size > matrix_size[1]:
        raise ValueError("Size can not exceed the size of the matrix")

def uppgiftB5():
    m1 = [[-1, -2, -3],
          [-3, -5, 6],
          [7, 8, 9]]
    m2 = [[-1, -2, -3, -4],
          [5, 6, -7, -8],
          [-9, 10, -11, -12],
          [-13, 14, 15, -16]]

    print(all_positive_submatrices(m1, 2))
    # [[[-3, -5], [7, 8]], [[-5, 6], [8, 9]]]

    print(all_positive_submatrices(m2, 3))
    # [[[5, 6, -7], [-9, 10, -11], [-13, 14, 15]]]

    print(all_positive_submatrices(m1, 4))
    # []

print("Uppgift B5:")
uppgiftB5()
print()

# Max poäng del A+B: 60p
# Krav för betyg 4: 36p
# Krav för betyg 5: 48p