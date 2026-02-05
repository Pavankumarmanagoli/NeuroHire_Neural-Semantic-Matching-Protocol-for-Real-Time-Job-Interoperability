import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Groq client (make sure GROQ_API_KEY is in your .env)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file (Streamlit uploaded_file).
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Keep the same name so app.py doesn't need changes
def ask_openai(prompt, max_tokens=500):
    """
    Sends a prompt to Groq (OpenAI-style naming kept to avoid changing app.py).
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # fast + good for this use case
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
