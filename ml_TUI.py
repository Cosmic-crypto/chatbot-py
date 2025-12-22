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

# Load data from JSON into intents
with open('py_chatbot\\training.json', 'r', encoding='utf-8') as f:
    intents = jload(f)

# Normalize patterns to lowercase for consistency
for intent in intents:
    intent['patterns'] = [p.lower() for p in intent['patterns']]

# Build training data
patterns = []
tags = []

for intent in intents:
    for pattern in intent['patterns']:
        patterns.append(pattern)
        tags.append(intent['tag'])

# Convert text → numbers
vectorizer = load('model.pkl')
model = load('model.pkl')

def AI_response(user_input: str) -> str:
    input_vec = vectorizer.transform([user_input])
    proba = model.predict_proba(input_vec)[0]
    confidence = max(proba)
    tag = model.classes_[proba.argmax()]

    CONFIDENCE_THRESHOLDS = {
        "greeting": 0.17,
        "goodbye": 0.25,
        "thanks": 0.30,
        "help": 0.30,
        "joke": 0.30,

        # risky intents
        "math": 0.55,
        "equation": 0.60,
        "weather": 0.50,
        "news": 0.50
    }


    threshold = CONFIDENCE_THRESHOLDS.get(tag, 0.45)

    if confidence < threshold:
        return "I'm not sure I understood that. Could you rephrase?"
    
    # Handle math intent
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
        
    elif tag == "random":
        numbers = findall(r"\d+", user_input)
        return f"Here is a random number from {numbers[0]} to {numbers[1]}: {generate_rand(numbers[0], numbers[1])}"
    
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
    
    elif tag == "repeat":
        words = user_input.split()
        ignored_words = "repeat", "after", "me", "say", "this", ":", "can", "you"
        
        # Filter out the common words to leave just the city
        words = [w for w in words if w.lower() not in ignored_words]
        return repeat("".join(word for word in words)) # repeat
    
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

chars = ascii_letters + digits + punctuation

while True:
    try:
        user = input("You: ")

        if not user:
            print("AI: Please enter a valid input")
            continue

        if user not in chars:
            print(f"AI: Your input: {user} contains non-standard characters")
            continue

        if user.strip().lower() in ("break", "stop", "quit", "end", "exit", "goodbye", "bye"):
            user_choice = input("AI: are you sure you want to end this conversation?\n (y/n): ").strip().lower()

            if user_choice == "y":
                print(AI_response("goodbye"))
                break
            
        print(AI_response(user))
    
    except KeyboardInterrupt:
        print(AI_response("goodbye"))
        break

    except Exception as err:
        print(f"AI: A problem has occured: {err}")
