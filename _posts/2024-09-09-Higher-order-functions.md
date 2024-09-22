---
layout: post
title: "Higher Order Functions in Python"
date: 2024-09-09
permalink: /posts/:title
categories: [Reading Python]
--- 
- HOF take one or more functions as arguments, return a function, or both.
-  This allows for more abstract and flexible programming patterns 

#### Functions as First-class Citizens 
- In Python functions are first-class citizens. This means you can pass them as arguments to other functions, return them from other functions, and assign them to variables.  HOF leverage this feature 


```python
# Example 
def greet(): 
    return "Hello"

def call_func(func): 
    return func() 

# passing the greet fun to call_func 

print(call_func(greet))
```

    Hello


- In the example above call_func is a higher-order function because it accepts another function(greet) as an argument 

#### Returning functions from functions 
   - A higher order function can also return a function as its result


```python
### example 
def create_multiplier(x): 
    def multiplier(y): 
        return x * y 
    return multiplier 

times_three = create_multiplier(3)
print(times_three(5))
```

    15


- Here, `create_multiplier` returns a new function(`multiplier`) that multiplies its argument by `x`. The returned function is then stored in `times_three`, which can be used to multiply any number by 3 

#### Common Higher-Order Function in Python 
- Python has several built-in higher-order functions, which are useful for operations like mapping, filtering, and reducing data 
- `map`: Applies a function to all items in an iterable(e.g list) 



```python
nums = [1,2,3,4]
squared = list(map(lambda x: x** 2, nums))
print(squared)
```

    [1, 4, 9, 16]


- `filter`: filters elements in an iterable based on a function that returns `True` or `False` 


```python
nums = [1,2,3,4]
evens = list(filter(lambda x: x%2 == 0, nums))
print(evens)
```

    [2, 4]


- `reduce`: Applies a function cumulatively to the items of an iterable, reducing it to a single value. 
- You need to import it from `functools` 


```python
from functools import reduce 
nums = [1,2,3,4]

product = reduce(lambda x, y: x * y, nums )
print(product)
```

    24


#### Decorators 
- A decorator is a special type of higher-order functions that 'wraps' another function, adding additional behavior to it. 
- it's commonly used for logging, authentication, timing, etc 


```python
#Example: simple decorator 
def decorator(func): 
    def wrapper(): 
        print("Something extra before the function call ")
        result = func() 
        print("something extra after the function call. ")
        return result 
    return wrapper 

@decorator
def say_hello(): 
    print("Hello!")

say_hello()

```

    Something extra before the function call 
    Hello!
    something extra after the function call. 


- In this example, the `decorator` function takes `say_hello` as an argument and adds some behavior before and after calling it. Using the `@decorator` syntax is shorthand for `say_hello=decorator(say_hello)`
  

#### Currying 
- Here, a function that takes multiple arguments is transformed into a series of functions, each with a single argument.
- Python doesn't enforce currying natively, but you can achieve it manually with higher-order functions 
 



```python
# example curried function 
def curried_add(x): 
    def add_to(y):
        return x + y 
    return add_to 

add_five = curried_add(5)
print(add_five(10))
```

    15

