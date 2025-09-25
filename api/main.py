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
from src.application.generate_vocabtest import GenerateVocabTest
from src.application.test_db_mgr import TestDBManager

from logger import GLOBAL_LOGGER as log

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
    resp = templates.TemplateResponse("index_new.html", {"request": request})
    resp.headers["Cache-Control"] = "no-store"
    return resp

# Get request to serve the original UI
@app.get("/original", response_class=HTMLResponse)
async def serve_original_ui(request: Request):
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
async def add_word(request: Request) -> dict:
    # Get the raw body as text
    body = await request.body()
    word_list = body.decode('utf-8')
    
    log.info(f"Adding words: {word_list}")
    ingestor = IngestWords()
    ingest_status = ingestor.ingest_wordlist(word_list.split())
    ingestor.close()
    return {"total-words":len(word_list.split()), 
            "failed-count": len(ingest_status.get("failed", [])),
            "failed-words": ingest_status.get("failed", []),
            "skipped-count": len(ingest_status.get("exists", [])),
            "skipped-words": ingest_status.get("exists", [])}

# request to generate vocab tests
@app.post("/api/vocabtest")
async def post_test(request: Request) -> dict:
    body = await request.body()
    test_type = body.decode('utf-8')
    log.info(f"Generating vocab test for type: {test_type}")
    generator = GenerateVocabTest(test_type=test_type)
    result = generator.generate_tests()
    generator.close()   
    return result

# request to get all tests
@app.get("/api/vocabtest")
async def get_test(testtype: int = Query(...)) -> List[Dict[str, Any]]:
    log.info(f"Getting vocab test for type: {testtype}")
    generator = GenerateVocabTest(test_type=testtype)
    result = generator.retrieve_test()
    generator.close()
    return result

# request to get test summary
@app.get("/api/vocabtest/summary")
async def get_all_test_summary() -> List[Dict[str, Any]]:
    log.info(f"Getting vocab test summary")
    test_db_mgr = TestDBManager()
    result = test_db_mgr.get_all_test_summary()
    test_db_mgr.close()
    return result
    

# command for executing the fast api
# uvicorn api.main:app --port 8080 --reload    
# uvicorn api.main:app --host 0.0.0.0 --port 8080 --reload