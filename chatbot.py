import os
import csv
from dataclasses import dataclass
from typing import Literal
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score
import streamlit as st
from datetime import datetime
from chatbot_model import chat_bot, X_test, y_test, clf


# Define message class to store chat history
@dataclass
class Message:
    origin: Literal["user", "bot"]
    content: str


# Load CSS for styling
def load_css():
    st.markdown(
        """
        <style>
            body {
                background-color: #1e1e1e;
                color: white;
            }
            .chat-container {
                max-height: 70vh;
                overflow-y: auto;
                padding-right: 15px;
                border: 1px solid white;
            }
            .user-message {
                text-align: right;
                margin-bottom: 10px;
            }
            .user-message .message-bubble {
                display: inline-block;
                background-color: #1e90ff;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            .bot-message {
                text-align: left;
                margin-bottom: 10px;
            }
            .bot-message .message-bubble {
                display: inline-block;
                background-color: #333333;
                color: white;
                padding: 10px;
                border-radius: 10px;
            }
            .input-container {
                display: flex;
                width: 100%;
                position: fixed;
                bottom: 0;
                left: 0;
                padding: 10px;
                background-color: #000000;
            }
            .input-box {
                flex: 1;
                padding: 10px;
                border-radius: 5px;
                background-color: #333333;
                color: white;
                border: none;
            }
            .input-box:focus {
                outline: none;
            }
            .submit-button {
                padding: 10px 20px;
                margin-left: 10px;
                background-color: #1e90ff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .submit-button:hover {
                background-color: #005ea6;
            }
            
            .sidebar-button {
                width: 100%; /* Ensure the button takes full width */
                padding: 10px;
                margin-bottom: 10px;
                text-align: center;
                background-color: #1e90ff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            .sidebar-button:hover {
                background-color: #005ea6;
            }
            .st-emotion-cache-jh76sn {
                width: 100% !important; /* Override default auto width */
            }

            .sidebar-button:active {
                background-color: #003f74;
            }
            .ask-button, .save-button {
                margin-top: 10px;
            }
            .column-container {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .column-item {
                margin-right: 10px;
            }
           .st-emotion-cache-129e8oq {
            margin: 27px -45px 0px -6px !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "current_view" not in st.session_state:
        st.session_state["current_view"] = "Chat"

def handle_chat_input():
    user_message = st.session_state.user_input.strip()
    if user_message:
        st.session_state.chat_history.append(
            Message("user", f"User: {user_message}")
        )
        bot_response = chat_bot(user_message)
        st.session_state.chat_history.append(
            Message("bot", f"Bot: {bot_response}")
        )
        st.session_state.user_input = ""

def save_chat_history():
    filename = "chat_log.csv"
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        if os.stat(filename).st_size == 0:
            csv_writer.writerow(["User", "Bot", "Timestamp"])

        for i in range(0, len(st.session_state.chat_history), 2):
            user_message = st.session_state.chat_history[i]
            bot_message = st.session_state.chat_history[i + 1] if i + 1 < len(st.session_state.chat_history) else None

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if bot_message:
                csv_writer.writerow([user_message.content, bot_message.content, timestamp])

def clear_chat_history():
    filename = "chat_log.csv"
    if os.path.exists(filename):
        os.remove(filename)
        st.success("Chat history cleared!")
    else:
        st.error("No chat history to clear.")

def display_chat_history():
    st.subheader("🕓 Chat History")
    if os.path.exists("chat_log.csv"):
        with open("chat_log.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)

            for row in reader:
                if len(row) == 3:
                    user_msg, bot_msg, timestamp = row
                    st.markdown(f"{user_msg}")
                    st.markdown(f"{bot_msg}")
                    st.markdown(f"Timestamp: {timestamp}")
                    st.markdown("---")
    else:
        st.info("No chat history found.")
    if st.button("Clear History"):
        clear_chat_history()

def sidebar_navigation():
    st.sidebar.title("Navigation")
    st.sidebar.markdown("---")

    if st.sidebar.button("📝 Chat", key="chat_btn"):
        st.session_state.current_view = "Chat"

    if st.sidebar.button("🕛 Chat History", key="history_btn"):
        st.session_state.current_view = "Chat History"

    if st.sidebar.button("📊 Model Evaluation", key="evaluation_btn"):
        st.session_state.current_view = "Model Evaluation"

    if st.sidebar.button("📝 About", key="about_btn"):
        st.session_state.current_view = "About"

def display_chat_view():
    st.title("🔮 IntelliChat AI Chatbot")
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            bubble_class = "user-message" if message.origin == "user" else "bot-message"
            st.markdown(
                f'<div class="{bubble_class}"><div class="message-bubble">{message.content}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
    col1, col2 = st.columns([6, 1])
    with col1:
        st.text_input(
            "Type your message here...",
            key="user_input",
            on_change=handle_chat_input,
            label_visibility="visible",
        )
    with col2:
        if st.button("Ask", key="ask_btn", help="Click to send your message"):
            handle_chat_input()

    if st.button("Save Chat History"):
        save_chat_history()
        st.success("Chat history saved!")

def display_model_evaluation_view():
    st.subheader("📊 Model Performance Evaluation")
    st.write(f"**Model Accuracy:** {accuracy_score(y_test, clf.predict(X_test)) * 100:.2f}%")

    # Calculate precision and recall (with zero_division=0)
    precision = precision_score(y_test, clf.predict(X_test), average='macro', zero_division=0)
    recall = recall_score(y_test, clf.predict(X_test), average='macro', zero_division=0)

    st.write(f"**Precision:** {precision * 100:.2f}%")
    st.write(f"**Recall:** {recall * 100:.2f}%")

    # Display classification report
    st.text(classification_report(y_test, clf.predict(X_test), zero_division=0))

def display_about_view():
  st.subheader("📝 About IntelliChat AI")
  st.write("""**IntelliChat AI Chatbot** is designed to assist users with travel-related queries using NLP and Machine Learning techniques.
  It processes natural language inputs and responds based on the pre-trained model's understanding of user intents.
  """)
  st.subheader("Key Features")
  st.write("""
  - **Natural Language Processing (NLP):** Understands and processes user inputs to determine intent.
  - **Interactive Interface:** Built using Streamlit for easy interaction.
  - **Machine Learning Model:** Utilizes a logistic regression classifier for intent classification.
  """)
  st.subheader("Future Enhancements")
  st.write("""- **Multi-language support:** Expand chatbot capabilities to handle queries in multiple languages.
  - **Emotion detection:** Improve the response by detecting user emotions through text analysis.
  - **Improved intent classification:** Explore advanced NLP techniques like transformers for better accuracy.
  """)


def main():
    initialize_session_state()
    load_css()
    sidebar_navigation()

    if st.session_state.current_view == "Chat":
        display_chat_view()
    elif st.session_state.current_view == "Chat History":
        display_chat_history()
    elif st.session_state.current_view == "Model Evaluation":
        display_model_evaluation_view()
    elif st.session_state.current_view == "About":
        display_about_view()


if __name__ == "__main__":
    main()

