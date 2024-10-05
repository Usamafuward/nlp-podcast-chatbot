class MemoryManager:
    def __init__(self, memory_limit=5):
        """
        Initialize memory with an optional memory limit (default 5 interactions).
        """
        self.memory = []
        self.memory_limit = memory_limit

    def add_to_memory(self, user_input, bot_response):
        """
        Store the user's input and the bot's response in memory.
        """
        # Append the user input and bot response as a dictionary
        self.memory.append({"user_input": user_input, "bot_response": bot_response})

        # If the memory exceeds the limit, remove the oldest interaction
        if len(self.memory) > self.memory_limit:
            self.memory.pop(0)

    def get_memory(self):
        """
        Retrieve the last few interactions stored in memory for context.
        """
        return self.memory

    def clear_memory(self):
        """
        Clear the memory, resetting the conversation history.
        """
        self.memory = []

    def get_context_from_memory(self):
        """
        Retrieve user inputs and bot responses as a concatenated context string.
        This can be fed back into the chatbot for better understanding of the conversation.
        """
        context = ""
        for interaction in self.memory:
            context += f"User: {interaction['user_input']}\nBot: {interaction['bot_response']}\n"
        return context
