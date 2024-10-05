from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from src.chatbot import Chatbot

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the chatbot
chatbot = Chatbot()


@app.route("/")
def home():
    return (
        "Welcome to the Usama's Podcast Chatbot! Ask me questions about the podcasts."
    )


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    print(f"User input: {user_input}")  # Log user input

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = chatbot.get_response(user_input)
        print(f"Chatbot response: {response}")  # Log chatbot response

        return jsonify(
            {
                "user_input": user_input,
                "response": response.get("answer", "No response"),
                "sentiment": response.get("sentiment", "Neutral"),
                "speaker": response.get("speaker", "Unknown"),
                "source_link": response.get("source_link", "#"),
            }
        )
    except Exception as e:
        print(f"Error getting chatbot response: {e}")  # Log any exceptions
        return jsonify({"error": "Error processing the request."}), 500


if __name__ == "__main__":
    app.run(debug=True)
