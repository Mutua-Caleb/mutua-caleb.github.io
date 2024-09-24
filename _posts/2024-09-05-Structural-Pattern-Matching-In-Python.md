---
layout: post
title: "Structural Pattern Matching In Python "
date: 2024-09-05
permalink: /posts/:title
categories: [Reading Python]
excerpt: "This blog attempts to show the powerful features of Structural Pattern Matching in Python, a feature similar to Ruby's but with some differences."
---

 The first time I encountered this term was while learning Ruby. I was terrified by it — "terrified" doesn’t even fully capture how **scared I felt**.
 I was reading a highly technical blog at the time, and as a beginner, none of it made sense to me. Today, while reading about the match statement in the official Python tutorial, I couldn’t help but think, "Why does this just sound like simple if-elif-else statements?". 
  However, I wasn't technically right. This blog attempts to show the powerful features of SPM 


### Basic Concept of SPM
- The `match` statement allows you to compare a value(or a structure) against one or more patterns and execute code based on the first pattern that matches. 
- The structure being matched can be simple types like numbers or strings, or more complex types like objects and collections 
#### Syntax
```Python
match subject: 
    case pattern1: 
     # action for pattern1 
    case pattern2: 
    # action for pattern2: 
    case _: 
        #Default case(matches anything)
```
`subject`: the value or structure being matched 
`pattern`: The pattern against which the subject is checked 

### Examples 
1. #### Matching simple values 

```Python 
def test_value(value): 
    match value: 
        case 1: 
            print("Matched one!")
        case 2: 
            print("Matched two!") 
        case _: 
            print("Default match")
test_value(1) # Output: Matched one! 
test_value(3) #Output: Default match
```

2. #### Matching Data sequence(e.g lists or tuples)

```Python
def process_sequence(seq): 
    match seq: 
        case []: 
            print("Empty list")
        case [1]: 
            print("Single element: 1")
        case [1,2,3]: 
            print("Matched list [1,2,3]")
        case [1, *rest]: 
            print(f"starts with 1, remaining: {rest}")
        case _: 
            print("Unknown sequence") 

process_sequence([1,2,3]) # Output: matched list [1,2,3]
process_sequence([1,4,5]) #Output: starts with 1, remaining: [4,5]
```

- Here, the pattern `[1, *rest]` is using **deconstruction** to match a list starting with `1` and assigning the rest of the list to the variable `rest` 

 3. ####   Matching classes and object attributes 
- When Matching classes, Python can match against the type of the object and its attributes. Here's where `__match_args__` comes into play

```Python 
class Point: 
    __match_args__ = ('x', 'y')

    def __init__(self,x,y): 
        self.x =x 
        self.y = y
    
    def describe_point(point): 
        match point: 
            case Point(0,0): 
                print("The origin")
            case Point(x,0): 
                print(f"On the X-axis at {x}")
            case Point(0,y): 
                print(f"On the Y-axis at {y}")
            case Point(x,y): 
                print(f"Point at ({x}, {y})")

p1 = Point(1,0)        
describe_point(p1) #Output: On the x-axis at 1 
```

- Here, `__match_args__` allows matching the attributes `x` and `y` positionally 

4. ####  Guard Clauses
- You can add conditions(guards) to patterns to further refine matching logic: 
  
```Python
def classify_number(n): 
    match n: 
        case n if n < 0: 
            print("Negative number")
        case n if ==0: 
            print("zero")
        case n if n > 0: 
            print("Positive number")

classify_number(-5) #Output: Negative number
```

## API Simulation Example 
- Let's simulate a simple API using `match` and `__match_args__` for handling different types of responses. we can treat the API as a service that returns various responses(success, error, or different kinds of data), and we'll use structural pattern matching to process them in a clean and efficient way. 
  
- Here's a simulation where we define API responses using classes and handle them with the `match` statement 

```Python
#define classes for different response types 
class SuccessResponse: 
    __match_args__ = ('data',)

    def __init__(self, data): 
        self.data = data

class ErrorResponse: 
    __match_args__ = ('message',)

    def __init__(self, message): 
        self.message = message 

class NotFoundResponse: 
    __match_args__ = ('resource', )

    def __init__(self, resource): 
        self.resource = resource

class ServerErrorResponse: 
    __match_args__ = ('code', 'message')

    def __init__(self, code, message): 
        self.code = code 
        self.message = message 

# Simulate a function that processes different API responses 
def process_api_response(response): 
    match response: 
        case SuccessResponse(data): 
            print(f"Success! Received data: {data}") 
        case ErrorResponse(message):
            print(f"Error: {message}")
        case NotFoundResponse(resource):
            print(f"Resource '{resource}' not found.")
        case ServerErrorResponse(code, message): 
            print(f"server error {code}, {message}") 
        case _: 
            print("Unknown response format") 

#Simulated API responses 
response1 = SuccessResponse({"temperature": 25, "condition": "Sunny"})
response2 = ErrorResponse("Invalid API key") 
response3 = NotFoundResponse("User")
response4 = ServerErrorResponse(503, "Service Unavailable")


#process each response 
process_api_response(response1)  # Output: Success! Received data: {'temperature': 25, 'condition': 'Sunny'}
process_api_response(response2)  # Output: Error: Invalid API key
process_api_response(response3)  # Output: Resource 'User' not found.
process_api_response(response4)  # Output: Server Error 503: Service Unavailable
```


