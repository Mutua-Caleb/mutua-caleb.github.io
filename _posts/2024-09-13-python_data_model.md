---
layout: post
title: "Python Data Model"
date: 2024-09-13
permalink: /posts/:title
categories: [Reading Python]
---

If you learned another object-oriented language before Python, you may have found it strange to use **len(collection)** instead of collection.len(). This apparent oddity is the tip of an iceberg that when properly understood, it is the ke to everything we call Pythonic 

- The **python data model** describes the API that you can call to make your own objects lay well with the most idiomatic language features 
- It's helpful to think of the data model as a description of Python as a framework. It formalises the interface of the building blocks of the language itself, such as sequences, iterators, functions, classes, context managers and so on. 
- While coding with any framework you spend a lot of time implementing methods that are called by the framework. The same happens when when you leverage the Python data model. The interpreter invokes special methods to perform basic object operations, often triggered by special syntax. This methods are called **dunder** methods. For example `getitem()` supports `obj[key]`. In order to evaluate `my_collection[key]`, the interpreter calls `mycollection.getitem(key)`
- The special method names allows your objects to implement, support, and interact with basic language constructs such as: 
  - iteration
  - collections
  - attribute access 
  - operator overloading 
  - function and method invocation 
  - object creation and destruction 
  - string representation and formatting
  - managed contexts(i.e with blocks)
  


```Python
ranks = [str(n) for n in range(2,11)] + list('JQKA')
print(ranks)
suits = 'spades diamonds clubs hearts'.split()
print(suits)
```

    ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    ['spades', 'diamonds', 'clubs', 'hearts']



```Python
import collections
#Let's try to create 52 cards 
Card = collections.namedtuple('Card', ['rank', 'suit'])
_cards = [Card(rank, suit) for suit in suits for rank in ranks]
for card in _cards: 
    print (card)
```

    Card(rank='2', suit='spades')
    Card(rank='3', suit='spades')
    Card(rank='4', suit='spades')
    Card(rank='5', suit='spades')
    Card(rank='6', suit='spades')
    Card(rank='7', suit='spades')
    Card(rank='8', suit='spades')
    Card(rank='9', suit='spades')
    Card(rank='10', suit='spades')
    Card(rank='J', suit='spades')
    Card(rank='Q', suit='spades')
    Card(rank='K', suit='spades')
    Card(rank='A', suit='spades')
    Card(rank='2', suit='diamonds')
    Card(rank='3', suit='diamonds')
    Card(rank='4', suit='diamonds')
    Card(rank='5', suit='diamonds')
    Card(rank='6', suit='diamonds')
    Card(rank='7', suit='diamonds')
    Card(rank='8', suit='diamonds')
    Card(rank='9', suit='diamonds')
    Card(rank='10', suit='diamonds')
    Card(rank='J', suit='diamonds')
    Card(rank='Q', suit='diamonds')
    Card(rank='K', suit='diamonds')
    Card(rank='A', suit='diamonds')
    Card(rank='2', suit='clubs')
    Card(rank='3', suit='clubs')
    Card(rank='4', suit='clubs')
    Card(rank='5', suit='clubs')
    Card(rank='6', suit='clubs')
    Card(rank='7', suit='clubs')
    Card(rank='8', suit='clubs')
    Card(rank='9', suit='clubs')
    Card(rank='10', suit='clubs')
    Card(rank='J', suit='clubs')
    Card(rank='Q', suit='clubs')
    Card(rank='K', suit='clubs')
    Card(rank='A', suit='clubs')
    Card(rank='2', suit='hearts')
    Card(rank='3', suit='hearts')
    Card(rank='4', suit='hearts')
    Card(rank='5', suit='hearts')
    Card(rank='6', suit='hearts')
    Card(rank='7', suit='hearts')
    Card(rank='8', suit='hearts')
    Card(rank='9', suit='hearts')
    Card(rank='10', suit='hearts')
    Card(rank='J', suit='hearts')
    Card(rank='Q', suit='hearts')
    Card(rank='K', suit='hearts')
    Card(rank='A', suit='hearts')



