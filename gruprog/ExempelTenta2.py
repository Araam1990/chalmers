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
	- return returnerar ett värde från en funktion

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
	x = -->	| :K 	  |<----------|
			| ls = [  |	   _______|__
			|     a,--|--> | :L   | |
			|	  b,--|--> | k = -| |
			|	  c---|--> |________|
			| ]       |
			|_________|

	after
			___________
	x = -->	| :K 	  |<----------|
			| ls = [  |	   _______|__
			|     a,--|--> | :L   | |
			|	  b,--|--> | k = -| |
			|	  c,--|--> |________|
			|	  d---|-|  __________ 
			| ]       | -->| :L     |
			|_________|    | k = -| |
					^	   |______|_|
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
	
"""

"""	Uppgift A6: 4 poäng

	Förklara Principle of Least Astonishment. Ge konkreta exempel på vad den innebär. 

	Svar:

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

"""

"""	Uppgift B3: 5 poäng 

	Förklara vad en datastruktur är. Ge exempel på några olika enkla datastrukturer, och vad som bör 
	avgöra vilken datastruktur vi väljer att använda i en specifik situation.

	Svar:

"""

"""	Uppgift B4: 5 poäng 

	Förklara hur mekanismerna arv och komposition båda kan hjälpa oss att undvika kodduplicering. 
	Förklara hur respektive mekanism löser problemet, och diskutera för och nackdelar. 

	Svar:

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