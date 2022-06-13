import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

patterns = "[^а-яА-я0-9a-zA-Z]"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()

def tokenize(text: str) -> list:
    text = re.sub(patterns, ' ', text)

    tokens = []
    for token in text.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            if not token:
                token = ''
            tokens.append(token)
    return tokens

def lemmatize(text: str) -> str:
    t = tokenize(text)
    if t == None: t = ''
    return ' '.join(t)

def main():
    print(lemmatize(input()))

if __name__ == "__main__":
    main()