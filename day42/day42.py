import pandas as pd
import re
import nltk
import joblib
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
nltk.download('stopwords')
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)
def load_data(path):
    df = pd.read_csv(path)
    df["processed_text"] = df["review"].apply(clean_text)
    return df

def split_data(df):
    X = df["processed_text"]
    y = df["sentiment"]
    return train_test_split(X, y, test_size=0.2, random_state=42)
def vectorize(X_train, X_test):
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    return vectorizer, X_train_tfidf, X_test_tfidf

def train_model(X_train, y_train):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

def save_model(model, vectorizer):
    joblib.dump(model, "sentiment_model.pkl")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
    print("\nModel saved successfully")

def main():
    print("\n" + "="*70)
    print("END-TO-END NLP PIPELINE")
    print("="*70)
    df = load_data("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day41/IMDB Dataset.csv")
    X_train, X_test, y_train, y_test = split_data(df)
    vectorizer, X_train_tfidf, X_test_tfidf = vectorize(X_train, X_test)
    model = train_model(X_train_tfidf, y_train)
    evaluate(model, X_test_tfidf, y_test)
    save_model(model, vectorizer)
if __name__ == "__main__":
    main()