# app.py
import streamlit as st
import ollama

st.set_page_config(page_title="DeepSeek R1 1.5B Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 DeepSeek-R1 1.5B Chatbot (Ollama)")

# ---------------------------
# Initialize session state
# ---------------------------
if "conversations" not in st.session_state:
    st.session_state.conversations = {
        "Chat 1": [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
    }
if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Chat 1"

# ---------------------------
# Sidebar - chat history
# ---------------------------
with st.sidebar:
    st.header("📂 Chats")

    # Button for new chat
    if st.button("➕ New Chat"):
        new_name = f"Chat {len(st.session_state.conversations)+1}"
        st.session_state.conversations[new_name] = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
        st.session_state.active_chat = new_name
        st.rerun()

    # Show list of chats
    for name in st.session_state.conversations.keys():
        if st.button(name):
            st.session_state.active_chat = name
            st.rerun()

    # Clear chat button
    if st.button("🗑️ Clear Current Chat"):
        st.session_state.conversations[st.session_state.active_chat] = [
            {"role": "system", "content": "You are a helpful AI assistant."}
        ]
        st.rerun()

# ---------------------------
# Main chat window
# ---------------------------
chat_name = st.session_state.active_chat
messages = st.session_state.conversations[chat_name]

st.subheader(f"💬 {chat_name}")

# Show past messages
for msg in messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Input box
if prompt := st.chat_input("Type your message..."):
    # Save user message
    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking..."):
        try:
            response = ollama.chat(
                model="deepseek-r1:1.5b",
                messages=messages
            )
            reply = response["message"]["content"]

            # Save assistant reply
            messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")
