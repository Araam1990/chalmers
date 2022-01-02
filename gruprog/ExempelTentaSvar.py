"""
Denna exempeltenta är uppdelad i två delar, A och B.

För att nå godkänt betyg (3) på tentan krävs 24 poäng, av 32 möjliga, på del A.
Poängen på del B spelar ingen roll om du inte når dessa 24 poäng på del A.

För högre betyg än 3 avgörs betyget av summan på del A och del B; för betyg 4
krävs sammanlagt minst 36 poäng, och för betyg 5 krävs sammanlagt minst 48
poäng av 60 möjliga totalt.
"""

from typing import List


# ------- DEL A ------- #
""" Uppgift A1: 3p
Förklara med egna ord: Vad är skillnaden mellan en for- och while-loop?
Ge också exempel eller generell tumregel för när de olika kan användas.
"""
"""
Den främsta skillnaden är att en for-loop gör något för alla element i en
sekvens - dvs ett finit antal gånger, en gång per element - medan en while-loop
gör något medan ett visst kriterium är uppfyllt - dvs ett obestämt antal 
gånger, tills någonting inträffar som ändrar kontexten på ett visst sätt.

Tumregeln är alltså att använda for-loop för ett förbestämt (max-)antal
iterationer, och en while-loop om antalet iterationer i förväg är okänt.
"""

def uppgiftA2():
    """
    Uppgift A2: 4p
    Förklara noggrant steg för steg hur variabeln x får det värde som skrivs
    ut, och vilket värde.
    """
    x = 0
    for a in range(3):
        for b in range(3):
            x += 1
            if b == 1:
                break
    print(x)

    """
    x initieras till värdet 0. Därefter inkrementeras den n antal gånger, och
    får således slutvärdet n, där n alltså är antalet inkrementeringar. För att
    veta värdet på n behöver vi alltså veta hur många gånger raden x += 1
    exekveras. Den yttre for-loopen körs 3 gånger, för a = 0, 1, 2 respektive.
    För varje iteration av den yttre loopen körs den inre loopen först för
    b = 0, därefter för b = 1, men aldrig för b = 2 eftersom den inre loopen
    avbryts av break när b = 1. Den inre loopen körs alltså två gånger per
    iteration av den yttre, vilket ger oss att n = 3*2 = 6.
    Slutsats: x slutvärde är 6
    """
print("Uppgift A2:")
uppgiftA2()
print()

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

"""
Se filen uppgiftA3-svar.png
"""

""" Uppgift A4: 6p
Presentera en algoritm för en funktion as_set(in_list) som returnerar en ny
lista, där alla element i in_list finns i resultatlistan, men utan att något
element duplicerats (dvs gör om listan till en "mängd"). 

Presentera ditt svar som ett flödesschema, eller som pseudo-kod ("kodskiss"),
eller som faktisk kod i valfritt (känt) programmeringsspråk.
"""
def as_set(in_list):
    result_list = []
    for elem in in_list:
        if elem not in result_list:
            result_list.append(elem)
    return result_list

"""
eller något i stil med:

* Skapa en tom lista för att hålla resultaten
* Start av loop
* Finns fler element i in_list?
* Ja: 
  * Ta nästa element ur in_list 
  * Finns elementet i resultatlistan?
  * Ja: ---
  * Nej: Lägg till elementet i resultatlistan
  * Hoppa till start av loop
* Nej: Returnera resultatlistan
"""
def uppgiftA4():
    print(as_set([1,1,2,2,3,3,3,3,3,4,7,7,1,3,3,5,1,1,4,6]))

print("Uppgift A4:")
uppgiftA4()
print()

""" Uppgift A5: 4p
Förklara begreppet funktionell nedbrytning. Beskriv varför och när vi vill göra
funktionell nedbrytning, och vad vi vill uppnå. Ge ett konkret exempel.
"""
"""
Funktionell nedbrytning är en form av refaktorisering, där vi förändrar koden
utan att förändra dess funktion, för att åstadkomma bättre kodstruktur. Det
innebär att bryta ut delsteg ur en funktion, och namnge dessa som egna, mindre
funktioner. Syftet är att förenkla och förbättra läsbarheten hos varje enskild
funktion: dels genom att varje steg har ett relevant och lättförståeligt namn;
och dels genom att varje funktion/metod består av färre delsteg, och således
lägre komplexitet.
"""

