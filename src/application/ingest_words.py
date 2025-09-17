import os
import sys
import json

from pathlib import Path


class vocab_manager:
    def __init__(self):
        self.WORD_DB = self.vocab_db_init()

    def vocab_db_init(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent
        data_folder = BASE_DIR / "data"
        with open(os.path.join(data_folder, "sample_vocab.json"), "r", encoding="utf-8") as f:
            WORD_DB = json.load(f)
        return WORD_DB
    
    def vocab_db_read(self, word):
        return self.WORD_DB.get(word.lower(), {})

    
if __name__ == "__main__":
    words = ["abandon", "benevolent", "candid"]
    vocab_mgr = vocab_manager()
    for word in words:
        print(f"Details for word: {word}")
        print(json.dumps(vocab_mgr.vocab_db_read(word), indent=2))
        print("\n")