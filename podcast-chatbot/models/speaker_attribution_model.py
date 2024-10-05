import re
class SpeakerAttribution:
    def __init__(self, transcripts):
        self.transcripts = transcripts  # Load transcripts data
        self.speaker_pattern = re.compile(
            r"([A-Za-z\s]+)\n\(\d{2}:\d{2}:\d{2}\)"
        )  # Regex to match speaker names and timestamps
        self.speakers = (
            self.extract_speakers()
        )  # Extract speakers during initialization

    def extract_speakers(self):
        """
        Extract speaker names and corresponding segments from the transcript.
        """
        speakers = {}
        segments = self.speaker_pattern.split(
            self.transcripts
        )  # Split by speaker patterns

        for i in range(1, len(segments), 2):
            speaker_name = segments[i].strip()
            speaker_text = segments[i + 1].strip()

            if speaker_name in speakers:
                speakers[speaker_name] += " " + speaker_text
            else:
                speakers[speaker_name] = speaker_text

        return speakers

    def attribute_speaker(self, response):
        """
        Match the response text to the correct speaker using keyword matching or more advanced techniques.
        """
        speaker = self.find_speaker(response)
        return speaker

    def find_speaker(self, response):
        """
        Match the response text with a speaker by searching for overlapping phrases or keywords.
        """
        response = response.lower()

        for speaker, text in self.speakers.items():
            if response in text.lower():
                return speaker

        return "Unknown Speaker"
