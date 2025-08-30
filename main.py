from fastapi import FastAPI
from fastf1_service import get_race_results
from fastf1_service import get_next_session
from fastf1_service import get_pilot_classification, get_team_classification


app = FastAPI()

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

@app.get("/")
def root():
    return {"message": "API FastF1 ativa"}

@app.get("/race/{year}/{round}")
def race_results(year: int, round: int):
    return get_race_results(year, round)

@app.get("/next_session")
def next_session():
    return get_next_session()

@app.get("/classification/pilots")
def pilot_classification():
    return get_pilot_classification()

@app.get("/classification/teams")
def team_classification():
    return get_team_classification()