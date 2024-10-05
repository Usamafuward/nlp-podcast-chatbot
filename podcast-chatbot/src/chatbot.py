from models.chatbot_model import Chatbot

class PodcastChatbot:
    def __init__(self):
        self.chatbot_model = Chatbot()

    def get_response(self, user_input):
        # Get response from the chatbot model
        response = self.chatbot_model.get_response(user_input)

        print("Completed -- chatbot.py")

        return {
            "text": response["answer"],
            "speaker": response["speaker"],
            "sentiment": response["sentiment"],
            "source_link": response["source_link"],
        }
