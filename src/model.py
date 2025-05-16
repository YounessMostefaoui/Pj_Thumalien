import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

def train_model(X_train, y_train):
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vect = vectorizer.fit_transform(X_train)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_vect, y_train)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, 'models/fake_news_model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    print("✅ Modèle entraîné et sauvegardé.")

def predict(text, model_path='models/fake_news_model.pkl', vec_path='models/vectorizer.pkl'):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    X = vectorizer.transform([text])
    return model.predict_proba(X)[0][1]  # Probabilité d'être une fake news

# 🔁 Bloc exécutable
if __name__ == "__main__":
    # Charger les données
    with open('preprocessed_liar_train.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)
    X = df['lemmatized_text']
    y = df['label']

    # Séparer en train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entraîner
    train_model(X_train, y_train)

    # Évaluer
    vectorizer = joblib.load('models/vectorizer.pkl')
    model = joblib.load('models/fake_news_model.pkl')
    X_test_vect = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_vect)

    print("\n📊 Rapport d'évaluation :")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
