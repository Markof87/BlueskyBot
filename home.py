import requests

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import config
import utils
import reports
import webbrowser
from io import BytesIO
from PIL import Image

def image_creator(url, event_name, name, opponent):

    response = requests.get(url)
    # Assicurati che la richiesta sia andata a buon fine
    if response.status_code == 200:
        match_data = response.json()
    else:
        print(f"Errore nella richiesta: {response.status_code}")

    img_buffer = reports.getEventReport(match_data, event_name, name, opponent, pitch_color='#FFFFFF')
    img_buffer.seek(0)
    image_data = utils.compress_image(img_buffer.read(), target_size_kb=976.56, initial_resize_factor=1.0)

    image = Image.open(BytesIO(image_data))
    image.show()

    with open('report_image.png', 'wb') as f:
        f.write(image_data)
    print("Immagine salvata come debug_image.png per verifica.")

    if not image_data:
        print("Errore: Il buffer dell'immagine è vuoto.")
        exit(1)

    #upload = client.com.atproto.repo.upload_blob(image_data, timeout=120)

home_url = config.HOME_URL

if "partita_selezionata" not in st.session_state:
    st.session_state.partita_selezionata = None

if "risultato" not in st.session_state:
    st.session_state.risultato = None

if "pagina" not in st.session_state:
    st.session_state.pagina = None

