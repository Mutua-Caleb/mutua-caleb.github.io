---
layout: post
title: "Creating APIs in Python - Part 2"
date: 2024-10-17
permalink: /posts/:title
categories: [APIs]
excerpt: "Flask-RESTful is a python extension for Flask that helps you build RESTful APIs faster and in a more organized way. Think of it as adding extra tools to your toolbox so you can build your APIs more efficiently."
---

### What is Flask-Restful? 
- Flask-RESTful is a python extension for Flask that helps you build RESTful APIs faster and in a more organized way. Think of it as adding extra tools to your toolbox so you can build your APIs more efficiently. 
- Earlier, we used basic Flask routes like  `@app.route()` to create endpoints. Flask-RESTful makes this even easier by letting you organize your API using classes and methods, which is especially helpful for bigger projects 

#### Here's how we can create an API with Flask-RESTful: 
- The first step is installing Flask-RESTful:  `pip install flask-restful ` 
- **Creating an API with Flask-RESTful:** Instead of using `@app.route()` for each endpoint, Flask-RESTful lets you create **resources** and define how they handle HTTP methods(GET, POST, PUT, DELETE). Let's see ane example
.

```python
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 

app = Flask(__name__)
api = Api(app) #Use Flask-RESTful's Api 

# Toy collection 
toys = [
    {"id": 1, "name": "Toy Car", "color": "Red"},
    {"id": 2, "name": "Toy Robot", "color": "Blue"}
]

# Define a Resource for Toy 
class ToyResource(Resource): 
    def get(self): 
        return jsonify({"toys": toys}) 
    
    def post(self): 
        new_toy = request.get_json() 
        new_toy["id"] = len(toys) + 1 
        toys.append(new_toy) 
        return jsonify(new_toy), 201 

#Add the resource to the API 
api.add_resource(ToyResource, '/toys')  

if __name__ == '__main__':
    app.run(debug=True)


```

What changed here? 
- `Resource` Class: Instead of manually writing routes and functions, we created a class called  `ToyResource`. This class has methods like `get()`(for GET Request) and  `post()` (for POST requests)
- `api.add_resource()`: We use this to tell Flask-RESTful to add our `ToyResource` class and associate it with `/toys` endpoint 

- Now, our API can handle both GET and POST requests with much cleaner code! 

#### Extending the API with PUT and DELETE 
Let's extend the example to include PUT and DELETE for updating and removing toys. 



```python
class ToyResource(Resource): 
    def get(self): 
        return jsonify({"toys": toys})
    
    def post(self): 
        new_toy = request.get_json() 
        new_toy["id"] = len(toys) + 1 
        toys.append(new_toy)
        return jsonify(new_toy), 201 
    

class ToyItemResource(Resource): 
    def put(self, toy_id): 
        toy = next((t for t in toys if t['id'] == toy_id), None)
        if toy is None: 
            return {"message": "Toy not found"}, 404 

        updated_data = request.jsoin() 
        toy.update(updated_data) 
        return jsonify(toy), 200 

    def delete(self, toy_id): 
        toy = next((t for t in toys if t['id'] == toy_id), None) 
        if toy is None: 
            return {"message": "Toy not found"}, 404 
        
        toys.remove(toy)
        return {"message": "Toy deleted"}, 204 


# Adding resources to handle specific toy items
api.add_resource(ToyResource, '/toys') 
api.add_resource(ToyItemResource, '/toys/<int:toy_id>')
```

##### What's New? 
- **ToyItemResource**: This handles specific toy items (e.g `/toys/1` to update or delete toy with ID 1) 
- **PUT and DELETE**: The `put()` method is used to update a toy, and `delete()` removes a toy based on its ID 

- Now you can: 
    - `GET` all toys: `GET /toys`
    - `POST` a new toy: `POST /toys`
    - `PUT`(update) a toy by ID: `PUT /toys/1` 
    - `DELETE` a toy by ID: `DELETE /toys/1` 

##### Connecting to Database with Flask-SQLAlchemy
- So far, we've been storing our toy **in memory**, which means they disappear when you restart the server. To make your API more useful, you'll want to store data permanently using a **database** 
- We can use **Flask-SQLAlchemy** which is an extension that helps us connect our databases like PostgreSQL or SQLite. 
  
1. **Install Flask-sqlalchemy**
   


```python
pip install flask-sqlalchemy
```

2. **Setting Up a Database**: Let's set up an SQLite database( which is easy to use) to store our toys 


```python
from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toys.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Toy model (database table)
class Toy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)

# Create the database and table
with app.app_context():
    db.create_all()

# Define the Toy Resource (GET, POST)
class ToyResource(Resource):
    def get(self):
        toys = Toy.query.all()  # Fetch all toys from the database
        return [{"id": toy.id, "name": toy.name, "color": toy.color} for toy in toys], 200

    def post(self):
        data = request.get_json()
        new_toy = Toy(name=data['name'], color=data['color'])
        db.session.add(new_toy)
        db.session.commit()
        return {"id": new_toy.id, "name": new_toy.name, "color": new_toy.color}, 201

# Define ToyItem Resource (GET, PUT, DELETE by ID)
class ToyItemResource(Resource):
    def get(self, toy_id):
        toy = Toy.query.get(toy_id)
        if not toy:
            return {"message": "Toy not found"}, 404
        return {"id": toy.id, "name": toy.name, "color": toy.color}, 200

    def put(self, toy_id):
        toy = Toy.query.get(toy_id)
        if not toy:
            return {"message": "Toy not found"}, 404

        data = request.get_json()
        toy.name = data['name']
        toy.color = data['color']
        db.session.commit()
        return {"id": toy.id, "name": toy.name, "color": toy.color}, 200

    def delete(self, toy_id):
        toy = Toy.query.get(toy_id)
        if not toy:
            return {"message": "Toy not found"}, 404

        db.session.delete(toy)
        db.session.commit()
        return {"message": "Toy deleted"}, 204

# Add Resources to API
api.add_resource(ToyResource, '/toys')  # For GET and POST requests on all toys
api.add_resource(ToyItemResource, '/toys/<int:toy_id>')  # For GET, PUT, DELETE by toy ID

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

```

##### What's Happening Here?  
1. Flask-SQLAlchemy: 
   1. The `Toy` model represents a table in the SQLite database with `id`, `name`, `color` columns 
   2. We initialize the database using `db.create_all()` inside the application context to ensure the table is created if it doesn't already exist. 
2. `Flask-RESTful Resources`: 
      1. `ToyResource`: Handles `GET` requests to retrieve all toys and `POST` requests to add new toys.  
      2. `ToyItemResource`: Handles `GET`, `PUT`, and `DELETE` requests for individual toys, identified by their `toy_id`


   

#### Testing the API
You can test the API by making the following HTTP requests. 
1. `GET /toys`(Retrieve all toys): 


```python
curl http://127.0.0.1:5000/toys
```

2.  `POST /toys`(Add a new toy): 


```python
curl -X POST -H "Content-Type: application/json" -d '{"name": "Toy Train", "color": "Green"}' http://127.0.0.1:5000/toys

{
    "id": 1,
    "name": "Toy Train",
    "color": "Blue"
}
```

3. `GET` /toys/1 (Retrieve a specific toy by ID): 


```python
curl http://127.0.0.1:5000/toys/1

{
    "id": 1,
    "name": "Toy Train",
    "color": "Blue"
}
```

4. `PUT` /toys/1 (Update a toy by ID): 


```python
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Toy", "color": "Blue"}' http://127.0.0.1:5000/toys/1
{
    "id": 1,
    "name": "Updated Toy",
    "color": "Blue"
}
```

5. `DELETE` /toys/1(Delete a toy by ID)


```python
curl -X DELETE http://127.0.0.1:5000/toys/1    
```


```python
curl http://localhost:5000/toys
[]
```
