import datetime
import requests
import locale

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

@st.fragment
def lazy_expander(
    title: str,
    key: str,
    on_expand,
    expanded: bool = False,
    callback_kwargs: dict = None
):
    """
    A 'lazy' expander that only loads/renders content on expand.

    Args:
        title (str): Title to show beside the arrow.
        key (str): Unique key for storing expanded state in st.session_state.
        on_expand (callable): A function that takes a container (and optional kwargs)
                              to fill with content *only* after expanding.
        expanded (bool): Initial state (collapsed=False by default).
        callback_kwargs (dict): Extra kwargs for on_expand() if needed.
    """
    if callback_kwargs is None:
        callback_kwargs = {}

    # Initialize session state in the first run
    if key not in st.session_state:
        st.session_state[key] = expanded

    outer_container = st.container(border=True)

    arrows = ["▼", "▲"]  # down, up
    arrow_keys = ["down", "up"]

    with outer_container:
        col1, col2 = st.columns([0.9, 0.1])
        col1.write(f"**{title}**")

        if col2.button(
            arrows[int(st.session_state[key])],
            key=f"{key}_arrow_{arrow_keys[int(st.session_state[key])]}"
        ):
            # If currently collapsed -> expand and call on_expand
            if not st.session_state[key]:
                st.session_state[key] = True
                on_expand(outer_container, **callback_kwargs)

            # If currently expanded -> collapse (force a rerun)
            else:
                st.session_state[key] = False
                st.rerun()


