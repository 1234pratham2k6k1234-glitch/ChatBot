import streamlit as st
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("Your Personal Chatbot (Groq)")


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

user_input = st.chat_input("Type your message here...")

# 🔥 model fallback list
MODELS = [
    "llama-3.1-8b-instant",
    "openai/gpt-oss-20b",
    "groq/compound"
]

def get_response(messages):
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            continue
    return "⚠️ All models failed."

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ai_message = get_response(st.session_state.messages)
            st.markdown(ai_message)

            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_message
            })