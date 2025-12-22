import customtkinter as ctk
from re import findall, search
from string import (
    ascii_letters,
    digits,
    punctuation
)
from json import load as jload
from joblib import load
from random import choice
from tools import *

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

APP = ctk.CTk()
APP.title("Py-chatbot")
APP.geometry('800x600')

OUTPUT_FRAME = ctk.CTkScrollableFrame(APP)
OUTPUT_FRAME.pack(pady=10, fill="both", expand=True)

# Load data from JSON into intents
with open('py_chatbot\\training.json', 'r', encoding='utf-8') as f:
    intents = jload(f)

# Normalize patterns to lowercase for consistency
for intent in intents:
    intent['patterns'] = [p.lower() for p in intent['patterns']]

patterns = []
tags = []

for intent in intents:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])

vectorizer = load('vectorizer.pkl')
model = load('model.pkl')

def AI_response(user_input: str) -> str:
    if not user_input:
        return "please enter a valid input"
    
    chars = ascii_letters + digits + punctuation + " "
    
    for s in user_input:
        if s not in chars:
            return f"Your input: {user_input} contains non-standard characters"
    
    input_vec = vectorizer.transform([user_input])
    proba = model.predict_proba(input_vec)[0]
    confidence = max(proba)
    tag = model.classes_[proba.argmax()]

    if confidence < 0.5:
        return "I am not sure I understand that"

    if tag == "math":
        numbers = findall(r"\d+", user_input)
        
        # Check we have exactly 2 numbers
        if len(numbers) != 2:
            return "I need/can only take two numbers to perform the operation."
        
        x, y = float(numbers[0]), float(numbers[1])

        # Map operation keywords to math function operations
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
        
        # Call the math function
        try:
            return f"The answer to that question is: {str(maths(x, y, operation))}"
        except Exception as err:
            return f"Error performing calculation: {err}"
        
    elif tag == "repeat":
        words = user_input.split()
        ignored_words = "repeat", "after", "me", "say", "this", ":", "can", "you"
        
        # Filter out the common words to leave just the city
        words = [w for w in words if w.lower() not in ignored_words]
        return repeat("".join(word for word in words)) # repeat
    
    elif tag == "random":
        numbers = findall(r"\d+", user_input)
        if len(numbers) < 2:
            return "Please provide two numbers for the range."
        return f"... {generate_rand(numbers[0], numbers[1])}"
    
    elif tag == "weather":
        return weather()
    
    elif tag == "equation":
        try:
            # Extract equation using regex
            match = search(r"([a-zA-Z0-9+\-*/^=() ]+)", user_input)
            if not match:
                return "I couldn't find an equation to solve."

            equation = match.group(1).replace(" ", "")
            
            # Detect variables (letters only)
            variables = sorted(set(findall(r"[a-zA-Z]", equation)))

            return solve_equation(equation, *variables)

        except Exception as err:
            return f"Could not solve the equation: {err}"
    
    elif tag == "simplify":
        words = user_input.split()
        ignored_words = "what", "solve", "equation", "can", "you", "do", "this", "for", "me", ":"

        # Filter out the common words to leave just the city
        expr = [w for w in words if w.lower() not in ignored_words]
        expr = [str(e) for e in expr]
        return simplify(expr)

    elif tag == "news":
        news_providers = (
            "https://edition.cnn.com/", 
            "https://www.bbc.co.uk/news",
            "https://www.nytimes.com/international/",
            "https://www.ctvnews.ca/"
        )

        news_provider = choice(news_providers)

        return get_news(news_provider)
    
    elif tag in ("date", "time"):
        return f"Here is the date & time: {fetch_date()}"
    
    elif tag == "calendar":
        numbers = findall(r"\d+", user_input)
        if len(numbers) == 0:
            numbers = None
        else:
            numbers = int("".join(n for n in numbers))
        return f"Calendar: {show_calender(numbers)}"
        
    # Handle normal intents
    else:
        for intent in intents:
            if intent['tag'] == tag:
                return choice(intent['responses'])
    
    return "I'm not sure I understand that."

def ask():
    user_input = user.get().strip()
    
    if not user_input:
        return
    
    # Create separate labels for user and AI messages
    user_label = ctk.CTkLabel(
        OUTPUT_FRAME, 
        text=f"You: {user_input}", 
        wraplength=700,
        anchor="w",
        justify="left"
    )
    user_label.pack(pady=(10, 2), anchor="w", fill="x")
    
    ai_response = AI_response(user_input)
    
    ai_label = ctk.CTkLabel(
        OUTPUT_FRAME, 
        text=f"AI: {ai_response}", 
        wraplength=700,
        anchor="w",
        justify="left"
    )
    ai_label.pack(pady=(2, 10), anchor="w", fill="x")
    
    # Clear entry after asking
    user.delete(0, 'end')

def clear():
    for widget in OUTPUT_FRAME.winfo_children():
        widget.destroy()

    user.delete(0, 'end')

user = ctk.CTkEntry(APP, placeholder_text="Ask the AI...")
user.pack(pady=20)

enter_button = ctk.CTkButton(APP, text="Ask", command=ask)
enter_button.pack(pady=10)

clear_button = ctk.CTkButton(APP, text="Clear", command=clear).pack(pady=10)

APP.mainloop()
