import os
from dotenv import load_dotenv
import streamlit as st
import openai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="ChatBot!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",    # Page layout option
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize chat session in Streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to get a response from OpenAI's API
def get_openai_response(user_input, chat_history):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for entry in chat_history:
        messages.append({"role": entry["role"], "content": entry["content"]})
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Correct model name
        messages=messages,
        temperature=1,  # Corrected this from 1.0
        max_tokens=4095,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message["content"]

# Display the chatbot's title on the page
st.title("💭💭ChatBot")

# Display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask ChatBot...")
if user_prompt:
    # Add user's message to chat and display it
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to OpenAI and get the response
    openai_response = get_openai_response(user_prompt, st.session_state.chat_history)

    # Display OpenAI's response
    st.session_state.chat_history.append({"role": "assistant", "content": openai_response})
    with st.chat_message("assistant"):
        st.markdown(openai_response)
