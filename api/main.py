import os
import json
from pathlib import Path  
from typing import Dict, List, Any

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

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

# Example database
data_folder = BASE_DIR / "data"
print(os.path.join(data_folder,"sample_vocab.jsonl"))
# Open and load the JSON file
with open(os.path.join(data_folder,"sample_vocab.json"), "r", encoding="utf-8") as f:
    WORD_DB = json.load(f)

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    resp = templates.TemplateResponse("index.html", {"request": request})
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.get("/api/words")
def get_words() -> List[str]:
    return list(WORD_DB.keys())

@app.get("/api/word")
def get_word(word: str = Query(...)) -> Dict[str, Any]:
    return WORD_DB.get(word.lower(), {})

@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "vocabulary-card"}




# command for executing the fast api
# uvicorn api.main:app --port 8080 --reload    
#uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload


