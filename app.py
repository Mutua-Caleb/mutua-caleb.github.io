
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
    toy.update(updated_data) #Update the toy with the new deails 
    return jsonify(toy), 200 #Return the updated toy with status 200 (OK)

#API endpoint to delete a toy (DELETE method)
@app.route('/toys/<int:toy_id>', methods=['DELETE']) 
def delete_toy(toy_id): 
    toy = next((t for t in toys if t['id'] == toy_id), None)
    if toy is None: 
        return jsonify({'message': 'Toy not found'}), 404 # Return 404 if toy doesn't exist

    toys.remove(toy) #Remove the toy from the collection 
    return jsonify({'message': 'Toy deleted'}), 204 #Return 204 No content (success)

    


if __name__ == '__main__':
    app.run(debug=True)
