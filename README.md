# velib

# 🚲 JAUGE remplissage  - Carte interactive Vélib’ – Données temps réel

Cette application Streamlit vous permet de visualiser la disponibilité des vélos Vélib’ à Paris en temps réel.  
Elle exploite les données ouvertes fournies par Smovengo via l’API officielle GBFS.

status_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json'

info_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json'

## 🗺️ Fonctionnalités

- 🔄 Bouton **STATUS** : télécharge les données en temps réel des stations (`station_status.json`)

- 🔄 Bouton **INFO** : télécharge les données de métadonnées des stations (`station_information.json`)

- 🕒 Affichage de :
  - L’**heure de dernière mise à jour globale** (`lastUpdatedOther`)
  - L’**heure de dernière mise à jour individuelle** pour chaque station (`last_reported`)

- 📍 Carte interactive avec couleurs :
  - "🖤 0 vélo dispo": "black",
  - "🔴 ≤2 vélos": "red",
  - "🟢 ≤40% dispo": "green",
  - "🔵 ≤80% dispo": "blue",
  - "🌸 >80% dispo": "pink"

- 📊 Détail affiché au survol : vélos mécaniques, électriques, capacité totale

## ▶️ Lancer l’application localement

### 1. Cloner le dépôt

git clone https://github.com/votre-utilisateur/velib-streamlit-app.git
cd velib-streamlit-app

2. Installer les dépendances

pip install -r requirements.txt

3. Lancer l’application

streamlit run app_velib.py

Fichier principal : app_velib.py

📦 Fichiers inclus

app_velib.py — Application principale

requirements.txt — Dépendances Python

README.md — Ce fichier

📡 Source des données

Données Open Data Vélib’ (Smovengo)
https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/

Format GBFS (General Bikeshare Feed Specification)
https://github.com/NABSA/gbfs

🙌 Contributeurs
Projet Data Product Manager — DataScientest

Partagé avec ❤️ par Vince

