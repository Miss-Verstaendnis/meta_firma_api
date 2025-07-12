from fastapi import FastAPI, HTTPException, Query
import requests
from pathlib import Path
import pandas as pd

app = FastAPI()

BASE_API = "http://127.0.0.1:8000"
BASE_DIR = Path(__file__).resolve().parent

@app.get("/ping")
def ping():
    return {"message": "Bridge aktiv"}

@app.get("/bridge_read_file")
def bridge_read_file(path: str = Query(..., description="Pfad zur Datei innerhalb von Meta_Firma")):
    try:
        response = requests.get(f"{BASE_API}/read_file", params={"path": path})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bridge_read_excel")
def bridge_read_excel(path: str = Query(..., description="Pfad zur Excel-Datei innerhalb von Meta_Firma")):
    try:
        response = requests.get(f"{BASE_API}/read_excel", params={"path": path})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
