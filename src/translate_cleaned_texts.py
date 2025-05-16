import json
from deep_translator import GoogleTranslator

# Charger les données existantes
with open("preprocessed_posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Traduire les cleaned_text
translator = GoogleTranslator(source='auto', target='fr')

for post in data:
    try:
        english_text = post["cleaned_text"]
        translated = translator.translate(english_text)
        post["cleaned_text_fr"] = translated
    except Exception as e:
        print(f"Erreur pour le post {post['uri']} : {e}")
        post["cleaned_text_fr"] = ""

# Sauvegarder les données enrichies
with open("preprocessed_posts_translated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Traduction terminée. Fichier enregistré sous preprocessed_posts_translated.json")
