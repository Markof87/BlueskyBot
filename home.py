
import sys
import os

from taipy.gui import Gui, notify
import datetime
import numpy as np
import plotly.express as px
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from services.readers import extractTopTournaments, extractMatchesByDay

# Stato globale dell'applicazione
state = {
    "top_tournaments": None,
    "matches": None,
    "formation_home": None,
    "formation_away": None,
    "selected_player": ""
}

extractTopTournaments(state)
extractMatchesByDay(state, datetime.datetime.now().strftime('%Y%m%d'), state["top_tournaments"])

# Funzioni per caricare le formazioni (simulazione)
def show_home_formation(match_id: str, team_id: str):
    # In una versione reale effettueresti una richiesta REST
    formation = formations.get(team_id, {})
    state["formation_home"] = formation.get("starters", [])
    notify(f"Formazione Home caricata per il match {match_id}", "info")

def show_away_formation(match_id: str, team_id: str):
    formation = formations.get(team_id, {})
    state["formation_away"] = formation.get("starters", [])
    notify(f"Formazione Away caricata per il match {match_id}", "info")

def update_selected_player(selection: str):
    state["selected_player"] = selection
    notify(f"Giocatore selezionato: {selection}", "info")

print(state["matches"])
state["matches"] = pd.DataFrame(state["matches"])


# Creiamo la GUI in Taipy usando il linguaggio di template
page = f"""
# Match del Giorno - Cyberpunk Dashboard

Questa dashboard mostra le partite del giorno in stile cyberpunk blu.

<|{state['matches']}table|>

"""

# CSS personalizzato in stile cyberpunk blu
css = """
<style>
body {
    background-color: #1e1e2f;
    color: #e3e3e3;
    font-family: 'Courier New', monospace;
    margin: 0;
    padding: 0;
}
h1, h2, h3, h4 {
    color: #00d4ff;
    text-shadow: 0px 0px 8px #00b3cc;
}
button {
    background: linear-gradient(135deg, #00b3cc, #00d4ff);
    color: #1e1e2f;
    border: 2px solid #00b3cc;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}
button:hover {
    background: linear-gradient(135deg, #00d4ff, #00b3cc);
    border: 2px solid #00d4ff;
}
.select-widget__radio label {
    display: block;
    padding: 5px;
    margin: 2px 0;
    border: 1px solid #00b3cc;
    border-radius: 4px;
    cursor: pointer;
}
@media only screen and (max-width: 600px) {
    body {
        font-size: 14px;
    }
    button {
        font-size: 14px;
        padding: 8px 16px;
    }
}
</style>
"""

# Inizializziamo la GUI di Taipy con il template e lo stato globale
gui = Gui(page=page)

# Definisci una funzione di callback per selezionare un match dalla tabella
def select_match(event):
    # 'event' contiene i dati dell'elemento cliccato, convertiamoli in dizionario
    if event:
        match = event["value"]
        state["selected_match"] = match
        # Resettiamo eventuali formazioni e selezioni precedenti
        state["formation_home"] = None
        state["formation_away"] = None
        state["selected_player"] = ""
        notify(f"Match selezionato: {match['match_name']}", "info")

# Avvia la GUI
gui.run(port=8080, use_reloader=True)