def build_match_panel(container, match_data):
    home_url = config.HOME_URL
    print(match_data)
    with container:
        colHomeFormation, colHomeReports, colAwayFormation, colAwayReports = st.columns(4)

        with colHomeFormation:
            url_home_formation = home_url + f'match/{match_data["id"]}/team/home'
            response = requests.get(url_home_formation)

            if response.status_code == 200:
                home_formation = response.json()
            else:
                print(f"Errore nella richiesta: {response.status_code}")
            #with st.form(key='player_selection_form'):
            st.write(f"**Formazione {match_data['homeTeamName']}**")
            starters = [player for player in home_formation[:11]]
            bench = [player for player in home_formation[11:] if player['stats'] != {}]

            def update_selected_home_player():
                st.session_state.selected_player = st.session_state.get(f"home_players_{match_data['homeTeamId']}")

            titolari_home = st.radio("Titolari", [f"{player['name']}" for player in starters], key=f"home_players_{match_data['homeTeamId']}", on_change=update_selected_home_player)
                #panchina = st.radio("Panchina", [f"{player['name']}" for player in bench] if bench else [], key=f"home_players_bench_{match_data['homeTeamId']}")
            st.write(f"Giocatore selezionato tra i titolari: {titolari_home}")
            #    submit_button = st.form_submit_button(label='Conferma Selezione')


        with colAwayFormation:
            url_away_formation = home_url + f'match/{match_data["id"]}/team/away'
            response = requests.get(url_away_formation)

            if response.status_code == 200:
                away_formation = response.json()
            else:
                print(f"Errore nella richiesta: {response.status_code}")

            st.write(f"**Formazione {match_data['awayTeamName']}**")
            starters = [player for player in away_formation[:11]]
            def update_selected_away_player():
                st.session_state.selected_player = st.session_state.get(f"away_players_{match_data['awayTeamId']}")

            titolari_away = st.radio("Titolari", [f"{player['name']}" for player in starters], key=f"away_players_{match_data['awayTeamId']}", on_change=update_selected_away_player)
                #panchina = st.radio("Panchina", [f"{player['name']}" for player in bench] if bench else [], key=f"away_players_bench_{match_data['awayTeamId']}")
            st.write(f"Giocatore selezionato tra i titolari: {st.session_state.selected_player }")
        
        with colHomeReports:
            st.write(f"**Report {match_data['homeTeamName']}**")
            if st.button("Passaggi", key=f"home_pass_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["homeTeamId"]}/event/Pass', 'Pass', match_data['homeTeamName'], match_data['awayTeamName'])
            if st.button("Contrasti", key=f"home_tackle_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["homeTeamId"]}/event/Tackle', 'Tackle', match_data['homeTeamName'], match_data['awayTeamName'])

        with colAwayReports:
            st.write(f"**Report {match_data['awayTeamName']}**")
            if st.button("Passaggi", key=f"away_pass_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["awayTeamId"]}/event/Pass', 'Pass', match_data['awayTeamName'], match_data['homeTeamName'])
            if st.button("Contrasti", key=f"away_tackle_{match_data['id']}"):
                image_creator(home_url + f'match/{match_data["id"]}/team/{match_data["awayTeamId"]}/event/Tackle', 'Tackle', match_data['awayTeamName'], match_data['homeTeamName'])


@st.cache_data
def extractTopTournaments():
    url = config.HOME_URL + 'tournaments'
    response = requests.get(url)

    if response.status_code == 200:
        topTournaments = response.json()
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return []

    return topTournaments

@st.cache_data
def extractMatchesByDay(date, topTournaments):
    url = config.HOME_URL + 'matchesbydate/' + date
    response = requests.get(url)

    if response.status_code == 200:
        matches = response.json()
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return []

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
                    "tournament_id": tournament["tournamentId"],
                    "id": match["id"]
                })
    return matches_data

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

    with open('temp_image.png', 'wb') as temp_file:
        temp_file.write(image_data)
    webbrowser.open('temp_image.png')

    print("Immagine salvata come debug_image.png per verifica.")

    if not image_data:
        print("Errore: Il buffer dell'immagine è vuoto.")
        exit(1)

    #upload = client.com.atproto.repo.upload_blob(image_data, timeout=120)
def write_on_change(data):
    print(data)
    selected_player = st.session_state.selected_player
    if selected_player:
        st.session_state.selected_player = selected_player
    else:
        st.session_state.selected_player = None
    print(f"Selected player: {selected_player}")

if 'topTournaments' not in st.session_state:
    st.session_state.top_tournaments = None

if 'matches_data' not in st.session_state:
    st.session_state.matches_data = None

if 'selected_player' not in st.session_state:
    st.session_state.selected_player = None

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
                
    .stMainBlockContainer {
        max-width: none;
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
add_css()

if(st.session_state.top_tournaments == None):
    topTournaments = extractTopTournaments()
    st.session_state.top_tournaments = topTournaments

else:
    topTournaments = st.session_state.top_tournaments

if(st.session_state.matches_data == None):
    today_date = datetime.datetime.now().strftime('%Y%m%d')
    matches_data = extractMatchesByDay(today_date, topTournaments) 
    st.session_state.matches_data = matches_data

st.sidebar.title("Menu")

if not topTournaments == None:
    campionato = st.sidebar.selectbox("Seleziona il Campionato", options=[(tournament["tournament_name"], tournament["id"], tournament["region"]) for tournament in topTournaments['topTournaments']], format_func=lambda x: x[0])
    selected_campionato_id = campionato[1]
    
giornata = st.sidebar.date_input("Seleziona il giorno", pd.to_datetime('today'))
if giornata:
    matches_data = extractMatchesByDay(giornata.strftime('%Y%m%d'), topTournaments)
    st.session_state.matches_data = matches_data

# Sezione centrale con partite
st.title("Match del giorno")
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')
st.write(f"**Giornata**: {giornata.strftime('%d %B %Y')}")

# Mostrare le partite della giornata
for match_data in matches_data:

    lazy_expander(f"{match_data['match_name']} - {match_data['score']}", f"match_{match_data['id']}", on_expand=build_match_panel, expanded=False, callback_kwargs={'match_data': match_data})

    #with st.expander(f"{match_data['match_name']} - {match_data['score']}"):
        #st.write(f"**Data**: {partita['Data']}")

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
