import streamlit as st
import pandas as pd
import json
import requests
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")
st.title("📍 JAUGE remplissage interactive Vélib’ – Data temps réel")

# URLs API Vélib'
status_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_status.json'
info_url = 'https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole/station_information.json'

# --- Initialisation de session_state
if 'status_file' not in st.session_state:
    st.session_state.status_file = None
if 'information_file' not in st.session_state:
    st.session_state.information_file = None

# --- 1. Boutons de mise à jour
col1, col2 = st.columns(2)
with col1:
    if st.button(" STATUS 👆 JAUGES de remplissages 👆 "):
        try:
            response = requests.get(status_url)
            if response.status_code == 200:
                st.session_state.status_file = response.text
                st.success("✅ Données STATUS téléchargées avec succès.")
            else:
                st.error(f"❌ Erreur STATUS {response.status_code}")
        except Exception as e:
            st.error(f"❌ Erreur de téléchargement STATUS : {e}")

with col2:
    if st.button(" INFO 👆 COORD. des stations 👆 "):
        try:
            response = requests.get(info_url)
            if response.status_code == 200:
                st.session_state.information_file = response.text
                st.success("✅ Données INFO téléchargées avec succès.")
            else:
                st.error(f"❌ Erreur INFO {response.status_code}")
        except Exception as e:
            st.error(f"❌ Erreur de téléchargement INFO : {e}")

# --- Vérification que les deux fichiers sont présents
if not st.session_state.status_file or not st.session_state.information_file:
    st.info("👆 Cliquez sur les deux boutons STATUS et INFO pour bien charger toutes les données.")
    st.stop()

# --- 2. Charger les données JSON
status_data = json.loads(st.session_state.status_file)
info_data = json.loads(st.session_state.information_file)

status_df = pd.DataFrame(status_data['data']['stations'])
info_df = pd.DataFrame(info_data['data']['stations'])
df = pd.merge(status_df, info_df, on="station_id")

# --- 3. Horodatage global (lastUpdatedOther)
try:
    timestamp = status_data.get("lastUpdatedOther")
    if timestamp:
        dt_obj = datetime.utcfromtimestamp(timestamp)
        formatted_time = dt_obj.strftime("%H:%M:%S - %d/%m/%Y")
    else:
        formatted_time = "Heure inconnue"
except Exception as e:
    formatted_time = f"Erreur horodatage global : {e}"

# --- 4. Timestamp par station (last_reported)
df['last_reported_str'] = df['last_reported'].apply(
    lambda ts: datetime.utcfromtimestamp(ts).strftime("%H:%M:%S - %d/%m/%Y")
)

# --- 5. Traitement des données
df['availability_ratio'] = df['num_bikes_available'] / df['capacity']

def classify(row):
    if row['num_bikes_available'] == 0:
        return "🖤 0 vélo dispo"
    elif 1 <= row['num_bikes_available'] <= 2:
        return "🔴 1-2 vélos"
    elif abs(row['availability_ratio'] - 0.4) <= 0.05:
        return "🟢 ~40% dispo"
    elif row['availability_ratio'] >= 0.8:
        return "🔵 ≥80% dispo"
    else:
        return None

df['categorie'] = df.apply(classify, axis=1)
df = df.dropna(subset=["categorie"])
df["mécaniques"] = df["num_bikes_available_types"].apply(lambda x: x[0].get("mechanical", 0))
df["électriques"] = df["num_bikes_available_types"].apply(lambda x: x[1].get("ebike", 0))

# --- 6. Affichage timestamps
st.markdown(f"### 🕒 Mise à jour globale (lastUpdatedOther) : `{formatted_time}`")
st.markdown("⏱️ * M. à j. ttes les 3600 sec. par Smovengo. *")

# --- 7. Affichage carte interactive
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="name",
    hover_data={
        "categorie": True,
        "num_bikes_available": True,
        "mécaniques": True,
        "électriques": True,
        "capacity": True,
        "availability_ratio": ':.1%',
        "last_reported_str": True
    },
    color="categorie",
    color_discrete_map={
        "🖤 0 vélo dispo": "black",
        "🔴 1-2 vélos": "red",
        "🟢 ~40% dispo": "green",
        "🔵 ≥80% dispo": "blue"
    },
    zoom=12,
    height=600
)

fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)
