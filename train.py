from json import load
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump

# Load training data
with open("training.json", "r", encoding="utf-8") as f:
    intents = load(f)

patterns = []
tags = []

for intent in intents:
    for p in intent["patterns"]:
        patterns.append(p.lower())
        tags.append(intent["tag"])

# Better vectorizer
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    stop_words="english",
    max_df=0.9
)

X = vectorizer.fit_transform(patterns)

X_train, X_test, y_train, y_test = train_test_split(
    X, tags, stratify=tags, test_size=0.2, random_state=42
)

# Better model
model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

# Save model + vectorizer
dump(model, "model.pkl")
dump(vectorizer, "vectorizer.pkl")

print("✅ Model trained and saved successfully")
