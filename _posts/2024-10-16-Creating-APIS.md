---
layout: post
title: "Creating APIs in Python - Part 1"
date: 2024-10-16
permalink: /posts/:title
categories: [APIs]
excerpt: "This series about APIs is taught in a rather simple manner. I have refrained from using a lot of jargon and gone for simple examples that are easier to digest. You might also notice that the language and examples are kid-like."
---
This series about APIs is taught in a rather simple manner. I have refrained from using a lot of jargon and gone for simple examples that are easier to digest. You might also notice that the language and examples are kid-like. This is by design because I believe that if you want to truly understand a topic you should try as much as possible to explain to a child.  

### What's an API? 
- An API(Application Programming Interface) is like a messenger. Imagine you're in restaurant, and you want to order food. You tell the waiter what you want, and the waiter goes to the kitchen to get it for you. 
- The waiter is like an API- it takes your request (your order) and sends it to the kitchen(the backend). Then, the kitchen makes the food and the waiter brings it back to you. 
- So, an API helps two things talk to each other --like your phone and a website, or a mobile app and a server

### What is REST? 
- REST(Representational State Transfer) is a set of rules that make APIs work better. Think of REST like traffic rules that cars have to follow so they don't crash. These rules make sure everything stays organized then you ask for information from an API
- For example, some of the REST rues are: 
  - **Client-server**: Like a customer and a chef. The customer(client) asks, and the chef(server) delivers. They're separate but work together through the API(waiter)
  - **Stateless**:  Every time you order, it's like a new order, even if you've ordered before, the server doesn't remember the previous requests. 
  - **HTTP(HyperText Transfer Protocol)** is the way APIs talk. It's like the language they use to understand each other. 

- Imagine you're writing down what you want in your order using different action words(HTTP verbs): 
  -  __GET__: Means you're asking for something, like "Get me all the toys" 
  -  __POST__: Means you're creating something new, like "Ad this new toy to my toy box" 
  -  __PUT__ : Means you're changing something completely, like "Replace my old toy with a new one" 
  -  __DELETE__: Means you want to remove something, like "Take this toy out of my toy box" 

### How Does an API work? 
- Imagine you have a toy box. When you want a toy, you can either **ask** for it(GET), **add** a new toy(POST), **replace** a broken toy (PUT), or **throw one away**(DELETE). The API is like your assistant that helps you do all these things.
- Each action has a specific **endpoint**. Think of an endpoint like a specific shelf or box where a toy is kept. You need to know exactly where to send your assistant to get what you want. 
- for example: 
  - **GET /toys**: "Get me all the toys in my toy box." 
  - **POST /toys**: "Add this new toy to my toy box" 
  - **PUT /toys/2**: "Replace toy number 2 with a new one" 
  - **DELETE /toys/2**: "Throw away toy number 2" 
Here's what happens when you interact with an API: 
  1. **Request**: You send a request to the API using one of these methods(GET, POST, PUT, DELETE). It's like telling your assistant what to do. 
  2. **Response**: The API sends back a response. It's like your assistant bringing you the toy you asked for. 

**What is JSON?**
- JSON (Javascript Object Notation Notation) is a way of organizing information that makes it easy for APIs to send and receive data. Think of JSON like a toy catalog that shows you all the toys available with pictures and descriptions. 
- For example, if you have two toys in your box, this is how you can show them using JSON: 



```python

{
  "toys": [
    {
      "id": 1,
      "name": "Toy Car",
      "color": "Red"
    },
    {
      "id": 2,
      "name": "Toy Robot",
      "color": "Blue"
    }
  ]
}
```

- Here's what this means: 
  - You have a list of toys 
  - Each toy has an ID(a unique number so you can identify it), a **name** (what type of toy it is), and a **color** 
- When you ask for the toys(using a **GET request**), the API sends you this JSON list as a response 
- Here are some important ones: 
  - 200 OK: Everything worked! The API found the toys you asked for and sent them back 
  - 201 created: The API successfully added a new toy to your toy box. 
  - 404 Not Found: The API couldn't find the toy you were asking for (maybe it  doesn't exist)
  - 400 Bad Request: Something went wrong with your request(like you asked for a toy), but forgot to tell the API which one. 

**Let's Build a Simple API with Flask**
- Now, let's build a simple API to handle your toy collection using Flask (a Python tool that helps you build web apps and APIs) 
1. Set UP flask: First, you need to install Flask. You can do this in your project's virtual environment 




```python
pip install Flask 
```

2. **Create an API**: 
   - Now let's write some code to create an API that shows your toy collection. We'll use Flask to handle requests and responses


```python
from flask import Flask, jsonify

app = Flask(__name__)

# Toy collection (stored in memory)
toys = [
    {"id": 1, "name": "Toy Car", "color": "Red"},
    {"id": 2, "name": "Toy Robot", "color": "Blue"}
]

# API endpoint to get all toys
@app.route('/toys', methods=['GET'])
def get_toys():
    return jsonify({"toys": toys}), 200  # Return toys with HTTP status 200 (OK)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

```


