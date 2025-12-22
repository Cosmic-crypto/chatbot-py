# PyBot Chatbot (v3) 🤖

A simple **intent-based chatbot** built with **Python**, **scikit-learn**, and **TF-IDF**. PyBot uses classic machine learning (not deep learning) to classify user input into intents and respond accordingly. It also supports basic tools like math operations, random number generation, date/time, and calendar display.

---
## Release notes (v3)
- train.py meaning only train once and no more training
- better accuracy, the model now will not answer unless it is atleast 50% clear on what you are asking
- equation solver made better but full fix coming with v3.1

---

## 📂 Project Structure

```
py_chatbot/
│
├── ml_TUI.py          # Main chatbot + ML model (Terminal)
├── ml_GUI.py          # Main chatbot + ML model (User-interface)
├── train.py           # trains the chatbots and creates model.plk and vectorizer.plk
├── model.plk          # trained model. File made by train.py
├── vectorizer.plk     # trained vectorizer. File made by train.py
├── tools.py           # Utility functions (math, date, calendar, random, search, weather)
├── training.json      # Intent definitions (patterns & responses)
└── README.md          # Project documentation
```

---

## ⚙️ How It Works

1. **Training Data**
   - Intents are defined in `training.json`
   - Each intent contains:
     - `tag` – intent label
     - `patterns` – example user inputs
     - `responses` – possible bot replies

2. **Text Vectorization**
   - User patterns are converted into numerical features using **TF-IDF**

3. **Intent Classification**
   - A machine learning model (`LinearSVC`) is trained to classify input text into intents

4. **Training**
 - Uses joblib to train the `LinearSVC` model and `TF-IDF` vectorizer
 - creates a model.plk and vectorizer.plk
 - You only have to run train.py once  

5. **Response Handling**
   - Some intents trigger **tool functions** (math, date, calendar, random)
   - Other intents return predefined responses

---

## 🚀 Features

- 💬 Natural language intent classification
- 🧮 Math operations (add, subtract, multiply, divide)
- 🎲 Random number generation
- 📅 Date & time lookup
- 📰 News headline shower
- 🌤️ Check the weather (currently only for London)
- 🗓 Calendar display (current year or specific year)
- 😂 Jokes & casual conversation
- 🛑 Graceful exit with terminal clear
- 🕒 Only have to train once making it faster

---

## 🧠 Supported Intents

- greeting
- goodbye
- thanks
- how_are_you
- name
- creator
- time
- date
- calendar
- news
- weather
- math
- equation
- simplify
- random
- joke
- help
- fallback (for unknown input)

You can easily add more by editing `training.json`.

---

## 🛠 Requirements

- Python **3.9+**
- Required libraries:

```bash
pip install scikit-learn joblib
```
and if you want the GUI:

```bash
pip install customtkinter
```

with everyting included:

```bash
pip install scikit-learn joblib customtkinter
```

(Standard libraries like `json`, `datetime`, `random`, etc. are included with Python.)

---

## ▶️ Running the Chatbot

From the project directory:

```bash
python train.py
```
to train the model

```bash
python ml_GUI.py # GUI version
python ml_TUI.py # TUI version
```

You’ll see:
```
You:
```
Type a message and chat with PyBot.

To exit:
- Type `bye`, `quit`, `exit`, etc.
- Or press **Ctrl + C**

---

## 🧮 Math Examples

```
You: add 5 and 10
You: divide 20 by 4
You: multiply 6 times 7
You: what is 20x5
You: what is 4/2
You: solve: 3x+2=10
```

---

## 🎲 Random Number Example

```
You: give me a random number between 1 and 50
```

---

## 📅 Calendar Example

```
You: show me the calendar
You: calendar for the year 2024
```

---

## 🧩 Customization

### Add New Intents
Edit `training.json`:

```json
{
  "tag": "new_intent",
  "patterns": ["example input"],
  "responses": ["example response"]
}
```

Restart the chatbot to retrain the model.

---

## 📈 Improving Accuracy

For best results:
- Add **20–30 patterns per intent**
- Avoid overlapping phrases between intents

---

## ⚠️ Notes & Limitations

- This is a **rule + ML hybrid**, not a generative AI
- Accuracy depends heavily on training data quality

---

## Improvement ideas:

- Currently the equation solver does not really work, so fix the equation solver
- Add a choice to chose where you are and get the weather
- Add better training data!

---

## 📜 License

This project is open-source and free to use for learning and experimentation.

---

## 👤 Author

Created by **Cosmic Beast** 🚀

Built with Python, curiosity, and machine learning.

---
## Feedback
I would love to have some feedback because this is lime my first major project building a chatbot with ML and it's isn't really the best but it's like an alright beginner
version.
