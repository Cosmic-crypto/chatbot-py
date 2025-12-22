from json import load
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from joblib import dump

BASE = Path("py_chatbot")

with open(BASE / "training.json", encoding="utf-8") as f:
    intents = load(f)

patterns, tags = [], []

for intent in intents:
    for p in intent["patterns"]:
        patterns.append(p.lower())
        tags.append(intent["tag"])

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english",
    max_df=0.9,
    min_df=1
)

X = vectorizer.fit_transform(patterns)

X_train, X_test, y_train, y_test = train_test_split(
    X, tags,
    stratify=tags,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression(
    max_iter=2000,
    solver="liblinear",
    class_weight="balanced"
)

model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

dump(model, BASE / "model.pkl")
dump(vectorizer, BASE / "vectorizer.pkl")

print("✅ Model trained and saved successfully")