```python
curl http://localhost:5000/toys

{
  "toys": [
    {
      "id": 1,
      "name": "Toy Car",
      "color": "Red"
    },
    {
      "id": 2,
      "name": "Toy Robot",
      "color": "Blue"
    }
  ]
}


```
### Creating a new TOY Using POST
let's add a new toy to the API using POST


```python
from flask import Flask, jsonify, request  # We need 'request' to handle incoming data

app = Flask(__name__)

# Toy collection
toys = [
    {"id": 1, "name": "Toy Car", "color": "Red"},
    {"id": 2, "name": "Toy Robot", "color": "Blue"}
]

# API endpoint to get all toys
@app.route('/toys', methods=['GET'])
def get_toys():
    return jsonify({"toys": toys}), 200

# API endpoint to add a new toy (POST method)
@app.route('/toys', methods=['POST'])
def add_toy():
    # Get data from the request (the new toy details)
    new_toy = request.get_json()
    new_id = len(toys) + 1  # Automatically assign the next ID
    new_toy['id'] = new_id  # Add ID to the new toy
    toys.append(new_toy)  # Add the new toy to the toy collection
    return jsonify(new_toy), 201  # Return the new toy with status 201 (Created)

if __name__ == '__main__':
    app.run(debug=True)

```


```python
curl -X POST http://localhost:5000/toys -H "Content-Type: application/json" -d '{"name": "Toy Train", "color": "Green"}'
{
  "color": "Green",
  "id": 3,
  "name": "Toy Train"
}
```

After this, if you visit the /toys URL again you'll see the new toy, "Toy Train", in the list


```python
curl  http://localhost:5000/toys
{
  "toys": [
    {
      "color": "Red",
      "id": 1,
      "name": "Toy Car"
    },
    {
      "color": "Blue",
      "id": 2,
      "name": "Toy Robot"
    },
    {
      "color": "Green",
      "id": 3,
      "name": "Toy Train"
    }
  ] 
}

```

### Updating a toy(PUT)
- What if you want to change the details of a toy that's already in your collection? For example, maybe your "Toy Car" should be blue instead of red. 
- This is where the **PUT** method comes in handy. **PUT** 
- Here's how we can add this feature to our API: 


```python

from flask import Flask, jsonify, request  # We need 'request' to handle incoming data

app = Flask(__name__)

# Toy collection
toys = [
    {"id": 1, "name": "Toy Car", "color": "Red"},
    {"id": 2, "name": "Toy Robot", "color": "Blue"}
]

# API endpoint to get all toys
@app.route('/toys', methods=['GET'])
def get_toys():
    return jsonify({"toys": toys}), 200

# API endpoint to add a new toy (POST method)
@app.route('/toys', methods=['POST'])
def add_toy():
    # Get data from the request (the new toy details)
    new_toy = request.get_json()
    new_id = len(toys) + 1  # Automatically assign the next ID
    new_toy['id'] = new_id  # Add ID to the new toy
    toys.append(new_toy)  # Add the new toy to the toy collection
    return jsonify(new_toy), 201  # Return the new toy with status 201 (Created)

#API endpoint to update a toy (PUT method) 
@app.route('/toys/<int:toy_id>', methods=['PUT'])
def update_toy(toy_id): 
    toy = next((t for t in toys if t['id'] == toy_id), None) #Find the toy by ID 
    if toy is None: 
        return jsonify({'message': 'Toy not found'}), 404 #Return 404 if toy doesn't exist 
    
    updated_data = request.get_json() #get updated details from the request 
    toy.update(updated_data) #Update the toy with the new details 
    return jsonify(toy), 200 #Return the updated toy with status 200 (OK) 
    


if __name__ == '__main__':
    app.run(debug=True)
```

**How to Test the PUT method** 
You can test the update like this: 


```python

$ curl -X PUT http://localhost:5000/toys/1 -H "Content-Type: application/json" -d '{"name": "Toy Car", "color": "Blue"}' 
```

Now, if you check the toy with ID 1 again, its color should have changed to blue

### Deleting a Toy (DELETE)
- If you no longer want a toy in your collection, you can remove it using **DELETE** method. This is like saying: "Throw this toy away" 
Here's how we can add the delete feature: 


```python
#API endpoint to delete a toy (DELETE method)
@app.route('/toys/<int:toy_id', methods=['DELETE']) 
def delete_toy(toy_id): 
    toy = next((t for t in toys if t['id'] == toy_id), None)
    if toy is None: 
        return jsonify({'message': 'Toy not found'}), 404 # Return 404 if toy doesn't exist

    toys.remove(toy) #Remove the toy from the collection 
    return jsonify({'message': 'Toy deleted'}), 204 #Return 204 No content (success)

```

**How to Test the DELETE method**


```python
curl -X DELETE http://localhost:5000/toys/1
```

If successful, the toy with ID 1 will be removed from the collection, and a **204 No Content** status will be returned.
