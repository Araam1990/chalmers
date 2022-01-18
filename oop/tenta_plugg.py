from abc import ABC, abstractclassmethod

"""
https://play.chalmers.se/media/Lecture+7-2A+Revision/0_q3b77w38
https://refactoring.guru/design-patterns/decorator
https://docs.google.com/document/d/1xnfqXqUVfe49HLLmR8NmttV2_ft6sCwBEjIhSNsaDr0/edit#heading=h.9idc5t4lfezo
https://chalmers.instructure.com/courses/16169/files/1955820?wrap=1
"""

# Principles

"""
1. Explain the principle.
2. Give a concrete example of how you follow, or break, the principle.
3. What is the purpose of the principle? Why is it good to follow the prin-
ciple? (*)
"""

# Single Responsibility Principle (SRP)
"""
Every class should only have on responsibility, with other words, it should only have one reason to change.

Can be seen as another way to define High Cohesion, Low Coupling

Example: One handles database modification and another handles database queries. If we now decide to change the type of database we use we would have to change multiple different classes/modules.

Maintainable, testable, easily accessable
"""

# Open-Closed Principle (OCP)
"""
Modules should be open for extension but closed for modification. We should be able extend the system without having to change it, or as little as possible.

Example: The head class should work with or without the hat class. You can break it by using type-checking which you need to change everytime something is added.

Future-compatible, maintanable, reuseable, extendable
"""

# Liskov Substitution Principle (LSP) (*)
"""
If S is a subtype of T, then for all programs defined in terms of T we should be able to substitute an object of T with an object of S and still get the same behavior. S must fulfill the contract of type T.

Example: If Car is a subclass of Vehicle which has a gas method, then the cars implementation of the gas method should be expected. If the gas method on Car would accelerate the car AND change the color of the road, then the contract is broken and thus it doesn't follow the principle.

Expectable behavior, better hierarchy
"""

# Interface Segregation Principle (ISP)
"""
No client should be forced to depend on methods it does not use. So instead we want to introduce an abstraction/interface for the shared methods. Similar to SRP but for interfaces.

Example: Lets say we have an interface called Arithmetic with the methods add and subtract. It would be better to split it up into two interfaces since if we just want an adder we'd have to implement subtract as well.

Reduces unnecessary code since classes dont need to implement methods they don't use. Lets us use the abstraction instead which is a weaker dependency
"""

# Dependency Inversion Principle (DIP)
"""
We should depend on abstractions and not on concrete implementations. Use supertypes, or make one if its needed and one doesn't exist, instead of subtypes since its a weaker dependency.

Example: 

Reduce dependencies, maintanable, flexibility
"""

# Separation of Concern (SoC)
"""
Do one thing and do it well. General concept of modular design. Break up the program so each part does one thing and one thing only and all code for that one thing is in the same place.

Applied to methods: functional decomposition
Applied to classes: Single Responsibility Principle
Applied to packages: Module pattern

Example: The MVC pattern

Simultaneous changes, reuseable, maintainable, testable
"""

# High Cohesion, Low Coupling
"""
High Cohesion: classes within a module should work tightly together to solve the modules task/responsibility

Low Coupling: The module should have as few and as weak dependencies as possible to other modules. 

Example: instead of fetching the same data in multiple classes within a module, fetch it once and share it between the classes inside a module.

reuseable, readable, maintainable
"""

# Prefer Composition over Inheritance
"""
If we have a class A that uses functionality of class B then we should make use of an instance of a class B rather than inherit from it. This because inheritance is a stronger dependency than composition

Example: 

Flexibility
"""

# Law of Demeter
"""
Don't talk to strangers. A method of an object may only call methods from its own object and its attributes, its parameters, any objects created in the method and any global variables accessible by its object in the scope of the method. So don't call methods outside your class unless you have to.

Example: Don't chain messages (a.getB().getC().doSomething())

Less dependencies, maintainable, readable, adheres to other principles
"""

# Command-Query Separation Principle
"""
A method should either have a side effect or return a value, not both. Seperation of Concerns, we want to be able to do one without the other.

Example: pop is a common operation which breaks the CQSP since it removes a value and returns said value.

Less unexpected behavior
"""


# Design patterns
"""
General solutions to common problems within object oriented design. Sort of a template on how certain problems can be solved and should be considered best-practises.

They have been created over time by experts with a lot more experience than you and me. Since they are common solutions, many other programmers will recognise them and thus have an easier time understanding your code if you implement them yourself as well as it will be easier to follow the principles of good design.

For some of the design patterns we covered in the course:
1. Describe design pattern X.
2. In which situations can you use X?
3. Which components are included in X?
4. What design problems can we solve with the help of X? (*)
"""

