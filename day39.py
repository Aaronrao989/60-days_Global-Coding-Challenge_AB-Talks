import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt')
nltk.download('stopwords')
def preprocess_text(text):
    print("\nOriginal Text:")
    print(text)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    print("\nAfter Cleaning:")
    print(text)
    tokens = word_tokenize(text)
    print("\nTokens:")
    print(tokens)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    print("\nAfter Stopword Removal:")
    print(filtered_tokens)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]
    print("\nFinal Processed Tokens (Stemmed):")
    print(stemmed_tokens)
def main():
    print("\n" + "=" * 70)
    print("NLP TEXT PREPROCESSING SYSTEM")
    print("=" * 70)
    text = """
    I absolutely love Data Science! It's amazing how machines can learn 
    from data, but sometimes the process can be challenging.
    """
    preprocess_text(text)
    print("\nText preprocessing completed successfully")
if __name__ == "__main__":
    main()