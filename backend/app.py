from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np
import json
import pickle
import spacy
from tensorflow.keras.models import load_model
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from waitress import serve
import requests

# Load environment variables from .env file
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('CLOUD_API_KEY'),
    api_secret=os.getenv('CLOUD_API_SECRET')
)

app = Flask(__name__)
CORS(app)

# MongoDB setup using the environment variable
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.get_database('CaseSnap')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Load the model and data
model = load_model('chatbot_model3.h5')
with open('words.pkl', 'rb') as file:
    words = pickle.load(file)
with open('classes.pkl', 'rb') as file:
    classes = pickle.load(file)

# Load intents
with open('intents.json') as file:
    data = json.load(file)

ignore_letters = ['!', '?', ',', '.']

# In-memory chat log storage
chat_log = []

# Function to preprocess the input text
def preprocess_input(text):
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if token.text not in ignore_letters]
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

# Function to wrap text and save as an image
def save_to_image(chat_log):
    image_width = 800
    image_height = 1200
    image = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    y_position = 10
    max_y_position = image_height - 10  # Prevent text from going off the bottom of the image
    line_height = 20  # Height of each line of text

    def wrap_text(text, max_width, font):
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        lines = []
        words = text.split()
        current_line = ''

        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = bbox[2] - bbox[0]  # bbox gives (left, top, right, bottom)

            if line_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    for entry in chat_log:
        question_text = f"User: {entry['question']}"
        response_text = f"Bot: {entry['response']}"

        # Wrap and draw the question text
        question_lines = wrap_text(question_text, image_width - 20, font)
        for line in question_lines:
            draw.text((10, y_position), line, fill='black', font=font)
            y_position += line_height
        y_position += line_height  # Add extra space after each entry

        # Wrap and draw the response text
        response_lines = wrap_text(response_text, image_width - 20, font)
        for line in response_lines:
            draw.text((10, y_position), line, fill='blue', font=font)
            y_position += line_height
        y_position += line_height * 2  # Add extra space after each entry

        # Check if we need to increase image size
        if y_position > max_y_position:
            # Resize the image if needed
            new_image_height = image_height + 500
            new_image = Image.new('RGB', (image_width, new_image_height), color='white')
            new_image.paste(image, (0, 0))
            image = new_image
            draw = ImageDraw.Draw(image)
            max_y_position = new_image_height - 10

    # Save the image
    file_path = 'casesnap_chat_log.jpg'
    image.save(file_path)

    # Upload to Cloudinary and get the direct download URL
    response = cloudinary.uploader.upload(file_path, resource_type='image')
    os.remove(file_path)  # Remove the local file after uploading
    return response['secure_url']

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
            return jsonify({"message": "User already exists, try logging in!"}), 400

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


API_KEY = os.getenv('GOOGLE_API_KEY')  # Add your API Key in .env
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')  # Add your Custom Search Engine ID in .env

def google_search_api(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': 10,  # Number of search results to return
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        
        search_data = response.json()
        search_results = search_data.get('items', [])
        
        # Filter the results based on user criteria (example filters)
        filtered_results = filter_lawyers(search_results)
        
        return filtered_results
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return None

def filter_lawyers(search_results):
    filtered = []
    
    # Simple filtering based on keywords for now, could expand to more complex logic
    for result in search_results:
        title = result.get('title', '').lower()
        snippet = result.get('snippet', '').lower()

        # Example criteria: Search for lawyers with specific specializations and price range
        if 'lawyer' in title and 'contract' in snippet and '20000' in snippet:
            filtered.append({
                'title': result['title'],
                'link': result['link'],
                'snippet': result['snippet']
            })
    
    return filtered

@app.route('/search', methods=['POST'])
def search_lawyers():
    user_input = request.json.get('message')

    # Use Google Search API to search for lawyers
    search_results = google_search_api(user_input)

    if search_results:
        return jsonify({'results': search_results})
    else:
        return jsonify({'message': 'No lawyers found based on your input'}), 404


@app.route('/chat', methods=['POST'])
def chat():
    global chat_log
    user_input = request.json.get('message')

    if user_input.lower() == 'end':
        image_url = save_to_image(chat_log)
        chat_log = []  # Clear chat log after saving
        return jsonify({'download_link': image_url})
    
    predicted_tag = predict_class(user_input)
    response = get_response(predicted_tag)

    # Append chat entry to chat_log
    chat_log.append({'question': user_input, 'response': response})

    return jsonify({'response': response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's dynamic port
    serve(app, host='0.0.0.0', port=port)  # Use waitress for production
