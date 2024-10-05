import json

class DataHandler:
    def __init__(self, transcripts_path):
        self.transcripts_path = transcripts_path

    def load_transcripts(self):
        """
        Load all transcripts from the specified directory and concatenate them into a single string.
        """
        try:
            transcripts = ""
            for filename in os.listdir(transcript_dir):
                if filename.endswith(".txt"):
                    with open(
                        os.path.join(transcript_dir, filename), "r", encoding="utf-8"
                    ) as file:
                        transcripts += file.read() + " "
            print("Completed -- chatbot_model.py -- load_transcripts")
            return transcripts.strip()
        except Exception as e:
            print(f"Error loading transcripts: {e}")
            return ""

    def preprocess_transcripts(self, transcripts):
        # Preprocess the transcripts (cleaning, segmenting, etc.)
        # Implement your preprocessing logic here
        return transcripts
