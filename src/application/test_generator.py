import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.output_parsers import JsonOutputParser

from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from prompt.prompt_library import PROMPT_REGISTRY
from model.model import Test1, PromptType
from utils.model_loader import ModelLoader

# Generate tests for vocab
class test_generator:
    def __init__(self, test_type=1):  
        load_dotenv()
        self.loader = ModelLoader()
        self.llm = self.loader.load_llm()
        self.prompt = PROMPT_REGISTRY[PromptType.TEST_VOCAB_TYPE1]
        self.parser = JsonOutputParser(pydantic_object=Test1)
        self.chain = self.prompt | self.llm | self.parser
        log.info("test generator initialized", model=self.llm)

    def generate_test(self, word_list) -> dict:
        # Placeholder for enhancement logic
        # e.g., add synonyms, usage examples, etc.
        try:            
            input = {"words": ' '.join([word['word'] for word in word_list])}
            return self.chain.invoke(input)
        except Exception as e:
            log.error(f"Error generating test for {word_list}", error=str(e))
            raise CustomException(f"Error generating test for {word_list}", sys)
    
if __name__ == "__main__":
    words = ["abandon", "benevolent", "candid"]
    test_mgr = test_generator()
    result = test_mgr.generate_test(words)
    print("result : {}".format(result))

    print("Test generation complete.")