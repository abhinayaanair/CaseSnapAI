from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from fpdf import FPDF
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB setup using the environment variable
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('CaseSnap')

# Load the model and data
model = load_model('chatbot_model3.h5')
with open('words.pkl', 'rb') as file:
    words = pickle.load(file)
with open('classes.pkl', 'rb') as file:
    classes = pickle.load(file)

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents
with open('intents.json') as file:
    data = json.load(file)

ignore_letters = ['!', '?', ',', '.']

# In-memory chat log storage
chat_log = []

# Function to preprocess the input text
def preprocess_input(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token not in ignore_letters]
    return tokens

# Function to create a bag of words
def bow(tokens, words):
    bag = [0] * len(words)
    for token in tokens:
        for i, word in enumerate(words):
            if word == token:
                bag[i] = 1
    return np.array(bag)

# Function to predict the class
def predict_class(text):
    tokens = preprocess_input(text)
    bow_array = bow(tokens, words)
    prediction = model.predict(np.array([bow_array]))[0]
    predicted_class = classes[np.argmax(prediction)]
    return predicted_class

# Function to get a response
def get_response(tag):
    for intent in data['intents']:
        if intent['tag'] == tag:
            return np.random.choice(intent['responses'])
    return "Sorry, I don't understand that."

# Function to save the chat log to a PDF
def save_to_pdf(chat_log):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    
    for entry in chat_log:
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 10, txt="User: " + entry['question'], ln=True, align='L')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt="Bot: " + entry['response'])
        pdf.ln(10)
    
    file_path = 'casesnap_chat_log.pdf'
    pdf.output(file_path)
    return file_path

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    try:
        user = db.users.find_one({'email': email})
        if user:
            return jsonify({"message": "User already exists try logging in!"}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        db.users.insert_one({'email': email, 'password': hashed_password})

        return jsonify({"message": "Signup successful"}), 201

    except errors.DuplicateKeyError as e:
        return jsonify({"message": f"Duplicate entry detected: {e}"}), 400
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    try:
        user = db.users.find_one({'email': email})
        if not user:
            return jsonify({"message": "Invalid email or password"}), 401

        if not check_password_hash(user['password'], password):
            return jsonify({"message": "Invalid email or password"}), 401

        return jsonify({"message": "Login successful"}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global chat_log
    user_input = request.json.get('message')

    if user_input.lower() == 'end':
        pdf_path = save_to_pdf(chat_log)
        chat_log = []  # Clear chat log after saving
        return jsonify({'download_link': f'/download/{pdf_path}'})
    
    predicted_tag = predict_class(user_input)
    response = get_response(predicted_tag)

    chat_log.append({'question': user_input, 'response': response})

    return jsonify({'response': response})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('.', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
