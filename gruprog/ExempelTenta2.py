""" Uppgift A1: 5 poäng
	
	Förklara med egna ord: Hur fungerar satserna (statements) break, continue och return.
	Förklara likheter och skillnader mellan dessa tre statements.

	Svar:
	Var?
	- Både break och continue används inom loopar
	- return används inom funktioner/metoder

	Vad?
	- break avslutar den närmsta omlutande loopen
	- continue går vidare till nästa iteration i den närmsta omslutande loopen
	- return avslutar en funktion och returnerar det givna värdet

	Varför/hur?
	- break används när resterande iterationer genom en loop inte längre är nödvändig. Säg att vi har en funktion som vill kolla om en lista är sorterad, då loopar vi över listan och stöter på att element i är större än element i+1 (inte sorterad), då kan vi spara det i en variabel och använda oss av en break för att inte loopa över resterande element i listan då vi redan har resultatet vi är ute efter.
	- continue används när vi är klara med det nuvarande elementet från en loop. Säg att vi loopar över en lista där vi vill utföra en operation/funktion på alla strängar, då skulle vi kunna kolla om elementet inte är en sträng (not isinstance(el, str)) i en if sats och därmed använda continue statement om det uttrycket är sant
	- return används när våran funktion kommit fram till det den ska göra och returnerar detta till där funktionen anropas, kan även denna användas som en break i vissa fall. Ta exemplet från break som exempel, istället för att använda oss av break kan vi direkt i loopen returnera False när vi stöter på ett ställe där element i är större än element i+1 och sedan om vi gick igenom hela loopen utan att stöta på det så kan vi bara returnera True

	Exempel break:
	is_sorted = True
	for i in range(len(list) - 1):
		el_1 = list[i]
		el_2 = list[i+1]
		if el_1 > el_2:
			is_sorted = False
			break
	do_something()

	Exempel continue:
	for el in list:
		if not isinstance(el, str):
			continue
		do_something(el)
		do_something_2(el)
		do_something_3(el)
	

	Exempel return:
	def is_sorted(list):
		for i in range(len(list) - 1):
			el_1 = list[i]
			el_2 = list[i+1]
			if el_1 > el_2:
				return False
		return True
"""

""" Uppgift A2: 4 poäng

	Förklara noggrant steg för steg hur variabeln x får det värde som skrivs ut, och vilket värde.
	Notera att operatorn / motsvarar äkta division, och funktionen int avrundar sitt argument nedåt
	till närmaste heltal.

	x = 0
	try:
	    for i in range(10):
	        x += 1 + int(i / (5 - i))
	except ZeroDivisionError:
	    x += 1
	except Exception:
	    x += 2
	print(x)

	Svar:
	- variabeln x definieras och tilldelas värdet 0, x = 0
	- try blocket exekveras
	- for loopen exekveras
		- i = 0, då int(i / (5 - i)) = int(0/5) = 0 så ökar värdet av x endast med 1 -> x = 1
		- i = 1, då int(i / (5 - i)) = int(1/4) = 0 så ökar värdet av x endast med 1 -> x = 2
		- i = 2, då int(i / (5 - i)) = int(2/3) = 0 så ökar värdet av x endast med 1 -> x = 3
		- i = 3, då int(i / (5 - i)) = int(3/2) = 1 så ökar värdet av x med 2 -> x = 5
		- i = 4, då int(i / (5 - i)) = int(4/1) = 4 så ökar värdet av x med 5 -> x = 10
		- i = 5, då i / (5 - i) = 5/0 så kommer ett exception kastas i och med att division med 0 inte går
	- exception blocket för ZeroDivisionError kommer då utföras och öka värdet av x med 1, x = 11
	- print(x) kommer då skriva ut 11
"""

""" Uppgift A3: 6 poäng

	Rita en bild som visar variabler, värden, referenser och objekt samt hur dessa förhåller sig till
	varandra före anropet av metoden do_it(), och vad som ändras av anropet.

	def uppgiftA3():
	    k = K(3)  # Before
	    do_it(k)  # The call
	    print(k)  # After

	def do_it(x):
	    x.ls.append(L(x))

	class K:
	    def __init__(self, length):
	        l = L(self)
	        self.ls = []
	        for i in range(length):
	            self.ls.append(l)

	class L:
	    def __init__(self, k):
	        self.k = k

	Svar:

	before
			___________
	x = --> | :K      |<----------|
			| ls = [  |    _______|__
			|     a,--|--> | :L   | |
			|     b,--|--> | k = -| |
			|     c---|--> |________|
			| ]       |
			|_________|

	after
			___________
	x = -->	| :K 	  |<----------|
			| ls = [  |    _______|__
			|     a,--|--> | :L   | |
			|     b,--|--> | k = -| |
			|     c,--|--> |________|
			|     d---|-|  __________ 
			| ]       | -->| :L     |
			|_________|    | k = -| |
				^      |______|_|
				|-------------|
"""

