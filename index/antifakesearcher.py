from catboost import CatBoostClassifier
from .semantic import lemmatize
import os

model = CatBoostClassifier()
BASE_DIR2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model.load_model(os.path.join(BASE_DIR2, 'media/antifake.model'))

def predict(text: str):
    result = model.predict([lemmatize(text)])
    
    return result

def predict_proba(text: str):
    result = model.predict_proba([lemmatize(text)])

    return result

def main():
    while True:
        input_text = input('Введите сообщение: ')
        result = predict_proba(input_text)
        print('Вероятность фейка: ', result)

if __name__ == "__main__":
    main()
