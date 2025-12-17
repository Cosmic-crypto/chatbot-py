# PyBot Chatbot 🤖

A simple **intent-based chatbot** built with **Python**, **scikit-learn**, and **TF-IDF**. PyBot uses classic machine learning (not deep learning) to classify user input into intents and respond accordingly. It also supports basic tools like math operations, random number generation, date/time, and calendar display.

---

## 📂 Project Structure

```
py_chatbot/
│
├── ml.py              # Main chatbot + ML model
├── tools.py           # Utility functions (math, date, calendar, random)
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

4. **Response Handling**
   - Some intents trigger **tool functions** (math, date, calendar, random)
   - Other intents return predefined responses

---

## 🚀 Features

- 💬 Natural language intent classification
- 🧮 Math operations (add, subtract, multiply, divide)
- 🎲 Random number generation
- 📅 Date & time lookup
- 🗓 Calendar display (current year or specific year)
- 😂 Jokes & casual conversation
- 🛑 Graceful exit with terminal clear

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
- math
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
pip install scikit-learn
```

(Standard libraries like `json`, `datetime`, `random`, etc. are included with Python.)

---

## ▶️ Running the Chatbot

From the project directory:

```bash
python ml.py
```

You’ll see:
```
You:
```
Type a message and chat with PyBot.

To exit:
- Type `bye`, `quit`, `exit`, etc.
- Or press **Ctrl + C**

The terminal will automatically clear when the chat ends.

---

## 🧮 Math Examples

```
You: add 5 and 10
You: divide 20 by 4
You: multiply 6 times 7
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
- Use `stratify=tags` in `train_test_split`
- Consider switching to `LogisticRegression` for better confidence handling

---

## ⚠️ Notes & Limitations

- This is a **rule + ML hybrid**, not a generative AI
- Accuracy depends heavily on training data quality
- Weather, news, and translations are placeholders unless connected to APIs

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