"""	Uppgift A4: 6 poäng

	Presentera en algoritm för en funktion differences(in_list) som för en lista av heltal (int) 
	returnerar en ny lista, där varje element i den nya listan motsvarar differensen av två närstående tal 
	i argumentlistan. 

	Exempel på körning: 
	differences([1,2,4,6,7]) 
	[1,2,2,1] 
	 
	differences([1,2,3,4,5]) 
	[1,1,1,1] 
	 
	differences([2,4,2,4]) 
	[2,-2,2,-2] 
	 
	differences([1]) 
	[]

	Presentera ditt svar som ett flödesschema, eller som pseudo-kod ("kodskiss"), eller som faktisk kod i 
	valfritt (känt) programmeringsspråk.

	Svar:
	def differences(in_list):
		if not isinstance(in_list, list):
			raise ArgumentError
		if len(in_list) < 2:
			return []
		diffs = []
		for el_1, el_2 in zip(in_list[:-1], in_list[1:]):
			if not isinstance(el_1, int) or not isinstance(el_2, int):
				raise ArgumentError
			diffs.append(el_2 - el_1)
		return diffs
"""

"""	Uppgift A5: 3 poäng

	Förklara begreppen statement och expression, hur de relaterar till varandra, och vad som skiljer 
	dem åt. 

	Svar:
	- Ett expression är något som representerar ett värde och består av en kombination av värden, variabler samt operatorer. Exempel är 42, True, (7+5*2), "hej" osv.
	- Ett statement är en bit kod som har en effekt utifrån ett eller flera expressions, kan vara att skapa en variabel, skriva ut ett värde, mm
	
	- TL;DR Man kan säga att ett expression översätts till ett värde och statements använder värden för att göra något
"""

"""	Uppgift A6: 4 poäng

	Förklara Principle of Least Astonishment. Ge konkreta exempel på vad den innebär. 

	Svar:
	- Principen innebär att man inte ska bli förvånad över vad något är eller gör. Detta kan bland annat uppnås genom bra namngivning, dokumentation och funktionell nedbrytning.
	- Har vi ett lista som heter numbers så bör den inte innehålla strängar med namn, en funktion bör inte ändra på ett argument såvida det inte framgår tydligt på något sätt, döp inte variabler till en bokstav (vanliga undantag här är x och y som kordinater samt i som index) utan skriv vad de är.
"""

"""	Uppgift A7: 4 poäng 

	Förklara vad en abstrakt klass är, och vad vi vill använda sådana till.

	Svar:
	Vad?
	En abstrakt klass är en klass som vi kan ärva av men inte instansiera.

	Varför?
	Vi vill använda abstrakta klasser för att minska kod duplicering då vi har flera klasser som delar funktionalitet.


	Exempelvis kan följande:
	class Cow:
		def __init__(self, name, age):
			self.name = name
			self.age = age

		def greet(self):
			print(f"Hello! My name is {self.name} and I am {self.age} years old")

		def to_string(self):
			return f"Cow({self.name=}, {self.age=})"

	class snake:
		def __init__(self, name, age, is_venomous):
			self.name = name
			self.age = age
			self.is_venomous = is_venomous

		def greet(self):
			print(f"Hello! My name is {self.name} and I am {self.age} years old")

		def to_string(self):
			return f"snake({self.name=}, {self.age=}, {self.is_venomous})"

	class Horse:
		def __init__(self, name, age, can_ride):
			self.name = name
			self.age = age
			self.can_ride = can_ride

		def greet(self):
			print(f"Hello! My name is {self.name} and I am {self.age} years old")

		def to_string(self):
			return f"Horse({self.name=}, {self.age=}, {self.can_ride=})"

	skrivas om till:

	class Animal(ABC):
		def __init__(self, name, age):
			self.name = name
			self.age = age

		def greet(self):
			print(f"Hello! My name is {self.name} and I am {self.age} years old")
		
		@abstractmethod
		def to_string(self):
			raise NotImplementedError

	class Cow:
		def __init__(self, name, age):
			super().__init(name, age)

		def to_string(self):
			return f"Cow({self.name=}, {self.age=})"

	class snake:
		def __init__(self, name, age, is_venomous):
			super().__init(name, age)
			self.is_venomous = is_venomous

		def to_string(self):
			return f"snake({self.name=}, {self.age=}, {self.is_venomous})"

	class Horse:
		def __init__(self, name, age, can_ride):
			super().__init(name, age)
			self.can_ride = can_ride

		def to_string(self):
			return f"Horse({self.name=}, {self.age=}, {self.can_ride=})"

	En annan fördel med den abstrakta klassen är att vi direkt kan kolla om ett objekt vi får in är av typen Animal istället för att behöva kolla om det är av typen Cow eller Snake eller Horse.
	Vi kan även använda oss av abstrakts metoder i en abstrakt klass vilket visar funktionalitet som är specifik för subklasserna och måste därför implementeras där.
"""

