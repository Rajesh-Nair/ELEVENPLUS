from pydantic import BaseModel
from enum import Enum

class WordInfo(BaseModel):
    Word: str
    Meaning: str
    Usage: str
    Etymology: str
    Word_break: str
    Picture: str
    Did_you_know_facts: str
    Synonyms: str
    Antonyms: str
    Additional_facts: str

class Test1(BaseModel):
    Questions: str
    Answers: str

class PromptType(str, Enum):
    RETRIEVE_VOCABINFO = "retrieve_vocabinfo_prompt"
    TEST_VOCAB_TYPE1 = "TestVocab_type1_prompt"

