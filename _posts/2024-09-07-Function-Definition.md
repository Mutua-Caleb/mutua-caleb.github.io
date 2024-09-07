---
layout: post
title: "Function Definition "
date: 2024-09-07
---

# Defining functions In Python
- Functions are usually defined by `def` keyword in Python
#### Syntax
```Python
def function_name(parameters): 
    # code block 
    return value # optional 
```



```python
## simple example
def greet(name): 
    return f"Hello {name}!"

print(greet("Alice"))
```

    Hello Alice!


#### Parameters and Arguments 
**parameters** are variables listed inside the parentheses in the function definition. 
**Arguments** are the values passed to the function when it is called 



```python
#Example 
def add(a,b): 
    return a +b 

print(add(2,3))
```

    5


**Keyword Arguments**: In keyword arguments, you can pass values explicitly specifying the parameter name, allowing them to be passed in any order 



```python
print(add(b=3, a=2))
```

    5


#### Default Arguments 
- functions can have default parameter values, which are used when an argument is not passed during the function call. 


```python
def greet(name="Guest"): 
    return f"Hello, {name}!"

print(greet())
print(greet("Alice"))
```

    Hello, Guest!
    Hello, Alice!


#### Variable-Length Arguments 
- Python allows functions to accept arbitrary numbers of arguments using `*args`(for non-keyword arguments) and `**kwargs` (for keyword arguments) 
- `args` collects positional arguments into a tuple 
- `**kwargs` collects keyword arguments into a dictionary 



```python
## Example of `**kwargs`
def print_info(**info): 
    for key, value in info.items(): 
        print(f"{key}: {value}") 

print_info(name="Alice", age=25, country="USA") 




```

    name: Alice
    age: 25
    country: USA


#### Scope and Lifetime of Variables
**Local scope**: Variables defined inside a function are local to that function and cannot be accessed outside of it. 
**Global scope**: Variables defined outside any function are global and can be accessed inside functions, though to modify them inside a function, you need to use the global keyword



```python
x = 10 # global variable

def modify(): 
    global x 
    x = 5 # modifies global variable 

modify() 

print(x)
```

    5


#### Lambda Function 
A **lambda** function is a small anonynous function defined using the `lambda` keyword. It can take any number of arguments but has a single expression

##### Syntax 
```Python
lambda arguments: expression
```


```python
square = lambda x: x*x 
print(square(5))
```

    25


#### Docstrings in Functions
- They document what a function does. It is written as the first statement inside a function using triple quotes 
  


```python
def greet(name): 
    """ This function greets the person whose name is passed """
    return f"Hello, {name}!"
print(greet.__doc__)
```

     This function greets the person whose name is passed 


#### Higher-order functions
- In python, functions are treated as first-class citizens, meaning they can be passed as arguments to other functions, returned fro`m other functions, or assigned to variables. 


```python
def apply_function(func, value): 
    return func(value)
```
