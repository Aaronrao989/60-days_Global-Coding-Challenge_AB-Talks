from flask import Flask, render_template, request
import joblib
import re
import os
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

app = Flask(__name__)

# Paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "sentiment_model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"))

# Load once at startup
STOP_WORDS = set(stopwords.words('english'))


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    words = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(words)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None

    if request.method == "POST":
        user_input = request.form.get("text", "").strip()

        if not user_input:
            error = "Please enter some text."
        else:
            try:
                cleaned = clean_text(user_input)
                vectorized = vectorizer.transform([cleaned])
                prediction = model.predict(vectorized)[0]
            except Exception as e:
                error = "Prediction failed. Please try again."

    return render_template("index.html", prediction=prediction, error=error)


if __name__ == "__main__":
    app.run(debug=False)