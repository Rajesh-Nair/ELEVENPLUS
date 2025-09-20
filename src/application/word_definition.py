import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.output_parsers import JsonOutputParser

from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from prompt.prompt_library import PROMPT_REGISTRY
from model.model import WordInfo, PromptType
from utils.model_loader import ModelLoader

# Access vocab database
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

# Enhance vocab info - for maintenance
class vocab_enhancer:
    def __init__(self):
        load_dotenv()
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.prompt = PROMPT_REGISTRY[PromptType.RETRIEVE_VOCABINFO]
        self.parser = JsonOutputParser(pydantic_object=WordInfo)
        self.chain = self.prompt | self.llm | self.parser
        log.info("vocab enhancer initialized", model=self.llm)

    def enhance_word_info(self, word) -> dict:
        # Placeholder for enhancement logic
        # e.g., add synonyms, usage examples, etc.
        try:
            input = {"input_word": word}
            return self.chain.invoke(input)
        except Exception as e:
            log.error(f"Error enhancing word info for {word}", error=str(e))
            raise CustomException(f"Error enhancing word info for {word}", sys)
    
if __name__ == "__main__":
    words = ["abandon", "benevolent", "candid"]
    vocab_mgr = vocab_enhancer()
    for word in words:
        print(f"Details for word: {word}")
        print(json.dumps(vocab_mgr.enhance_word_info(word), indent=2))
        print("\n")
    print("Ingestion complete.")