"""	Uppgift B1: 6 poäng

	Förklara noggrant vad som skrivs ut när följande kod körs, och varför:

	def uppgiftB1(): 
	    a = A(1) 
	    x = a 
	    a = B(1) 
	    x.x.x = a 
	    x.i = 5 
	    print(a.x.i) 
	    a.set(10) 
	    print(a.x.x.i) 
	    x.set(20) 
	    print(A.i) 
	    print(B.i) 
	    print(a.i) 
	    print(x.i) 
	 
	class A: 
	    i = 0 
	 
	    @classmethod 
	    def set(cls, i): 
	        cls.i = i 
	 
	    def __init__(self, i): 
	        self.i = i 
	        self.x = self 
	 
	class B(A): 
	    i = 1 
	 
	    def __init__(self, i): 
	        super().__init__(i) 
	 
	    @classmethod 
	    def set(cls, i): 
	        cls.i = 100 – i 
	 
	uppgiftB1()

	Svar:
	Rad 1: variabeln a tilldelas en referens till en instans av klassobjektet A
	Rad 2: variabeln x tilldelas en referens till samma objekt som variabeln a
	Rad 3: variabeln a tilldelas en referens till en instans av klassobjektet B
	Rad 4: då attributen x i klassen A pekar på sig själv så är x.x.x == x.x och vi skriver alltså över attributen x med instansen av klassobjektet B i variabeln a
	Rad 5: skriver över attributen i med värdet 5 på instansen av klassobjektet A i variabeln x
	Rad 6: då a.x == a så skrivs a.i ut vilket är 1
	Rad 7: vi skriver över attributet i på klassobjektet B till 90
	Rad 8: då a.x == a så är även a.x.x == a så skrivs a.i ut vilket är 1
	Rad 9: vi skriver över attributet i på klassobjektet A till 20
	Rad 10: vi skriver ut atteributet i på klassobjektet A vilket är 20
	Rad 11: vi skriver ut atteributet i på klassobjektet A vilket är 90
	Rad 12: vi skriver ut atteributet i på instansen av klassobjektet B i variabeln a som är 1
	Rad 13: vi skriver ut atteributet i på instansen av klassobjektet A i variabeln x som är 5

	output:
	1
	1
	20
	90
	1
	5
"""

"""	Uppgift B2: 6 poäng 

	Förklara begreppet gränssnitt, och hur vi bör förhålla oss. 

	Svar:
	- Gränssnitt är hur ett objekt ser ut utifrån, alltså vilken funktionalitet samt vilka attribut som finns på objektet.
	- 
"""

"""	Uppgift B3: 5 poäng 

	Förklara vad en datastruktur är. Ge exempel på några olika enkla datastrukturer, och vad som bör 
	avgöra vilken datastruktur vi väljer att använda i en specifik situation.

	Svar:
	- Datastrukturer är olika sätt man kan lagra data på som har sina fördelar i olika tillfällen.
	- Exempel på vanliga datastrukturer är list/array, dictionary och set.
	- Det som bör avgöra hur vi väljer datastruktur är hur det känns mest logiskt att representera datan. Säg att vi vill veta vilka unika värden som finns i en lista av integers
		- Vi skulle kunna representera det som en lista genom följande:
		1. 	unique_ints = []
		2. 	for num in in_list:
		3. 		if num not in unique_ints:
		4.			unique_ints.append(num)
		Detta fungerar alldeles utmärkt men kan snabbt ta för lång tid vilket är varför nästa exempel är bättre
		- Vi kan använda oss av en dictionary:
		1. 	unique_ints = {}
		2. 	for num in in_list:
		3. 		if num not in unique_ints:  # Denna if-satsen behövs inte, resultatet blir detsamma, beror på vad man trivs bäst med
		4.			unique_ints[num] = True
		Nu när vi använder oss av en dictionary så slipper man rad 3 i förra exemplet i vilket man itererar igenomn unique_ints listan som kan ta väldigt lång tid om man har en lång lista med många unika siffror
		- Vi kan även representera det som en mängd, ett set:
		unique_ints = set()
		for num in in_list:
			if num not in unique_ints:   # Samma här, denna if-satsen behövs inte, resultatet blir detsamma, beror på vad man trivs bäst med
				unique_ints.add(num)

		eller bara unique_ints = set(in_list)
		Då ett set egentligen bara är en True/False dict så uppnår detta samma resultat som förra exemplet
	Här har vi nu löst problemet med hjälp av 3 olika datastrukturer och vilken man vill använda beror helt på situationen och vad som känns mest logiskt
	- Vi inser nu att vi inte bara ville veta vilka unika nummer som finns i listan utan även räkna hur många av varje vi har
		- Vi skulle fortfarande kunna representera det som listor genom följande:
		1. 	unique_ints = []
		2.	counts = []
		3. 	for num in in_list:
		4. 		i = unique_ints.index(num)
		5. 		if i >= 0:
		6. 			counts[i] += 1
		7.		else:
		8. 			unique_ints.append(num)
		9.			counts.append(1)
		- Vi kan även fortfarande använda oss av en dictionary:
		1. 	unique_ints = {}
		2. 	for num in in_list:
		3. 		if num not in unique_ints:
		4.			unique_ints[num] = 0
		5. 		unique_ints[num] += 1
		- Men vi kan inte representera det som en mängd, ett set, längre då vi inte kan matcha ett värde med annat än True/False
	Tänk bara på att det oftast finns fler än en datastruktur som kan fungera.
"""

