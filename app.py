from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Retrieve environment variables
mongo_url = os.getenv('MONGO_URL')
mongo_db = os.getenv('MONGO_DB')
mongo_collection = os.getenv('MONGO_COLLECTION')

# Connect to MongoDB
client = MongoClient(mongo_url)
db = client[mongo_db]
collection = db[mongo_collection]

@app.route('/')
def index():
    # Health check endpoint
    return jsonify({"status": "API is running", "db_status": str(client.server_info())})

@app.route('/add', methods=['POST'])
def add_record():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        if isinstance(data, list) and data:
            result =  collection.insert_many(data)
            return jsonify({"result": len(result.inserted_ids)})
        else:
            result = collection.insert_one({
                'title': data.get('titleElement'),
                'prices': data.get('price'),
                'descriptions': data.get('descriptionElement'),
                'images': data.get('imageElement'),
                'url': data.get('urlElement'),
                'category': data.get('categoryElement')
            })
            return jsonify({"result": str(result.inserted_id)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/showAll', methods=['GET'])
def show_all():
    try:
        records = list(collection.find())
        for record in records:
            record['_id'] = str(record['_id'])
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
