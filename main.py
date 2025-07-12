from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import os
import fitz  # PyMuPDF für PDF-Handling

app = FastAPI()

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

@app.get("/")
def read_root():
    return {"message": "Meta Firma API läuft"}

@app.get("/read_file")
def read_file(filename: str = Query(..., description="Dateiname relativ zum API-Ordner")):
    file_path = os.path.join(BASE_PATH, filename)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=404, content={"error": "Datei nicht gefunden."})
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/list_files")
def list_files(extension: str = None):
    files = []
    for root, dirs, filenames in os.walk(BASE_PATH):
        for name in filenames:
            if not extension or name.endswith(extension):
                relative_path = os.path.relpath(os.path.join(root, name), BASE_PATH)
                files.append(relative_path)
    return {"files": files}

@app.get("/list_tree")
def list_tree():
    tree = {}

    for root, dirs, files in os.walk(BASE_PATH):
        rel_root = os.path.relpath(root, BASE_PATH)
        tree[rel_root] = {"dirs": dirs, "files": files}
    
    return tree

@app.get("/read_pdf")
def read_pdf(filename: str = Query(...)):
    file_path = os.path.join(BASE_PATH, filename)
    if not os.path.isfile(file_path) or not file_path.lower().endswith(".pdf"):
        return JSONResponse(status_code=404, content={"error": "PDF nicht gefunden."})

    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return {"content": text.strip()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/read_log")
def read_log(filename: str = Query(...)):
    file_path = os.path.join(BASE_PATH, filename)
    if not os.path.isfile(file_path) or not file_path.lower().endswith(".log"):
        return JSONResponse(status_code=404, content={"error": "Logdatei nicht gefunden."})
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
from fastapi.responses import HTMLResponse

@app.get("/datenschutz", response_class=HTMLResponse)
async def datenschutz():
    with open("datenschutz.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

from fastapi.responses import HTMLResponse

@app.get("/datenschutz", response_class=HTMLResponse, tags=["Info"])
def datenschutz():
    html_content = """
    <h1>Datenschutzrichtlinie für Chantalle GPT</h1>
    <p><strong>Verantwortlich:</strong> Angelika Jesse, Die 1A Montagehelden</p>
    <p><strong>Kontakt:</strong> <a href="mailto:info@1a-montagehelden.de">info@1a-montagehelden.de</a></p>

    <h2>1. Zweck der Datenverarbeitung</h2>
    <p>Diese GPT-Anwendung unterstützt Monteure, Projektbüro und interne Organisation der 1A Montagehelden durch semantische Analyse, Dateiverwaltung und strukturierte Informationsabfragen.</p>

    <h2>2. Erhobene Daten</h2>
    <ul>
        <li>Texteingaben (z. B. Sprachprotokolle, Projektnotizen)</li>
        <li>Dateinamen und -inhalte (z. B. PDFs, Logs, Projektakten)</li>
        <li>Zeitstempel und strukturbezogene Metadaten</li>
    </ul>

    <h2>3. Keine Weitergabe an Dritte</h2>
    <p>Alle Daten verbleiben auf internen Servern der 1A Montagehelden oder werden im Rahmen privater GPT-Instanzen lokal verarbeitet. Es erfolgt keine Übermittlung an externe Stellen oder OpenAI-Server.</p>

    <h2>4. Speicherdauer</h2>
    <p>Temporäre Daten (wie Sprachnachrichten oder Zwischenspeicher) werden nach Verarbeitung gelöscht. Projektdokumente werden nach den internen Aufbewahrungsrichtlinien verwaltet.</p>

    <h2>5. Nutzerrechte</h2>
    <p>Es gelten die internen Nutzungsrechte der Mitarbeiter und Vertragspartner. Ein externer Zugriff ist nicht vorgesehen. Die Nutzung erfolgt auf Basis betrieblicher Weisung.</p>

    <h2>6. Kontakt und Auskunft</h2>
    <p>Bei Rückfragen zur Datenverarbeitung im Kontext von Chantalle GPT:<br>
    Angelika Jesse<br>
    Die 1A Montagehelden<br>
    <a href="mailto:info@1a-montagehelden.de">info@1a-montagehelden.de</a></p>
    """
    return html_content
