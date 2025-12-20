from tools import *
from re import findall, search
from json import load
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from random import choice

# Load data from JSON into intents
with open('py_chatbot\\training.json', 'r', encoding='utf-8') as f:
    intents = load(f)

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
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

# train our model
X_train, X_test, y_train, y_test = train_test_split(X, tags, stratify=tags, test_size=0.2, random_state=42)

# Define our model
model = LinearSVC()
model.fit(X_train, y_train)

def AI_response(user_input: str) -> str:
    input_vec = vectorizer.transform([user_input])
    tag = model.predict(input_vec)[0]
    
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
        
while True:
    try:
        user = input("You: ")

        if not user:
            print("AI: Please enter a valid input")
            continue

        if search(r'[^a-zA-Z0-9\*$$$$\?\.\,\ ]', user):
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