"""	Uppgift B4: 5 poäng 

	Förklara hur mekanismerna arv och komposition båda kan hjälpa oss att undvika kodduplicering. 
	Förklara hur respektive mekanism löser problemet, och diskutera för och nackdelar. 

	Svar:
	Arv 
	- innebär att en klass kan ärva funktionalitet och attribut från en annan klass och därmed bli en subtyp respektive supertyp. 
	- Säg att vi har en klass Cat och en klass Animal, här är det mest logiskt att Cat ärver av Animal då Cat är en typ av Animal och Animal delar all funktionalitet med Cat, skulle vi använda komposition så skulle förhållandet bli att Cat har ett Animal (en katt har ett djur) vilket inte är logiskt alls.
	- Fördelen här kommer sen när vi vill implementera fler djur, då kan alla ärva av Animal och få viss grundfunktionalitet som respektive djur sedan kan utöka och göra om på sitt sätt  och vi undviker därmed kodduplicering. Alla djur kan inte flyga så Animal ska inte kunna flyga men fåglar kan så de får implementera det, eller skapa en till klass FlyingAnimal som ärver av Animal och som blir grunden till fåglar osv. 
	- En annan fördel är att vi kan hantera subtyperna som supertypen Animal, säg att vi har en lista med djur som alla ska göra något, då Animal från grunden har en do_something metod så kan vi hantera alla djur i denna listan som Animals:
	for (Animal animal : animals) {
		animal.do_something()
	}
	
	Komposition 
	- innebär att en klass använder ett annat objekt för att förse klassen med viss eller all funktionalitet av objektet. 
	- Säg att vi har en Car och denna bilen har en Engine, då är det mer logiskt att använda komposition så att Car har en attribut engine som är en instans av klassen Engine än att Car ska ärva från Engine då det skulle säga att Car är en typ av Engine.
	- Fördelen här kommer sen när vi implementerar andra typer av fordon, säg en båt eller flygplan, de har ochså motorer så då kan de använda den redan existerande Engine klassen för den funktionaliteten och därmed slipper implementera en helt ny motor i respektive klass och vi undviker därmed kodduplicering.
	- En nackdel här är att vi inte direkt kan hantera alla dessa klasser med motor
	for vehicle with engine in vehicles:
		vehicle.do_something()
	men det här här interfaces kommer in och räddar oss, vi kan göra ett interface Moveable med en attribut engine och funktionalitet för att t.ex. gasa, bromsa och svänga som dessa fordon implementerar, då kan vi göra på följande sätt:
	for (Moveable vehicle : vehicles) {
		vehicle.do_something()
	}

	Så frågan är, HAR klassen ett annat objekt på det sättet som en bil HAR en motor eller ÄR klassen ett annat objekt på det sätt som att en katt ÄR ett djur?
"""

"""	Uppgift B5: 6 poäng 

	Presentera en algoritm för en funktion longest_increasing_sublist(in_list) som, 
	givet ett argument som är en lista, returnerar den längsta delsekvensen i argumentlistan som är 
	monotont ökande, dvs där varje element i sekvensen är större än föregående element. 

	Exempel på körning: 
	longest_increasing_sublist([3,2,3,4,5,4,5,6]) 
	[2,3,4,5] 
	 
	longest_increasing_sublist([1,2,2,1,2]) 
	[1,2] 
	 
	longest_increasing_sublist([1,1,1,1,1) 
	[1]

	Svar:
	def longest_increasing_sublist(in_list):
		if len(in_list) == 0:
			return []
		longest_sublist = []
		cur_sublist = [in_list[0]]
		for el in in_list[1:]:
			if el > cur_sublist[-1]:
				cur_sublist.append(el)
			else:
				longest_sublist = cur_sublist if len(cur_sublist) > len(longest_sublist) else longest_sublist
				cur_sublist = [el]
		return cur_sublist if len(cur_sublist) > len(longest_sublist) else longest_sublist
"""
