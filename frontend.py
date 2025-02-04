import streamlit as st
import requests


st.set_page_config(page_title="Langgraph AI Agent", layout="centered")
st.title("AI Agent")
st.write("Create and Interact with the AI Agents")

system_prompt = st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here..")

GROQ_MODEL = [
    "llama-3.3-70b-versatile",
    "deepseek-r1-distill-llama-70b",
    "mixtral-8x7b-32768",
    "gemma2-9b-it"
]

OPEN_AI_MODEL = [
    "gpt-40-mini"
]

provider = st.radio("select Provider", ("Groq", "OpenAI"))
if provider == "Groq":
    select_model = st.selectbox("Select Groq model: ", GROQ_MODEL)
else:
    select_model = st.selectbox("Select OpenAI Model: ", OPEN_AI_MODEL)

allow_web_search = st.checkbox("Allow WebSearch")

user_query = st.text_area("Enter your query: ", height=80, placeholder="Ask Anything!")


API_URL = "http://127.0.0.1:9999/chat"
if st.button("Ask Agent!"):
    if user_query.strip():
        payload = {
            "model_name": select_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"{response_data}")