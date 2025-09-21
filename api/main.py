import os
import json
from pathlib import Path  
from typing import Dict, List, Any

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.application.ingest_words import IngestWords

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="Vocabulary Card", version="0.1")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get request to serve the UI
@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    resp = templates.TemplateResponse("index.html", {"request": request})
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.get("/api/words")
def get_words() -> List[str]:
    ingestor = IngestWords()
    output = ingestor.retrieve_all_words()
    ingestor.close()
    return output if output else []

@app.get("/api/word")
def get_word(word: str = Query(...)) -> Dict[str, Any]:
    ingestor = IngestWords()
    output = ingestor.retrieve_word(word)
    ingestor.close()
    return output if output else {}


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "vocabulary-card"}

# Post requests for adding/updating/deleting words can be added here
@app.post("/api/addword")
async def add_word(word_list: str) -> JSONResponse:
    ingestor = IngestWords()
    ingest_status = ingestor.ingest_wordlist(word_list.split())
    ingestor.close()
    return {"total-words":len(word_list.split()), 
            "failed-count": len(ingest_status.get("failed", [])),
            "failed-words": ingest_status.get("failed", []),
            "skipped-count": len(ingest_status.get("exists", [])),
            "skipped-words": ingest_status.get("exists", [])}
    


# command for executing the fast api
# uvicorn api.main:app --port 8080 --reload    
#uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload


