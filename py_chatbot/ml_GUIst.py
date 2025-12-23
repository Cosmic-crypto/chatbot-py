import streamlit as st
from re import findall, search
from string import ascii_letters, digits, punctuation
from json import load as jload
from joblib import load
from random import choice
from tools import *  # Ensure this contains all helper functions
import sys
from pathlib import Path

# ------------------------------
# UI Title
# ------------------------------
st.markdown('<h3 style="text-align:center;">AI Chatbot</h3>', unsafe_allow_html=True)

# ------------------------------
# Base Directory Handling
# ------------------------------
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent

# ------------------------------
# Load Intents and Normalize
# ------------------------------
with open(BASE_DIR / 'training.json', 'r', encoding='utf-8') as f:
    intents = jload(f)

for intent in intents:
    intent['patterns'] = [p.lower() for p in intent['patterns']]

# ------------------------------
# Load Vectorizer and Model
# ------------------------------
vectorizer = load(BASE_DIR / 'vectorizer.pkl')
model = load(BASE_DIR / 'model.pkl')

# ------------------------------
# AI Response Function
# ------------------------------
def AI_response(user_input: str) -> str:
    if not user_input.strip():
        return "Please enter a valid input."
    
    # Check for invalid characters
    chars = ascii_letters + digits + punctuation + " "
    for s in user_input:
        if s not in chars:
            return f"Your input contains non-standard characters: {s}"
    
    # Predict intent
    input_vec = vectorizer.transform([user_input])
    proba = model.predict_proba(input_vec)[0]
    confidence = max(proba)
    tag = model.classes_[proba.argmax()]
    first_tag = tag
    second_tag = model.predict(input_vec)[0]

    if first_tag != second_tag:
        return "I'm unsure what you mean. Can you clarify?"

    # Confidence thresholds
    CONFIDENCE_THRESHOLDS = {
        "greeting": 0.1,
        "how_are_you": 0.1,
        "goodbye": 0.2,
        "thanks": 0.25,
        "help": 0.25,
        "joke": 0.25,
        "math": 0.5,
        "equation": 0.55,
        "weather": 0.45,
        "news": 0.45,
        "name": 0.25,
        "creator": 0.25,
        "time": 0.25,
        "date": 0.25,
        "calendar": 0.3,
        "simplify": 0.5,
        "random": 0.25,
        "repeat": 0.25,
        "fallback": 0.1
    }

    threshold = CONFIDENCE_THRESHOLDS.get(tag, 0.45)
    if confidence < threshold:
        return "I'm not sure I understood that. Could you rephrase?"

    # ------------------------------
    # Handle Tags
    # ------------------------------
    if tag == "math":
        numbers = findall(r"\d+", user_input)
        if len(numbers) != 2:
            return "I can only handle two numbers for calculations."
        x, y = float(numbers[0]), float(numbers[1])
        keywords = {
            "divide": "divide", "over": "divide", "by": "divide", "divided": "divide", "divided by": "divide", "/": "divide",
            "times": "multiply", "multiply": "multiply", "multiplication": "multiply", "x": "multiply", "*": "multiply",
            "add": "add", "addition": "add", "plus": "add", "+": "add",
            "sub": "subtract", "take away": "subtract", "subtract": "subtract", "-": "subtract",
            "subtraction": "subtract", "minus": "subtract"
        }
        operation = None
        for word, op in keywords.items():
            if word in user_input.lower():
                operation = op
                break
        if operation is None:
            return "I couldn't find an operation to perform."
        try:
            return f"The answer is: {maths(x, y, operation)}"
        except Exception as e:
            return f"Error performing calculation: {e}"

    elif tag == "repeat":
        words = user_input.split()
        ignored_words = ("repeat", "after", "me", "say", "this", ":", "can", "you")
        filtered = [w for w in words if w.lower() not in ignored_words]
        return repeat(" ".join(filtered))

    elif tag == "random":
        numbers = findall(r"\d+", user_input)
        if len(numbers) < 2:
            return "Please provide two numbers for the range."
        return str(generate_rand(int(numbers[0]), int(numbers[1])))

    elif tag == "weather":
        return weather()

    elif tag == "equation":
        try:
            match = search(r"([a-zA-Z0-9+\-*/^=() ]+)", user_input)
            if not match:
                return "I couldn't find an equation."
            equation = match.group(1).replace(" ", "")
            variables = sorted(set(findall(r"[a-zA-Z]", equation)))
            return solve_equation(equation, *variables)
        except Exception as e:
            return f"Could not solve the equation: {e}"

    elif tag == "simplify":
        words = user_input.split()
        ignored_words = ("what", "solve", "equation", "can", "you", "do", "this", "for", "me", ":")
        expr = [w for w in words if w.lower() not in ignored_words]
        return simplify(expr)

    elif tag == "news":
        providers = [
            "https://edition.cnn.com/",
            "https://www.bbc.co.uk/news",
            "https://www.nytimes.com/international/",
            "https://www.ctvnews.ca/"
        ]
        return get_news(choice(providers))

    elif tag in ("date", "time"):
        return fetch_date()

    elif tag == "calendar":
        numbers = findall(r"\d+", user_input)
        num = int("".join(numbers)) if numbers else None
        return show_calender(num)

    else:
        for intent in intents:
            if intent['tag'] == tag:
                return choice(intent['responses'])

    return "I'm not sure I understand that."

# ------------------------------
# Session State Initialization
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# Handlers
# ------------------------------
def ask(user_input):
    if not user_input.strip():
        return
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = AI_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

def clear():
    st.session_state.messages.clear()

# ------------------------------
# UI Controls
# ------------------------------
st.button("Clear Chat", on_click=clear)

user_input = st.chat_input("Ask the AI...")
if user_input:
    ask(user_input)

# Display conversation history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"].strip())
