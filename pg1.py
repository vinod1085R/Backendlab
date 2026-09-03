from flask import Flask, jsonify 
app = Flask(__name__) 
users = [ 
    { 
        "id": 1, 
        "name": "Modi", 
        "email": "Modi@example.com", 
        "age": 25 
    }, 
    { 
        "id": 2, 
        "name": "Nirmala", 
        "email": "nirmala@example.com", 
        "age": 25 
    }, 
    { 
        "id": 3, 
        "name": "Seetha", 
        "email": "seetha@example.com", 
        "age": 28 
    }, 
    { 
        "id": 4, 
        "name": "David", 
        "email": "david@example.com", 
        "age": 24 
    }, 
    { 
        "id": 5, 
        "name": "Geetha", 
        "email": "geetha@example.com", 
        "age": 21 
    } 
] 
# Endpoint to return all users 
@app.route('/users', methods=['GET']) 
def get_users(): 
    return jsonify({ 
            "success": True, 
            "message": "Users retrieved successfully.", 
            "count": len(users), 
            "data": users 
        }), 200 
 
# Endpoint to return a specific user by ID 
@app.route('/users/<int:id>', methods=['GET']) 
def get_user(id): 
    for user in users: 
        if user["id"] == id: 
            return jsonify({ 
            "success": True, 
            "message": "User retrieved successfully.", 
            "data": user 
        }), 200 
    return jsonify({"message": "User not found"}), 404 
 
if __name__ == '__main__': 
    app.run(debug=True) 