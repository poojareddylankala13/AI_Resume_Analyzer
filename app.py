import streamlit as st
import PyPDF2
import requests

st.title("📄 AI Resume Analyzer (Advanced)")

# Mode selection
mode = st.radio("Choose AI Mode:", ["Local (Ollama)", "API (BYOK)"])

# API Key input
api_key = None
if mode == "API (BYOK)":
    api_key = st.text_input("Enter your API Key", type="password")

# Upload file
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Extract text
def extract_text(pdf):
    reader = PyPDF2.PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Ollama (Local AI)
def analyze_with_ollama(text):
    try:
        url = "http://localhost:11434/api/generate"
        data = {
            "model": "llama3",
            "prompt": f"Analyze this resume and give suggestions:\n{text}"
        }
        response = requests.post(url, json=data)
        return response.json().get("response", "Error from Ollama")
    except:
        return "⚠️ Ollama not running. Please start Ollama locally."

# API (BYOK)
def analyze_with_api(text, api_key):
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": f"Analyze this resume:\n{text}"}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "⚠️ Invalid API Key or request failed"

# Main
if uploaded_file:
    text = extract_text(uploaded_file)

    st.subheader("📊 AI Analysis")

    if mode == "Local (Ollama)":
        st.info("Using Local AI (Ollama)")
        result = analyze_with_ollama(text)
    else:
        if not api_key:
            st.warning("Enter API key")
            result = ""
        else:
            st.info("Using API AI")
            result = analyze_with_api(text, api_key)

    st.write(result)
