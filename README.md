# CaseSnap AI

**CaseSnap AI** is an AI-driven research engine designed to assist with legal analysis, focusing on commercial court cases. It leverages machine learning models to process legal documents, identify legal intents, and facilitate intelligent conversations that help in gathering key case information. The chatbot can also generate chat logs in PDF format for future reference.

## Features

- **Legal Intent Detection**: The AI identifies various legal intents from user queries, such as breach of contract, arbitration, or intellectual property issues.
- **Intelligent Questioning**: Based on the detected legal issues, the chatbot asks relevant follow-up questions to gather more details about the case.
- **Chat Log PDF Generation**: At the end of a conversation, users can generate a PDF containing the full chat log, with questions highlighted in bold.
- **Commercial Court Focus**: Specially trained to handle data related to commercial court cases, making it a valuable tool for legal professionals.
- **Flask Backend**: The project is powered by a Flask backend that handles the chatbot responses, chat log generation, and PDF export functionality.
- **React Frontend**: A user-friendly React-based frontend interface for interacting with the chatbot and accessing legal resources.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.9+
- Flask 3.0.3+
- Node.js 14+
- MongoDB (for storing chat logs or user data)
- TensorFlow (for AI model training)
- SpaCy (for NLP preprocessing)
- Bokeh (if you're using data visualization)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/casesnap-ai.git
   cd casesnap-ai


#  Set Up the backend

cd backend
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


pip install -r requirements.txt

# Set up the frontend:

cd ../frontend
npm install


# .env
FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=your-mongodb-uri
SECRET_KEY=your-secret-key

# Start the backend server

cd backend
flask run



# Start the frontend server

cd frontend
npm start


## project structure

├── backend                 # Flask backend for handling requests
│   ├── app.py              # Main Flask application
│   ├── models              # AI model and related code
│   ├── routes              # API routes for chatbot and PDF generation
│   ├── static              # Static files such as PDFs
│   └── templates           # HTML templates for PDF rendering
├── frontend                # React frontend for user interaction
│   ├── public              # Public assets
│   ├── src                 # Main React components
│   └── styles              # CSS stylesheets
└── README.md