# Funzione per lo stile cyberpunk migliorato
def add_css():
    st.markdown("""
    <style>
    /* Body */
    body {
        background-color: #1e1e2f;
        color: #e3e3e3;
        font-family: 'Courier New', monospace;
    }

    /* Navbar */
    .sidebar .sidebar-content {
        background-color: #2a2a3b;
        color: #00b3cc;
    }

    .stSidebar .stSidebarMenuButton {
        background-color: #00b3cc;
        color: white;
        padding: 12px;
        font-size: 14px;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }

    .stSidebar .stSidebarMenuButton:hover {
        background-color: #00d4ff;
    }

    /* Bottoni */
    .stButton>button {
        background: linear-gradient(135deg, #00b3cc, #00d4ff);
        color: #1e1e2f;
        border: 2px solid #00b3cc;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px 0 rgba(0, 179, 204, 0.8);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #00d4ff, #00b3cc);
        border: 2px solid #00d4ff;
        box-shadow: 0 0 20px 0 rgba(0, 179, 204, 1);
    }

    /* Selezioni */
    .stSelectbox, .stSlider, .stTextInput, .stDateInput {
        background-color: #2a2a3b;
        border: 1px solid #00b3cc;
        color: white;
    }

    /* Titoli */
    .stTitle, .stHeader {
        color: #00d4ff;
        text-shadow: 0 0 8px rgba(0, 179, 204, 1);
    }

    /* Espansioni */
    .stExpanderHeader {
        color: #00d4ff;
        font-weight: bold;
    }
    .stExpanderHeader:hover {
        color: #00b3cc;
    }

    /* Grafici */
    .plotly-graph-div {
        background-color: #2a2a3b;
        border: 2px solid #00b3cc;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# Aggiungere il CSS custom per lo stile cyberpunk
#add_css()

url = home_url + 'tournaments'
# Fai la richiesta GET per ottenere i dati
response = requests.get(url)

# Assicurati che la richiesta sia andata a buon fine
if response.status_code == 200:
    topTournaments = response.json()
else:
    print(f"Errore nella richiesta: {response.status_code}")

url = home_url + 'matchesbydate/20250331'
response = requests.get(url)

if response.status_code == 200:
    matches = response.json()
else:
    print(f"Errore nella richiesta: {response.status_code}")

matches_data = []
for tournament in matches["tournaments"]:
    if tournament["tournamentId"] in [t["id"] for t in topTournaments["topTournaments"]]:
        for match in tournament["matches"]:
            matches_data.append({
                "homeTeamName": match["homeTeamName"],
                "awayTeamName": match["awayTeamName"],
                "homeTeamId": match["homeTeamId"],
                "awayTeamId": match["awayTeamId"],
                "match_name": f"{match['homeTeamName']} - {match['awayTeamName']}",
                "score": f"{match['homeScore']} - {match['awayScore']}" if match["homeScore"] is not None and match["awayScore"] is not None else "In corso",
                "tournament_name": tournament["tournamentName"],
                "tournament_id" : tournament["tournamentId"],
                "id": match["id"]
            })

st.sidebar.title("Navigazione")

if not topTournaments == None:
    campionato = st.sidebar.selectbox("Seleziona il Campionato", options=[(tournament["tournament_name"], tournament["id"], tournament["region"]) for tournament in topTournaments['topTournaments']], format_func=lambda x: x[0])
    selected_campionato_id = campionato[1]
settimana = st.sidebar.date_input("Seleziona la settimana", pd.to_datetime('today'))

# Sezione centrale con partite
st.title("Partite di Calcio del giorno")
#st.write(f"**Campionato**: {campionato}")
#st.write(f"**Settimana**: {settimana.strftime('%d %B %Y')}")

# Mostrare le partite della giornata
for match_data in matches_data:
    with st.expander(f"{match_data['match_name']} - {match_data['score']}"):
        #st.write(f"**Data**: {partita['Data']}")
        colHome, colAway = st.columns(2)

        with colHome:
            st.write(f"**{match_data['homeTeamName']}**")
            if st.button("Passaggi", key=f"home_pass_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["homeTeamId"]}/event/Pass', 'Pass', match_data['homeTeamName'], match_data['awayTeamName'])
            if st.button("Contrasti", key=f"home_tackle_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["homeTeamId"]}/event/Tackle', 'Tackle', match_data['homeTeamName'], match_data['awayTeamName'])

        with colAway:
            st.write(f"**{match_data['awayTeamName']}**")
            if st.button("Passaggi", key=f"away_pass_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["awayTeamId"]}/event/Pass', 'Pass', match_data['awayTeamName'], match_data['homeTeamName'])
            if st.button("Contrasti", key=f"away_tackle_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["awayTeamId"]}/event/Tackle', 'Tackle', match_data['awayTeamName'], match_data['homeTeamName'])
            # Passaggio alla dashboard della partita
            #st.session_state.partita_selezionata = match_data['match_name']
            #st.session_state.risultato = match_data['score']

# Dashboard della partita
if 'partita_selezionata' in st.session_state and st.session_state.partita_selezionata is not None:
    partita = st.session_state.partita_selezionata
    risultato = st.session_state.risultato
    st.header(f"Dashboard - {partita}")
    st.write(f"**Risultato**: {risultato}")
    
    # Selezione dati da analizzare
    opzioni_report = ["Passaggi", "Tiri", "Contrasti", "Tutti i Dati"]
    report = st.selectbox("Seleziona i dati da visualizzare", opzioni_report)
    
    if report != "Tutti i Dati":
        st.write(f"Analizzando: {report}")
    else:
        st.write("Analizzando tutti i dati")

    # Esempio di grafico per visualizzare i dati (grafico casuale)
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    fig = px.line(x=x, y=y, title=f"Statistiche {report}")
    st.plotly_chart(fig)

    # Mostrare le formazioni (dati fittizi)
    st.write("**Formazioni**:")
    st.write("Giocatori squadra 1: [Giocatore 1, Giocatore 2, ...]")
    st.write("Giocatori squadra 2: [Giocatore 1, Giocatore 2, ...]")

    # Selezione giocatore per report
    giocatore = st.selectbox("Scegli un giocatore per report", ["Giocatore 1", "Giocatore 2", "Giocatore 3"])
    if giocatore:
        st.write(f"Report per {giocatore}:")
        # Mostra il report del giocatore (grafico casuale)
        fig = px.line(x=x, y=np.cos(x), title=f"Statistiche {giocatore}")
        st.plotly_chart(fig)
