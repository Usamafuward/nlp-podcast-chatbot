Podcast Chatbot

This project is a natural language processing (NLP) chatbot designed to provide conversational experiences based on podcast transcripts. The chatbot can answer questions, attribute responses to the correct speakers, analyze sentiment and tone, and provide links to relevant YouTube video segments.

Setup Instructions

1. Setting Up the Python Backend Environment

Requirements:
Python 3.8+

pip (Python package installer)

Node.js and npm (for the frontend)

Step 1: Clone the Repository

git clone https://github.com/Usamafuward/nlp-podcast-chatbot.git

for backend
cd podcast-chatbot

for frontend
cd podcast-chatbot-frontend
npm start

Step 2: Set Up a Virtual Environment

python -m venv venv

venv\Scripts\activate

Once the virtual environment is activated, install the necessary Python dependencies:

pip install -r requirements.txt

Step 4: Run the Backend

python app.py

This will start the Flask backend, which will serve as the API for the chatbot's functionality.
