from src.collect import get_tweet_data
from src.preprocess import preprocess
from src.model import predict

# 1. Récupération du tweet
tweet = get_tweet_data("https://...", "email", "mdp")
text = tweet['text']

# 2. Prétraitement
text_clean = preprocess(text)

# 3. Prédiction
score = predict(text_clean)

# 4. Affichage
print(f"Score de fiabilité : {score:.2f}")

'''Appelle les fonctions de collecte, nettoyage, prédiction.

Affiche un score entre 0 (vrai) et 1 (fake).'''