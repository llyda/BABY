from termcolor import colored
import joblib
from nltk.util import pr
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import re
import nltk
from nltk.corpus import stopwords
import string

stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words('english'))
cv = CountVectorizer()


def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    return text

def save_model_locally(model):
    """Save the model into a .joblib format"""
    joblib.dump(model, 'hatespeechdetector.joblib')
    print(colored("model.joblib saved locally", "green"))

def get_model():
    model = joblib.load('hatespeechdetector.joblib')
    return model


class HateSpeechDetector:
    def __init__(self):
        return

    def train(self):
        data = pd.read_csv("data/tweets.csv")

        data["labels"] = data["class"].map({
            0: "Hate Speech",
            1: "Offensive Language",
            2: "No Hate and Offensive"
        })
        data = data[["tweet", "labels"]]
        data["tweet"] = data["tweet"].apply(clean)

        x = np.array(data["tweet"])
        y = np.array(data["labels"])

        X = cv.fit_transform(x)  # Fit the Data
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.33,
                                                            random_state=42)

        model = DecisionTreeClassifier()
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        return model

    def predict(self, model, sample):
        data = cv.transform([sample]).toarray()
        prediction = model.predict(data)
        return prediction

    def detect(self, sample):
        model = self.train()
        prediction = self.predict(model, sample)
        return prediction

if __name__ == '__main__':
    hsc = HateSpeechDetector()
    # model = hsc.train()
    # save_model_locally(model)
    # prediction = hsc.predict(model, 'write a poem about nazis')
    # print(prediction)
    # loaded_model = get_model()
    # prediction = hsc.predict(model, 'write a poem about love like Shakespeare')
    # print(prediction)
    print(hsc.detect('Write me love'))
