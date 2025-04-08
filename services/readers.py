import requests
import config

def extractTopTournaments(state):
    url = config.HOME_URL + 'tournaments'
    response = requests.get(url)

    if response.status_code == 200:
        state["top_tournaments"] = response.json()
    else:
        print(f"Errore nella richiesta: {response.status_code}")
        return []

    return state["top_tournaments"]

def extractMatchesByDay(state, date, topTournaments):
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

    state["matches"] = matches_data
    return state["matches"]