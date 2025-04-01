import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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

st.title("⚽ Partite della Giornata")

partite = [
    {"Partita": "Milan - Inter", "ID": "milan_inter"},
    {"Partita": "Juventus - Roma", "ID": "juve_roma"},
]

for partita in partite:
    if st.button(f"Dettagli {partita['Partita']}"):
        st.session_state.partita_selezionata = partita["ID"]
        st.session_state.pagina = "details"

# Navbar con scelta del campionato e settimana
st.sidebar.title("Navigazione")
campionato = st.sidebar.selectbox("Seleziona il Campionato", ["Serie A", "Premier League", "La Liga", "Bundesliga", "Ligue 1"])
settimana = st.sidebar.date_input("Seleziona la settimana", pd.to_datetime('today'))

# Sezione centrale con partite
st.title("Partite di Calcio della Giornata")
st.write(f"**Campionato**: {campionato}")
st.write(f"**Settimana**: {settimana.strftime('%d %B %Y')}")

# Creazione di dati di esempio per le partite
partite = pd.DataFrame({
    'Partita': ['Juventus vs Milan', 'Napoli vs Roma', 'Inter vs Lazio'],
    'Risultato': ['2-1', '1-1', '3-0'],
    'Data': ['2025-04-01', '2025-04-01', '2025-04-01']
})

# Mostrare le partite della giornata
for index, partita in partite.iterrows():
    with st.expander(f"{partita['Partita']} - {partita['Risultato']}"):
        st.write(f"**Data**: {partita['Data']}")
        st.write("Clicca per dettagli")
        if st.button(f"Dettagli {partita['Partita']}"):
            # Passaggio alla dashboard della partita
            st.session_state.partita_selezionata = partita['Partita']
            st.session_state.risultato = partita['Risultato']

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