```Python
# The following is a very simple example but it demonstrates the power of implementing just two special methods __getitem__ and __len__ 
import collections
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck: 
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split() 

    def __init__(self): 
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks] 
    def __len__(self): 
        return len(self._cards)
    
    def __getitem__(self,position): #allows indexing and slicing operations 
        return self._cards[position] 

beer_card = Card('7', 'diamonds')
beer_card
    
```




    Card(rank='7', suit='diamonds')




```Python
#let's try to call the len() function that we've implemented 
deck = FrenchDeck()
print(len(deck))
```

    52



```Python
#Reading specific cards from the deck --say, the first or the last should be really easy to do 
#This is due to the __getitem()__ method 
print(deck[0])
print(deck[-1])
```

    Card(rank='2', suit='spades')
    Card(rank='A', suit='hearts')



```Python
#should we create a method to pick a random card? No need. Python already has a function to do so
from random import choice 
print(choice(deck))
print(choice(deck))
```

    Card(rank='A', suit='spades')
    Card(rank='10', suit='spades')



```Python
### But it gets better
#Because our __getitem__ delegates to the [] operator of self._cards, our deck automatically supports slicing. here's how we look at the top three cards from a brand new deck and then pick just the aces by starting on index 12 and skipping 13 cards at a time 
print(deck[:3])
print(deck[12::13])
```

    [Card(rank='2', suit='spades'), Card(rank='3', suit='spades'), Card(rank='4', suit='spades')]
    [Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'), Card(rank='A', suit='clubs'), Card(rank='A', suit='hearts')]



```Python
#just by implementing the __getitem__ special method, our deck is also iterable: 
for card in deck: 
    print(card)
```

    Card(rank='2', suit='spades')
    Card(rank='3', suit='spades')
    Card(rank='4', suit='spades')
    Card(rank='5', suit='spades')
    Card(rank='6', suit='spades')
    Card(rank='7', suit='spades')
    Card(rank='8', suit='spades')
    Card(rank='9', suit='spades')
    Card(rank='10', suit='spades')
    Card(rank='J', suit='spades')
    Card(rank='Q', suit='spades')
    Card(rank='K', suit='spades')
    Card(rank='A', suit='spades')
    Card(rank='2', suit='diamonds')
    Card(rank='3', suit='diamonds')
    Card(rank='4', suit='diamonds')
    Card(rank='5', suit='diamonds')
    Card(rank='6', suit='diamonds')
    Card(rank='7', suit='diamonds')
    Card(rank='8', suit='diamonds')
    Card(rank='9', suit='diamonds')
    Card(rank='10', suit='diamonds')
    Card(rank='J', suit='diamonds')
    Card(rank='Q', suit='diamonds')
    Card(rank='K', suit='diamonds')
    Card(rank='A', suit='diamonds')
    Card(rank='2', suit='clubs')
    Card(rank='3', suit='clubs')
    Card(rank='4', suit='clubs')
    Card(rank='5', suit='clubs')
    Card(rank='6', suit='clubs')
    Card(rank='7', suit='clubs')
    Card(rank='8', suit='clubs')
    Card(rank='9', suit='clubs')
    Card(rank='10', suit='clubs')
    Card(rank='J', suit='clubs')
    Card(rank='Q', suit='clubs')
    Card(rank='K', suit='clubs')
    Card(rank='A', suit='clubs')
    Card(rank='2', suit='hearts')
    Card(rank='3', suit='hearts')
    Card(rank='4', suit='hearts')
    Card(rank='5', suit='hearts')
    Card(rank='6', suit='hearts')
    Card(rank='7', suit='hearts')
    Card(rank='8', suit='hearts')
    Card(rank='9', suit='hearts')
    Card(rank='10', suit='hearts')
    Card(rank='J', suit='hearts')
    Card(rank='Q', suit='hearts')
    Card(rank='K', suit='hearts')
    Card(rank='A', suit='hearts')



```Python
# the deck can also be iterated in reverse: 
for card in reversed(deck): 
    print(card)
```

    Card(rank='A', suit='hearts')
    Card(rank='K', suit='hearts')
    Card(rank='Q', suit='hearts')
    Card(rank='J', suit='hearts')
    Card(rank='10', suit='hearts')
    Card(rank='9', suit='hearts')
    Card(rank='8', suit='hearts')
    Card(rank='7', suit='hearts')
    Card(rank='6', suit='hearts')
    Card(rank='5', suit='hearts')
    Card(rank='4', suit='hearts')
    Card(rank='3', suit='hearts')
    Card(rank='2', suit='hearts')
    Card(rank='A', suit='clubs')
    Card(rank='K', suit='clubs')
    Card(rank='Q', suit='clubs')
    Card(rank='J', suit='clubs')
    Card(rank='10', suit='clubs')
    Card(rank='9', suit='clubs')
    Card(rank='8', suit='clubs')
    Card(rank='7', suit='clubs')
    Card(rank='6', suit='clubs')
    Card(rank='5', suit='clubs')
    Card(rank='4', suit='clubs')
    Card(rank='3', suit='clubs')
    Card(rank='2', suit='clubs')
    Card(rank='A', suit='diamonds')
    Card(rank='K', suit='diamonds')
    Card(rank='Q', suit='diamonds')
    Card(rank='J', suit='diamonds')
    Card(rank='10', suit='diamonds')
    Card(rank='9', suit='diamonds')
    Card(rank='8', suit='diamonds')
    Card(rank='7', suit='diamonds')
    Card(rank='6', suit='diamonds')
    Card(rank='5', suit='diamonds')
    Card(rank='4', suit='diamonds')
    Card(rank='3', suit='diamonds')
    Card(rank='2', suit='diamonds')
    Card(rank='A', suit='spades')
    Card(rank='K', suit='spades')
    Card(rank='Q', suit='spades')
    Card(rank='J', suit='spades')
    Card(rank='10', suit='spades')
    Card(rank='9', suit='spades')
    Card(rank='8', suit='spades')
    Card(rank='7', suit='spades')
    Card(rank='6', suit='spades')
    Card(rank='5', suit='spades')
    Card(rank='4', suit='spades')
    Card(rank='3', suit='spades')
    Card(rank='2', suit='spades')



```Python
# Iteration is often implicit. If a collection has __contains__ method, the in operator does a sequential scan. Case in point: it works with our FrenchDeck class because it is iterable 

Card('Q', 'hearts') in deck
```




    True




```Python
Card('7', 'beasts') in deck
```




    False



**How about sorting**? 
- A common system of ranking cards is by rank(with aces being highest), then by suits in the order of spades(highest), then hearts, diamonds with clubs(lowest)
- Here is a function that ranks cards by that rule, returning 0 for the 2 of clubs and 51 for the ace of spades 
  


```Python
deck = FrenchDeck()
suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card): 
    rank_value = FrenchDeck.ranks.index(card.rank) 
    return rank_value * len(suit_values) + suit_values[card.suit] 

for card in sorted(deck, key=spades_high): 
    print(card)
```

    Card(rank='2', suit='clubs')
    Card(rank='2', suit='diamonds')
    Card(rank='2', suit='hearts')
    Card(rank='2', suit='spades')
    Card(rank='3', suit='clubs')
    Card(rank='3', suit='diamonds')
    Card(rank='3', suit='hearts')
    Card(rank='3', suit='spades')
    Card(rank='4', suit='clubs')
    Card(rank='4', suit='diamonds')
    Card(rank='4', suit='hearts')
    Card(rank='4', suit='spades')
    Card(rank='5', suit='clubs')
    Card(rank='5', suit='diamonds')
    Card(rank='5', suit='hearts')
    Card(rank='5', suit='spades')
    Card(rank='6', suit='clubs')
    Card(rank='6', suit='diamonds')
    Card(rank='6', suit='hearts')
    Card(rank='6', suit='spades')
    Card(rank='7', suit='clubs')
    Card(rank='7', suit='diamonds')
    Card(rank='7', suit='hearts')
    Card(rank='7', suit='spades')
    Card(rank='8', suit='clubs')
    Card(rank='8', suit='diamonds')
    Card(rank='8', suit='hearts')
    Card(rank='8', suit='spades')
    Card(rank='9', suit='clubs')
    Card(rank='9', suit='diamonds')
    Card(rank='9', suit='hearts')
    Card(rank='9', suit='spades')
    Card(rank='10', suit='clubs')
    Card(rank='10', suit='diamonds')
    Card(rank='10', suit='hearts')
    Card(rank='10', suit='spades')
    Card(rank='J', suit='clubs')
    Card(rank='J', suit='diamonds')
    Card(rank='J', suit='hearts')
    Card(rank='J', suit='spades')
    Card(rank='Q', suit='clubs')
    Card(rank='Q', suit='diamonds')
    Card(rank='Q', suit='hearts')
    Card(rank='Q', suit='spades')
    Card(rank='K', suit='clubs')
    Card(rank='K', suit='diamonds')
    Card(rank='K', suit='hearts')
    Card(rank='K', suit='spades')
    Card(rank='A', suit='clubs')
    Card(rank='A', suit='diamonds')
    Card(rank='A', suit='hearts')
    Card(rank='A', suit='spades')


**How special methods are used**
- Special methods are meant to be called by the python interpreter, and not by you
- You don't write `my_object.__len__()`. you write `len(my_object)`, and if `my_object` is an instance of a user-defined class, then python calls the `__len__` instance method that you implemented 

## Emulating Numeric Types 
- Several special methods allow user objects to respond to operators such as `* , +, `. Our goal here is to further illustrate the use of special methods through another example 

- We will start by designing the API for such a class by writing simulated console session that we can use later as a doctest. This snippet tests the vector addition
```Python 
v1 = Vector(2,4)
v2 = Vector(2,1)
v1 + v2 
    Vector(4,5)

v = Vector(3,4)
abs(v) #calculate the magnitude of vector=(sqrt(a*a + b*b))
    5.0 

 We can also implement * operator to perform scalar multiplication (ie multiplying a vector by a number to produce a ne vector with the same direction and a multiplied magnitude): 
 V* 3
  Vector(9,12)
 abs(V*3) #sqrt(9*9 + 12*12)
   15.0
```



```Python
#let's implement the vector class using __repr__, __abs__, __add__ and __mul__

from math import hypot 

class Vector: 
    def __init__(self, x=0, y=0):
        self.x = x 
        self.y = y 
    
    def __repr__(self): 
        return 'Vector(%r, %r)' % (self.x, self.y)
    
    def __abs__(self): 
        return hypot(self.x, self.y)
    
    def __bool__(self): 
        return bool(abs(self))
    
    def __add__(self, other): 
        x = self.x + other.x 
        y = self.y + other.y 
        return Vector(x,y)

    def __mul__(self, scalar): 
        return Vector(self.x * scalar, self.y * scalar) 
```


```Python
V = Vector(5, 0)
V2 = Vector(4,5)

V3 = V2 * 4
V3
```




    Vector(16, 20)




```Python
V =Vector(3,4)
print(abs(V))
```

    5.0


**String Representation**
- The **repr** special method is caleld by the repr built-in to get the string representation  of the object for inspection. If we didn't implement **repr**, vector instances would be shown in the console like  <Vector object at 0x10e100070>
- The interactive console and debugger call **repr** on the results of teh expressions evaluated,as does the **%** placeholder in class formatting with the % operator, and the !r conversion field 
- Note that in our **repr** implementation, we used %r to obtain the standard representation of the attributes to be displayed 

**Boolean Value of a custom type**
- Our implementation of **bool** is simple: it returns False if the magnitude of the vector is zero, True otherwise 

- By default, instances of user-defined classes are considered  ` __truthy__ ` either  ` __bool__ ` or   ` __len__ ` is not implemented, python tries to invoke  ` x.__len__() `  and if it returns zero, bool returns False. Otherwise bool returns true

