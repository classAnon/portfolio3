from time import sleep
from flask import Flask, flash, jsonify, redirect, render_template, url_for, request
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("CONNECTION_STRING"))
db = client[os.getenv("DB_NAME")]

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/", methods=['POST'])   
def form_handler():

    name = request.form.get("clientName")
    email = request.form.get("clientEmail")
    message = request.form.get("clientMsg")

    client_data = {
		"Name": name,
		"Email": email,
		"Message": message
	}
    current_collection = db.contact_form_pf
    user = current_collection.find_one({"Message": client_data["Message"]}) and current_collection.find_one({"Email": client_data["Email"]})
    if not user:
        current_collection.insert_one(client_data)
        return redirect(url_for('home'))
    else:
        return jsonify({"msg": "Something went wrong. Could not send message"})

if __name__=='__main__':
    app.run(debug=True)