import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Training data (replace later with real dataset)
texts = [
    "Free entry win money",
    "Call now for prize",
    "Hello how are you",
    "Let's meet tomorrow",
    "Win cash now"
]

labels = [1, 1, 0, 0, 1]

# Create vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train model
model = LogisticRegression()
model.fit(X, labels)

# Save properly (IMPORTANT: use 'with')
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model & vectorizer saved!")