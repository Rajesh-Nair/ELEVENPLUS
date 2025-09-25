from src.application.word_definition import vocab_enhancer
from src.application.vocab_db_mgr import VocabDBManager
import os
import json
from collections import defaultdict

from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

class IngestWords:
    def __init__(self):
        self.vocab_enhancer = vocab_enhancer()
        self.db_mgr = VocabDBManager(db_path=os.path.join("data","vocab_11plus.db"))
        
  
    def ingest_word(self, word, critical=False):
        try:
            # Check if word already exists
            existing = self.db_mgr.get_word(word.lower())
            if existing :
                log.info(f"Word '{word}' already exists in DB. Skipping.")
                return {word: "exists"}

            # Enhance with LLM
            enhanced_info = self.vocab_enhancer.enhance_word_info(word)
            log.info(f"Enhanced info for '{word}': {enhanced_info}")
            if not enhanced_info or 'word' not in enhanced_info or not enhanced_info['word']:
                log.error(f"Enhanced info for '{word}' is invalid: {enhanced_info}")
                return {word: "failed"}
            

            # Insert into DB
            self.db_mgr.insert_word(enhanced_info, critical)
            log.info(f"Inserted word '{word}' into DB.")
            return {word: "inserted"}

        except Exception as e:
            log.error(f"Error ingesting word '{word}'", error=str(e))
            return {word: "failed"}
        
    def ingest_wordlist(self, wordlist, critical=False):
        ingest_counter = defaultdict(list)
        for word in wordlist:
            word = word.lower()
            status = self.ingest_word(word, critical)
            ingest_counter[status[word]].append(word)
        return dict(ingest_counter)

    def retrieve_all_words(self):
        return self.db_mgr.get_all_words()
    
    def retrieve_word(self, word):
        return self.db_mgr.get_word(word.lower())

    def close(self):
        self.db_mgr.close()

if __name__ == "__main__":
    words = ["belligerent","candid"]
    ingestor = IngestWords()
    ingest_status = ingestor.ingest_wordlist(words)
    print("Ingestion complete. Total words:{}\n \
    {} failed - {}\n \
    {} skipped - {}".format(len(words), \
        len(ingest_status.get("failed", [])), \
        ingest_status.get("failed", []), \
        len(ingest_status.get("exists", [])), \
        ingest_status.get("exists", [])))
    
    # Export to CSV
    ingestor.db_mgr.export_to_csv("data/vocab_11plus_export.csv")
    print("Exported vocab to data/vocab_11plus_export.csv")

    ingestor.close()
    
