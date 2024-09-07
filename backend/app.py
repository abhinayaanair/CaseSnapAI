from flask import Flask, request, jsonify
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
from PIL import Image, ImageDraw, ImageFont
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from waitress import serve

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

# Load NLTK punkt tokenizer
nltk_data_dir = os.getenv('NLTK_DATA', '/opt/render/nltk_data')
nltk.data.path.append(nltk_data_dir)
try:
    nltk.download('punkt', download_dir=nltk_data_dir)
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

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
            line_width, _ = draw.textsize(test_line, font=font)

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
