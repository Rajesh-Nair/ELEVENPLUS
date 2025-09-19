from pydantic import BaseModel


class WordInfo(BaseModel):
    word: str
    meaning: str
    usage: str
    etymology: str
    word_break: str
    picture: str
    dyk_facts: str
    synonyms: list[str]
    antonyms: list[str]
    additional_facts: str

class PromptType(str, Enum):
    RETRIEVE_VOCABINFO = "retrieve_vocabinfo_prompt"