# Template method
"""
When a mostly generic algorithm has context-dependent behavior: Create an abstract superclass that implements the algorithm; Include an abstract method reprensenting the context-dependent behavior, and call this method from the algorithm; Implement the context-dependent behavior in different subclasses.

code-reuse, less duplicate code, expandable
"""

class Heap(ABC): # The abstract superclass with a context dependant ordering method
    def __init__(self, key=lambda x:x):
        self._inner_list = []
        self._key = key
    
    def __repr__(self):
        return f"{self._inner_list}"

    def __len__(self) -> int:
        return len(self._inner_list)
    
    @abstractclassmethod
    def _ordering(self, el1, el2):
        pass

    def peek(self):
        return self._inner_list[0]

    def push(self, el):
        self._inner_list.append(el)
        i = len(self._inner_list) - 1
        j = i // 2
        while i > 0 and self._ordering(self._key(self._inner_list[i]), self._key(self._inner_list[j])):
            self._inner_list[i], self._inner_list[j] = self._inner_list[j], self._inner_list[i]
            i, j = j, j // 2

    def pop(self):
        if len(self) == 0:
            raise IndexError("No available value to pop")
        self._inner_list[0], self._inner_list[-1] = self._inner_list[-1], self._inner_list[0]
        el = self._inner_list.pop()
        i, j = 0, 1
        while j < len(self._inner_list):
            if j + 1 < len(self._inner_list) and self._ordering(self._inner_list[j + 1], self._inner_list[j]):
                j += 1
            elif j == len(self._inner_list):
                break
            if self._ordering(self._inner_list[j], self._inner_list[i]):
                self._inner_list[i], self._inner_list[j] = self._inner_list[j], self._inner_list[i]
                i, j = j, j*2+1
            else:
                break
        return el

class MinHeap(Heap): # Context 1
    def _ordering(self, el1, el2):
        return el1 < el2

class MaxHeap(Heap): # Context 2
    def _ordering(self, el1, el2):
        return el1 > el2

# Bridge
"""
An aspect that can vary independently of the object itself is extracted into its own hierarchy with different concrete implementations that are used with the object as needed.

Example: Comparators with different behaviors used in the sort method.

Less code, maintanable, less code breaking, abstraction over implementation
"""

class Shape(ABC):
    def __init__(self, color):
        self.color = color

class Triangle(Shape):
    def __init__(self, color):
        super().__init__(color)

class Square(Shape):
    def __init__(self, color):
        super().__init__(color)

class Color(ABC):
    pass

class Red(Color):
    def __init__(self):
        self.rgb = [255,0,0]

class Blue(Color):
    def __init__(self):
        self.rgb = [0,0,255]

# Factory
"""

"""

class Factory:
    @staticmethod
    def createRedSquare():
        return Square(Red())
    
    @staticmethod
    def createBlueTriangles(amount):
        return [Triangle(Blue()) for _ in range(amount)]


# Chain of Responsibility (*)
"""

"""

# Module
"""

"""

# Strategy
"""

"""

# Decorator (*)
"""

"""

# Observer
"""

"""

# Facade
"""

"""

# State
"""
If an object can vary between a finite number of different states then we can extract the methods and create an interface with them from which we define implementations we then use inside the object. The state is changeable.
"""

# Adapter
"""
When you want an object A to work in place of an object B but their signature is different you can make use of an adapter which wraps object A and reroutes methods.

Example: We have a calculator which uses full operation names, such as addition and subtraction, but in the object we make use of it we use abreviations, such as add and sub. We can then make an adapter with the methods add and sub which calls the addition and subtraction methods. Another use would be unit conversions, imperial to metric or kilometers to meters.
"""

class Calculator:
    def addition(o1, o2):
        return o1+o2

    def subtraction(o1, o2):
        return o1-o2
        
class CalculatorWrapper:
    def __init__(self):
        self.calculator = Calculator()
    
    def add(self, o1, o2):
        return self.calculator.addition(o1, o2)

    def sub(self, o1, o2):
        return self.calculator.subtraction(o1, o2)

class App:
    def __init__(self):
        self.calculator = CalculatorWrapper()
    
    def doSomething(self):
        a = self.calculator.add(1,2)
        b = self.calculator.sub(1,2)
        return a, b

# Model-View-Controller (MVC)
"""

"""