""" Uppgift A6: 5p
Förklara begreppet gränssnitt, och hur vi bör förhålla oss till dessa.
"""
"""
Gränssnittet till en modul/klass/objekt är den funktionalitet som syns för
klienter utifrån. Det består av de publikt exponerade metoder och attribut som
tillhandahålls av modulen/klassen/objektet, inklusive deras signaturer och
publik dokumentation. Vi kontrasterar detta med begreppet implementation,
som är den faktiska kod som utför det som gränssnittet utlovar. Vi kan säga att
gränssnittet berättar *vad* en modul/klass/objekt kan göra, medan
implementationen är *hur* den gör det.

När vi implementerar en modul/klass bör vi exponera så lite som möjligt av
implementationen, och göra dess gränssnitt tydligt och väl genomtänkt.

När vi implementerar en klient bör vi kunna förlita oss på att gränssnittet gör
det det säger att det ska göra, utan att behöva förstå och sätta oss in i
implementationen.

Ett talande exempel är en uttagsautomat. Vi ser dess publika funktioner för
uttag, kontoutdrag, kanske insättning, mm. Vi vet vad var och en av dessa gör,
men behöver inte fundera över hur den är implementerad under ytan.
"""

""" Uppgift A7: 4p
Förklara begreppen supertyp och subtyp, och hur de påverkar varandra.
"""
"""
Supertyper och subtyper är begrepp som hör ihop med mekanismen arv. En klass
A kan deklareras vara en subklass till en annan klass B, vilket innebär att
den ärver samtliga metoder och attribut från B (både gränssnitt och
implementation), men kan göra override för att tillhandahålla egen
implementation av metoder. Eftersom A har (minst) samma gränssnitt som B
är A en subtyp till B - den kan användas i alla sammanhang där B kan användas -
och till alla supertyper till B.

B i sin tur påverkas inte alls av att ha en (eller många) subtyp(er), den vet
inte om att/ifall dessa existerar.
"""


# Max poäng del A: 32p
# Krav för godkänt betyg: 24p


# ------- DEL B ------- #


def uppgiftB1():
    """ Uppgift B1: 6p
    Förklara noggrant vad som skrivs ut och varför det skrivs ut som det
    gör när följande kod körs:
    """
    _z = Z("Run 1")
    _z = Z("Run 2")

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

print("Uppgift B1")
uppgiftB1()
print()

"""
-- Utskriften blir:

Static in Y
Static in Z
Instance in Z
Z is done - Run 1
Instance in Z
Z is done - Run 2

-- Förklaring: 
Koden exekveras uppifrån och ner, enligt följande:
* Först skapas funktionen uppgiftB1 (men exekveras inte). 
* Därefter skapas klassen X, dvs dess klassobjekt skapas på heapen. Ingenting
  skrivs ut i samband med detta.
* Därefter skapas klassen Y, dvs dess klassobjekt skapas på heapen. I och med
  att detta skapas initieras dess klassattribut, vilket leder till att koden
  X("Static in Y") exekveras; denna konstruktor skriver ut rad 1.
* Därefter samma sak för klassen Z: koden X("Static in Z") exekveras när
  klassobjektet skapas. och skriver ut rad 2.
* Därefter anropas funktionen uppgiftB1(), vilken då exekveras. 
  * Det första som händer är ett anrop till Z("Run 1"), vilket leder till att
    Z-klassens __init__-metod exekveras. Denna exekverar först koden 
    X("Instance in Z"), vilket leder till rad 3; därefter skapar den en instans
    från klass Y, vilket inte ger några utskrifter, dess konstruktor är tom.
    Slutligen skriver den ut rad 4.
  * Samma uppsättning kommandon exekveras sen med start i Z("Run 2"), vilket
    leder till rad 5 respektive rad 6.
"""

