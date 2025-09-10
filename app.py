import streamlit as st
import ollama

st.set_page_config(page_title="DeepSeek Chatbot", page_icon="🤖", layout="wide")
st.title("💬 DeepSeek Chatbot (Ollama)")

# --- Initialize session state ---
if "chats" not in st.session_state:
    st.session_state.chats = []  # list of chat sessions (each is a list of messages)
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

# --- Sidebar ---
with st.sidebar:
    st.header("💬 Chat History")

    # 🔍 Search bar
    search_query = st.text_input("Search chats")

    # ➕ New Chat button
    if st.button("➕ New Chat", use_container_width=True):
        if len(st.session_state.chats) >= 15:
            st.session_state.chats.pop(0)  # remove oldest
        st.session_state.current_chat = len(st.session_state.chats)
        st.session_state.chats.append([])

    st.markdown("---")

    # Show chat titles
    for i, chat in enumerate(st.session_state.chats):
        if not chat:
            continue

        # Title = first user message
        title = next((m["content"] for m in chat if m["role"] == "user"), "Untitled Chat")

        # Apply search filter
        if search_query and search_query.lower() not in title.lower():
            continue

        # Truncate for sidebar
        short_title = title[:25] + ("..." if len(title) > 25 else "")

        # Select chat button
        if st.button(short_title, key=f"chat_{i}", help=title, use_container_width=True):
            st.session_state.current_chat = i

# --- Main Chat Area ---
if st.session_state.current_chat is not None:
    chat = st.session_state.chats[st.session_state.current_chat]

    # Display messages
    for msg in chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        # Save user message
        chat.append({"role": "user", "content": prompt})

        # Get response from DeepSeek (via Ollama)
        response = ollama.chat(
            model="deepseek-coder:1.3b",
            messages=chat
        )
        reply = response["message"]["content"]

        # Save assistant reply
        chat.append({"role": "assistant", "content": reply})

        # Refresh UI
        st.rerun()
else:
    st.info("👉 Start a new chat from the sidebar.")
