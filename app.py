from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# MONOCLE_MONOGO_URL=mongodb+srv://yash-shrestha:kC029pZzG7QmuKUU@cluster0.14dqgtr.mongodb.net/?authMechanism=DEFAULT
# MONOCLE_MONOGO_DB=prod

client = MongoClient('mongodb+srv://yash-shrestha:kC029pZzG7QmuKUU@cluster0.14dqgtr.mongodb.net/?authMechanism=DEFAULT')
db = client["prod"]
collection = db["extension"]

@app.route('/')
def index():
    return "Welcome to the Flask MongoDB app!"

@app.route('/add', methods=['POST'])
def add_record():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    result = collection.insert_one({
        'title': data.get('titleElement'),
        'prices': data.get('price'),
        'descriptions': data.get('descriptionElement'),
        'images': data.get('imageElement'),
        'url': data.get('urlElement')
    })
    return jsonify({"result": str(result.inserted_id)})

@app.route('/showAll', methods=['GET'])
def show_all():
    records = list(collection.find())
    for record in records:
        record['_id'] = str(record['_id'])
    return jsonify(records) 

if __name__ == '__main__':
    app.run(debug=True)