""" Uppgift B2: 4p
Förklara vad som menas med att listor har referens-semantik, medan tupler har
värde-semantik.
"""
"""
Listor är muterbara objekt. Skickar vi en lista som argument till en metod, är
det ett referensvärde som skickas. Listan kan förändras, element kan läggas
till och tas bort, och alla som har en referens (alias) till list-objektet
kommer att bli varse samma förändringar. Vill vi undvika detta måste vi
istället skicka en kopia av listan som argument.

Tupler är också objekt, men eftersom de är icke-muterbara fungerar de i
praktiken som värden. Det gör ingen skillnad om vi skickar en tupel direkt
eller om vi skickar en exakt kopia av tupeln, resultatet av metoden kommer vara
detsamma i båda fallen.
"""

""" Uppgift B3: 6p
Förklara vad en klass - dvs det vi deklarerar med hjälp av keyword class - är.
Beskriv samtliga aspekter av en klass, och ge exempel på hur vi kan använda oss
av dem.
"""
"""
När vi deklarerar en klass C åstadkommer vi många saker på en och samma gång.
1. Vi deklarerar en *typ* C, för instanser av klassen.
2. Vi definierar ett *klassobjekt*, med namn C och typen 'type', och anger dess
   implementation genom klassmetoder (statiska metoder) och klassattribut.
3. Vi ger en implementation av hur *instanser* av klassen uppfyller typen C
   (och supertyper till C), genom instansmetoder och instansattribut.
4. Vi beskriver, genom implementation av en *konstruktor*, hur instanser av
   klassen C skapas och initieras av klassobjektet C.

Att punkt 1 och 3 är separata kan vi se t ex genom att abstrakta metoder ingår
i 1, men inte i 3. Vi kan också se det genom att subtyper till C kan ge en
alternativ implementation (3), men inte ändra typen (2).

Punkt 1 kommer alltid vara en del av en klassdeklaration; det finns inget sätt
att undvika att skapa en typ.
Punkt 2 kommer också alltid vara en del, vi skapar alltid ett klassobjekt,
oavsett om detta klassobjekt (från början - Python låter oss lägga till
attribut och metoder dynamiskt!) har någon egen funktionalitet.
Punkt 3 kan utgå, helt eller delvis, om klassen C är abstrakt.
Punkt 4 kan utgå, om det inte ska vara möjligt att skapa instanser av klassen. 
"""

""" Uppgift B4: 6p
Förklara Principle of Least Astonishment, och vad den säger om hur vi bör
förhålla oss till funktioner, metoder, och deras argument.
"""
"""
PoLA säger i grunden att vi bör implementera funktioner på ett sätt som leder
till minsta möjliga förvirring. Konkret finns en uppsättning tumregler för vad
som kan betraktas som förvirrande och inte:
* Metoder ska namnges på ett sätt som tydligt visar vad de åstadkommer.
* Metoder bör inte både utföra en effekt (command) och returnera ett värde
  (query) - detta kallas Command-Query-Separation-Principle.
* Metoder bör inte uppdatera sina explicita argument - dvs de bör vara
  implementerade med Pass-By-Value-semantik.
* Metoder får uppdatera sitt implicita argument (som har Pass-By-Reference-
  semantik per default).
* Metoder och funktioner som bryter mot någon av punkterna 2 eller 3 måste
  dokumenteras extra väl, så att det blir väldigt tydligt varför och hur den
  bryter emot dem. 
"""

"""Uppgift B5: 6p
Presentera en algoritm för en funktion 

all_positive_submatrices(the_matrix: List[List[int]], size: int) 

som hittar och returnerar alla sub-matriser av storlek size*size,
vars sammanlagda värde på elementen i sub-matrisen är >0. 

Presentera ditt svar som ett eller flera flödesscheman, som pseudo-kod
("kodskiss"), eller som faktisk kod i valfritt (känt) programmeringsspråk.

Exempel på körning:
m1 = [[-1,-2,-3],
      [-3,-5, 6],
      [7, 8, 9]]
m2 = [[-1, -2, -3, -4],
      [ 5, 6, -7, -8],
      [-9, 10, -11, -12],
      [-13, 14, 15, -16]]

all_positive_submatrices(m1, 2)
[[[-3, -5],[7, 8]], [[-5, 6], [8, 9]]]

all_positive_submatrices(m2, 3)
[[[5, 6, -7], [-9, 10, -11], [-13, 14, 15]]] 

all_positive_submatrices(m1, 4)
[]

"""

