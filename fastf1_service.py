from datetime import datetime, timezone
import fastf1

from fastf1.ergast import Ergast

import pandas as pd
# Ativar o cache (opcional, mas recomendado)
import os
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache('cache')  # pasta onde os dados são guardados

# Configurar o FastF1
ergast = Ergast()

def get_race_results(year: int, round: int):
    try:
        session = fastf1.get_session(year, round, 'R')  # 'R' para Race
        session.load(laps=False, telemetry=False)
        results = session.results[['Abbreviation', 'Position', 'Time', 'Status']]
        return results.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


def get_next_session():
    try:
        ev_schedule = fastf1.get_events_remaining(dt=None, include_testing=True, backend=None, force_ergast=False)
        next_session = ev_schedule.iloc[0]
        ev_race = ergast.get_race_schedule(season=2025, round=next_session.RoundNumber, result_type='raw')
        race_info = ev_race[0]
        date = f"{race_info['date'].date()}T{race_info['time']}"
        print(race_info)
        return {
            "roundNumber": int(next_session.RoundNumber),
            "country": str(next_session.Country),
            "location": str(next_session.Location),
            "circuitName": str(race_info['Circuit']['circuitName']),
            "eventName": str(next_session.EventName),
            "eventDate": str(date),
            "eventDay": str(race_info['date'].date())
        }
    except Exception as e:
        return {"error": str(e)}
    
def get_pilot_classification():
    try:
        standings = ergast.get_driver_standings(season=2025, result_type='raw')

        return [
            {
                "position": driver["position"],
                "driver": f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}",
                "wins": driver["wins"],
                "team": driver["Constructors"][0]["name"],
                "points": driver["points"]
            }
            for driver in standings[0]['DriverStandings']
        ]
    except Exception as e:
        return {"error": str(e)}

def get_team_classification():
    try:
        standings = ergast.get_constructor_standings(season=2025, result_type='raw')
        team_classification = [
            {
                "position": team["position"],
                "team": team["Constructor"]["name"],
                "points": team["points"],
                "wins": team["wins"]
            }
            for team in standings[0]['ConstructorStandings']
        ]
        return team_classification
    except Exception as e:
        return {"error": str(e)}