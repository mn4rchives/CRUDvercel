import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

# โหลด .env
load_dotenv()

# Flask setup
app = Flask(__name__)
CORS(app)

# MongoDB Atlas Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["flaskdb"]          # หรือเปลี่ยนชื่อ database
collection = db["users"]        # collection ชื่อ 'users'

# 👤 Create User
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# 📋 Read All Users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = [{**u, '_id': str(u['_id'])} for u in collection.find()]
    return jsonify(users)

# 🔍 Read One User by ID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = collection.find_one({'_id': ObjectId(id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user['_id'] = str(user['_id'])
    return jsonify(user)

# ✏️ Update User by ID
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User updated'})

# ❌ Delete User by ID
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'})

# 🏠 Test route
@app.route('/')
def home():
    return "MongoDB Flask CRUD API is running!"

# 🔃 Run the server
if __name__ == '__main__':
    app.run(debug=True)