import json
import re
import spacy
import os
from langdetect import detect, LangDetectException
import pandas as pd

# 📥 Charger le modèle spaCy en fonction de la langue détectée
def load_spacy_model(text):
    # Vérifier si le texte est non vide avant de tenter de détecter la langue
    if not text or len(text.strip()) < 10:  # Si le texte est trop court ou vide, on ne détecte pas la langue
        return None

    try:
        # Détecte la langue du texte
        lang = detect(text)
    except LangDetectException:
        # En cas d'échec de la détection, on renvoie None
        return None
    
    # Charge le modèle spaCy en fonction de la langue détectée
    if lang == 'fr':
        try:
            nlp = spacy.load("fr_core_news_md")
        except OSError:
            print("Téléchargement du modèle spaCy 'fr_core_news_md'...")
            from spacy.cli import download
            download("fr_core_news_md")
            nlp = spacy.load("fr_core_news_md")
    else:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Téléchargement du modèle spaCy 'en_core_web_sm'...")
            from spacy.cli import download
            download("en_core_web_sm")
            nlp = spacy.load("en_core_web_sm")
    
    return nlp

# 📂 Charger les données collectées
with open('collected_posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)

# 🔧 Fonction de nettoyage
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)  # Supprimer les URLs
    text = re.sub(r'@\w+', '', text)  # Supprimer les mentions
    text = re.sub(r'#\w+', '', text)  # Supprimer les hashtags
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Supprimer la ponctuation et les chiffres
    
    # Charger le modèle spaCy basé sur la langue du texte
    nlp = load_spacy_model(text)
    if not nlp:
        return "", ""  # Retourner des chaînes vides si le modèle n'a pas pu être chargé
    
    doc = nlp(text)

    tokens = [
        token.text for token in doc
        if not token.is_stop and not token.is_punct and len(token.text) > 2
    ]

    # Lemmatisation
    lemmatized = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and len(token.text) > 2
    ]

    return tokens, " ".join(lemmatized)

# 🧪 Appliquer le prétraitement
preprocessed_posts = []
for post in posts:
    original_text = post.get('text', '')
    tokens, lemmatized_text = preprocess_text(original_text)
    cleaned_text = ' '.join(tokens)
    
    preprocessed_posts.append({
        'uri': post.get('uri'),
        'original_text': original_text,
        'cleaned_text': cleaned_text,
        'tokens': tokens,
        'lemmatized_text': lemmatized_text
    })

# 💾 Sauvegarder les résultats
with open('preprocessed_posts.json', 'w', encoding='utf-8') as f:
    json.dump(preprocessed_posts, f, indent=2, ensure_ascii=False)

print(f"✅ {len(preprocessed_posts)} posts prétraités avec spaCy et enregistrés dans preprocessed_posts.json")

def preprocess_liar_dataset(input_path, output_path):
    df = pd.read_csv(input_path, sep='\t', header=None, names=[
        'id', 'label', 'statement', 'subject', 'speaker', 'speaker_job', 'state_info',
        'party', 'barely_true', 'false', 'half_true', 'mostly_true', 'pants_on_fire',
        'context'
    ])
    
    print(f"🔍 Dataset chargé : {input_path} ({len(df)} lignes)")

    # Mapper les labels textuels en binaires : fake = 1, real = 0
    fake_labels = ['false', 'barely-true', 'pants-fire']
    df['label'] = df['label'].apply(lambda x: 1 if x in fake_labels else 0)

    preprocessed = []
    for _, row in df.iterrows():
        text = row['statement']
        tokens, lemmatized_text = preprocess_text(text)
        cleaned_text = ' '.join(tokens)

        preprocessed.append({
            'original_text': text,
            'cleaned_text': cleaned_text,
            'tokens': tokens,
            'lemmatized_text': lemmatized_text,
            'label': row['label']
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(preprocessed, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(preprocessed)} samples LIAR prétraités et sauvegardés dans {output_path}")

if __name__ == '__main__':
    mode = input("Tape 'liar' pour prétraiter le dataset LIAR, sinon Enter pour les posts Bluesky : ").strip().lower()

    if mode == 'liar':
        preprocess_liar_dataset('liar_dataset/train.tsv', 'preprocessed_liar_train.json')
    else:
        # 🧪 Appliquer le prétraitement des posts collectés
        preprocessed_posts = []
        for post in posts:
            original_text = post.get('text', '')
            tokens, lemmatized_text = preprocess_text(original_text)
            cleaned_text = ' '.join(tokens)
            
            preprocessed_posts.append({
                'uri': post.get('uri'),
                'original_text': original_text,
                'cleaned_text': cleaned_text,
                'tokens': tokens,
                'lemmatized_text': lemmatized_text
            })

        with open('preprocessed_posts.json', 'w', encoding='utf-8') as f:
            json.dump(preprocessed_posts, f, indent=2, ensure_ascii=False)

        print(f"✅ {len(preprocessed_posts)} posts prétraités avec spaCy et enregistrés dans preprocessed_posts.json")
