import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
from src.memory_manager import MemoryManager
from models.sentiment_analysis_model import SentimentAnalysis
from models.speaker_attribution_model import SpeakerAttribution
import networkx as nx  # For graph-based RAG


class Chatbot:
    def __init__(self, transcript_dir="data/transcript/"):
        """
        Initialize the chatbot with question-answering, speaker attribution, sentiment analysis models,
        and memory management.
        """
        self.qa_pipeline = pipeline(
            "question-answering", model="distilbert-base-cased-distilled-squad"
        )

        self.transcripts_str = self.load_transcripts_str(transcript_dir)

        # Load all available transcripts and extract YouTube links
        self.transcripts, self.youtube_links = self.load_transcripts(transcript_dir)

        # Extract timestamps and map them to text segments
        self.timestamp_maps = self.extract_timestamps(self.transcripts)

        # Build the RAG graph
        self.conversation_graph = nx.Graph()
        self.build_conversation_graph(self.timestamp_maps)

        # Initialize Speaker Attribution and Sentiment Analysis
        self.speaker_attribution = SpeakerAttribution(self.transcripts_str)
        self.sentiment_analysis = SentimentAnalysis()
        self.memory_manager = MemoryManager(memory_limit=5)

    def build_conversation_graph(self, timestamp_maps):
        """
        Build a graph where each node represents a conversation chunk and its timestamp.
        """
        previous_timestamp = None
        for timestamp_map in timestamp_maps:
            for timestamp, conversation in timestamp_map["timestamps"].items():
                # Add a node for each conversation chunk and its timestamp
                self.conversation_graph.add_node(timestamp, conversation=conversation)

                # Connect nodes sequentially based on timestamps to simulate the flow of conversation
                if previous_timestamp:
                    self.conversation_graph.add_edge(previous_timestamp, timestamp)
                previous_timestamp = timestamp

    def get_response(self, question):
        """
        Process the user's question, find the relevant transcript context, generate a response using the QA model,
        and store the conversation in memory.
        """
        relevant_context, timestamp, youtube_link = (
            self.find_relevant_context_and_timestamp(question)
        )

        if not relevant_context:
            return {
                "answer": "Sorry, I couldn't find relevant information.",
                "score": 0.0,
                "speaker": "Unknown Speaker",
                "sentiment": "neutral",
                "source_link": None,
            }

        result = self.qa_pipeline(question=question, context=relevant_context)

        # Speaker Attribution
        speaker = self.speaker_attribution.attribute_speaker(result["answer"])

        # Sentiment Analysis
        sentiment = self.sentiment_analysis.analyze_sentiment(result["answer"])

        # Get source link
        source_link = self.get_source_link(youtube_link, timestamp)

        bot_response = {
            "answer": result.get("answer", "No answer found."),
            "score": result.get("score", 0.0),
            "speaker": speaker,
            "sentiment": sentiment["sentiment"],
            "source_link": source_link,
        }

        # Store conversation in memory
        self.memory_manager.add_to_memory(question, bot_response["answer"])

        return bot_response

    def find_relevant_context_and_timestamp(self, question):
        """
        Use TF-IDF to find the most relevant chunk from the transcript based on the user's question.
        Also returns the associated timestamp and the corresponding YouTube link.
        """
        best_chunk = None
        best_timestamp = None
        best_youtube_link = None
        best_similarity = 0

        # Iterate through all transcripts
        for transcript, youtube_link in zip(self.timestamp_maps, self.youtube_links):
            chunks = list(transcript["timestamps"].values())
            corpus = [question] + chunks

            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(corpus)

            cosine_similarities = cosine_similarity(
                tfidf_matrix[0:1], tfidf_matrix[1:]
            ).flatten()

            most_relevant_index = cosine_similarities.argmax()
            similarity = cosine_similarities[most_relevant_index]

            if similarity > best_similarity:
                best_similarity = similarity
                best_chunk = chunks[most_relevant_index]
                best_timestamp = list(transcript["timestamps"].keys())[
                    most_relevant_index
                ]
                best_youtube_link = youtube_link

        return best_chunk, best_timestamp, best_youtube_link

    def get_source_link(self, youtube_link, timestamp):
        """
        Return the source link using the extracted YouTube link from the transcript file and appending the timestamp.
        """
        return f"{youtube_link}&t={self.convert_timestamp_to_seconds(timestamp)}"

    def load_transcripts_str(self, transcript_dir):
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
            return transcripts.strip()
        except Exception as e:
            print(f"Error loading transcripts: {e}")
            return ""

    def load_transcripts(self, transcript_dir):
        """
        Load all transcripts from the specified directory and extract their YouTube links.
        Returns a list of transcript texts and their corresponding YouTube links.
        """
        transcripts = []
        youtube_links = []
        try:
            for filename in os.listdir(transcript_dir):
                if filename.endswith(".txt"):
                    with open(
                        os.path.join(transcript_dir, filename), "r", encoding="utf-8"
                    ) as file:
                        lines = file.readlines()
                        youtube_link = lines[0].strip()  # First row is the YouTube link
                        transcript = " ".join(lines[1:]).strip()  # Skip the first line
                        transcripts.append(transcript)
                        youtube_links.append(youtube_link)
            return transcripts, youtube_links
        except Exception as e:
            print(f"Error loading transcripts: {e}")
            return [], []

    def extract_timestamps(self, transcripts):
        """
        Extract timestamps and corresponding text chunks from the transcript.
        Returns a list of dictionaries with timestamps and corresponding text for each transcript.
        """
        timestamp_maps = []
        for transcript in transcripts:
            timestamp_pattern = r"\((\d{2}:\d{2}:\d{2})\)"
            timestamps = re.findall(timestamp_pattern, transcript)
            text_chunks = re.split(timestamp_pattern, transcript)

            timestamp_map = {}
            for i in range(1, len(text_chunks), 2):
                timestamp = text_chunks[i]
                text = text_chunks[i + 1].strip()
                timestamp_map[timestamp] = text

            timestamp_maps.append({"timestamps": timestamp_map})

        return timestamp_maps

    def convert_timestamp_to_seconds(self, timestamp):
        """
        Convert a timestamp (hh:mm:ss) into seconds to append to YouTube links.
        """
        h, m, s = map(int, timestamp.split(":"))
        return h * 3600 + m * 60 + s
