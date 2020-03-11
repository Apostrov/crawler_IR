import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def normalize(text):
    return re.sub(r'[^A-Za-z *]+', '', text.lower())

def tokenize(text):
    return nltk.word_tokenize(text)

def lemmatization(tokens):
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

def remove_stop_word(tokens):
    stops = set(stopwords.words('english'))
    return [token for token in tokens if token not in stops]

def preprocess(text, lemmatize=True):
    normalized = normalize(text)
    tokens = tokenize(normalized)
    if not lemmatize:
        return remove_stop_word(tokens)
    lemmed = lemmatization(tokens)
    clean = remove_stop_word(lemmed)
    return clean