# Detta är topp-nivå-funktionen. Missar ni steg ett, dvs validering av
# argumenten, kan det bli lurigt senare, och leda till avdrag.
def all_positive_submatrices(the_matrix: List[List[int]], size: int):
    validate_arguments(size, the_matrix)
    return add_all_positive(the_matrix, size)


# Denna metod är den viktigaste att få till rätt, och beskriva i kod eller
# pseudo-kod. Jag kan acceptera att ni är vaga med detaljerna av de olika
# hjälp-funktionerna (determine_nr_of_subs, get_sub_matrix, add_if_positive).
def add_all_positive(the_matrix, size):
    nr_subs_height, nr_subs_width = determine_nr_of_subs(the_matrix, size)
    result = []
    for i in range(nr_subs_height):
        for j in range(nr_subs_width):
            sub_matrix = get_sub_matrix(the_matrix, i, j, size)
            add_if_positive(result, sub_matrix)
    return result


# Alternativ implementation: Denna plus find_all_subs (eller
# find_all_subs_lazy) är ett alternativt sätt att implementera algoritmen. Jag
# accepterar båda svaren.
def add_all_positive_alternate(the_matrix, size):
    result = []
    for sub_matrix in find_all_subs_lazy(the_matrix, size):
        add_if_positive(result, sub_matrix)
    return result


def find_all_subs(the_matrix, size):
    nr_subs_height, nr_subs_width = determine_nr_of_subs(the_matrix, size)
    all_subs = []
    for i in range(nr_subs_height):
        for j in range(nr_subs_width):
            all_subs.append(get_sub_matrix(the_matrix, i, j, size))
    return all_subs


def find_all_subs_lazy(the_matrix, size):
    nr_subs_height, nr_subs_width = determine_nr_of_subs(the_matrix, size)
    for i in range(nr_subs_height):
        for j in range(nr_subs_width):
            yield get_sub_matrix(the_matrix, i, j, size)


def add_if_positive(result, sub_matrix):
    if sum_matrix(sub_matrix) > 0:
        result.append(sub_matrix)


# ---- Matrix helper functions ----
# Det är helt okej att vara vag med beskrivningarna av dessa
def determine_nr_of_subs(the_matrix, size):
    height, width = get_height_and_width(the_matrix)
    nr_subs_height = max(0, height - size + 1)  # if size is larger than height or width,
    nr_subs_width  = max(0, width  - size + 1)  # the task will be impossible
    return nr_subs_height, nr_subs_width


def get_sub_matrix(the_matrix, start_row, start_col, size):
    return [row[start_col:start_col + size]
            for row in the_matrix[start_row:start_row + size]]


def sum_matrix(matrix_to_sum):
    return sum(map(sum, matrix_to_sum))


def get_height_and_width(the_matrix):
    height = len(the_matrix)
    width = 0 if height == 0 else len(the_matrix[0])
    return height, width


# ---- Validating arguments ----
# Utelämnar ni denna biten, utan annan felhantering eller kommentar, drar jag
# av något poäng.
def validate_arguments(size, the_matrix):
    validate_size_argument(size)
    validate_matrix_argument(the_matrix)


def validate_size_argument(size):
    if size <= 0:
        raise ValueError("all_positive_submatrices: size must be positive: " + str(size))


def validate_matrix_argument(the_matrix):
    if not all_rows_have_same_size(the_matrix):
        raise ValueError("all_positive_submatrices: the_matrix must be a proper NxM matrix")


def all_rows_have_same_size(the_matrix):
    for row in the_matrix:
        if len(the_matrix[0]) != len(row):
            return False
    return True


# ---- Testa implementationen ----
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

if __name__ == "__main__":
    pass  # De olika delarna anropas inline på toppnivå
