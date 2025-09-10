import streamlit as st
from groq import Groq
from datetime import datetime

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="DeepSeek R1 Chatbot",
    layout="wide"
)

# ------------------------------
# Session State Initialization
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# Helper Functions
# ------------------------------
def append_message(role, content):
    """Append a message to the session state with timestamp."""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

def display_last_message():
    """Display the last user and bot messages in the sidebar."""
    if st.session_state.messages:
        user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
        bot_msgs = [m for m in st.session_state.messages if m["role"] == "assistant"]

        if user_msgs:
            last_user = user_msgs[-1]
            st.markdown(f"**You ({last_user['timestamp']}):** {last_user['content']}")
        if bot_msgs:
            last_bot = bot_msgs[-1]
            st.markdown(f"**Bot ({last_bot['timestamp']}):** {last_bot['content']}")
    else:
        st.info("No messages yet.")

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.title("Settings & Last Message")

    # API Key Input
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("[Get Groq API Key](https://console.groq.com/keys)")

    # Clear Chat
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.markdown("---")
    st.subheader("Last Messages")
    display_last_message()

# ------------------------------
# Main Chat Panel
# ------------------------------
st.title("DeepSeek R1 Chatbot")
st.caption("Powered by Groq API")

# Chat Input
prompt = st.chat_input("Type your message here...")

if prompt:
    if not api_key:
        st.info("Please enter your Groq API key to continue")
        st.stop()

    # Append and display user message
    append_message("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"_{st.session_state.messages[-1]['timestamp']}_")

    # Call Groq API
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            # Optional parameters for customizing responses:
            # temperature=0.7, max_tokens=1024, top_p=1.0, frequency_penalty=0.0,
            stream=False
        )

        ai_response = response.choices[0].message.content

        # Append and display bot message
        append_message("assistant", ai_response)
        with st.chat_message("assistant"):
            st.markdown(ai_response)
            st.caption(f"_{st.session_state.messages[-1]['timestamp']}_")

    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
