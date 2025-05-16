from atproto import Client
import json
import os

# Initialisation
client = Client()
client.login('youness.mostefaoui@free.fr', 'Honaine77aa..()')

print("📥 Démarrage de la collecte de posts depuis le feed...")

# Récupération du feed "what's hot"
feed_uri = 'at://did:plc:z72i7hdynmk6r22z27h6tvur/app.bsky.feed.generator/whats-hot'
data = client.app.bsky.feed.get_feed({'feed': feed_uri, 'limit': 100})
feed = data.feed

# Extraction des posts (texte, uri, auteur, etc.)
posts_data = []
for post in feed:
    try:
        record = post.post.record
        post_info = {
            'text': record.text,
            'uri': post.post.uri,
            'author': post.post.author.handle,
            'created_at': record.created_at,
            'like_count': post.post.like_count,
            'repost_count': post.post.repost_count,
            'reply_count': post.post.reply_count
        }
        posts_data.append(post_info)
    except Exception as e:
        print(f"⚠️ Erreur lors du traitement d’un post : {e}")

# Sauvegarde dans un fichier
with open('collected_posts.json', 'w', encoding='utf-8') as f:
    json.dump(posts_data, f, ensure_ascii=False, indent=2)

print(f"✅ {len(posts_data)} posts collectés et enregistrés dans collected_posts.json")

# Charger un URI existant depuis le fichier
if posts_data:
    test_uri = posts_data[0]['uri']
    print(f"🔍 Extraction de détails pour le post : {test_uri}")

    try:
        thread_data = client.app.bsky.feed.get_post_thread({'uri': test_uri})
        print("📄 Contenu du post extrait :")
        print(thread_data.thread.post.record.text)
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction via l'URI : {e}")
else:
    print("❌ Aucun post disponible pour l'extraction.")
