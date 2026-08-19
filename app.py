import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="JARVIS AI", page_icon="⚡", layout="centered")
st.title("🤖 JARVIS Agentic AI")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.markdown("[Get Free API Key](https://aistudio.google.com/)")

JARVIS_PROMPT = """
You are JARVIS, a highly capable autonomous AI assistant.
Rules:
1. Act witty, professional, grounded, and highly efficient.
2. If asked to build an app or project, ask clarifying questions first.
3. Structure complex planning concisely using bullet points.
"""

if not api_key:
    st.warning("कृपया साइडबार में अपनी Gemini API Key डालें।")
    st.stop()

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Command JARVIS..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        contents = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part.from_text(text=m["content"])]
            )
            for m in st.session_state.messages
        ]
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=JARVIS_PROMPT,
                temperature=0.7,
            )
        )
        
        reply_text = response.text
        st.markdown(reply_text)
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
      
