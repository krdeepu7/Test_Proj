import os
from flask import Flask, request, render_template, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.test
collecion = db['flask-tutorial']

app = Flask(__name__)


@app.route('/submit', methods = ["POST"])
def submit():
    form_data= dict(request.json)

    collecion.insert_one(form_data)
    return "success"

@app.route('/view')
def view():

    data = collecion.find()
    data = list(data)

    for item in data:
        print(item)
        del item['_id']
    
    data ={
        'data':data
    }

    return jsonify(data)




if __name__ == '__main__':

    app.run(host='0.0.0.0',port = 9000, debug=True)

