import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", {
        message: input,
      });

      console.log("Server response:", response.data); // Log the response

      const {
        user_input,
        response: answer,
        sentiment,
        speaker,
        source_link,
      } = response.data;

      // Append both user input and chatbot response to chat history
      setChatHistory((prevHistory) => [
        ...prevHistory,
        { user: true, text: user_input },
        {
          user: false,
          text: answer,
          sentiment,
          speaker,
          source_link,
        },
      ]);

      setInput(""); // Clear input
    } catch (error) {
      console.error("Error sending message:", error); // Log the error
      alert(
        "Failed to get a response from chatbot. Check the server and try again."
      );
    }
  };

  return (
    <div className="App" style={styles.container}>
      <h1 style={styles.header}>Usama's Podcast Chatbot</h1>

      <div style={styles.chatBox}>
        {chatHistory.map((message, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: message.user ? "flex-end" : "flex-start",
              backgroundColor: message.user ? "#daf8cb" : "#f1f0f0",
            }}
          >
            <p>{message.text}</p>
            {!message.user && (
              <div style={styles.responseInfo}>
                <p>
                  <strong>Speaker:</strong> {message.speaker}
                </p>
                <p>
                  <strong>Sentiment:</strong> {message.sentiment}
                </p>
                <a
                  href={message.source_link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View Source
                </a>
              </div>
            )}
          </div>
        ))}
      </div>

      <div style={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)} // This should update the input state
          placeholder="Ask a question..."
          style={styles.input}
        />
        <button onClick={handleSendMessage} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    height: "100vh",
    padding: "20px",
    fontFamily: "Arial, sans-serif",
  },
  header: {
    fontSize: "24px",
    marginBottom: "20px",
  },
  chatBox: {
    display: "flex",
    flexDirection: "column",
    width: "100%",
    maxWidth: "600px",
    height: "400px",
    overflowY: "scroll",
    border: "1px solid #ccc",
    padding: "10px",
    borderRadius: "5px",
    backgroundColor: "#fafafa",
  },
  message: {
    padding: "10px",
    margin: "5px 0",
    borderRadius: "10px",
    maxWidth: "75%",
  },
  responseInfo: {
    marginTop: "5px",
    fontSize: "12px",
    color: "#555",
  },
  inputContainer: {
    display: "flex",
    width: "100%",
    maxWidth: "600px",
    marginTop: "10px",
  },
  input: {
    flexGrow: 1,
    padding: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "10px 20px",
    border: "none",
    borderRadius: "5px",
    marginLeft: "10px",
    backgroundColor: "#4caf50",
    color: "white",
    cursor: "pointer",
  },
};

export default App;
