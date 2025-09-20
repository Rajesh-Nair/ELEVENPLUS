from utils.db_manager import SQLiteManager
import os

from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

class VocabDBManager:
    def __init__(self, db_path=os.path.join("data","vocab.db")):
        self.db = SQLiteManager(db_path=db_path)
        if not self.db.table_exists("vocab"):
            self.create_table()    

    def create_table(self):
        try :
            create_table_query = """
            CREATE TABLE IF NOT EXISTS vocab (            
                word TEXT UNIQUE NOT NULL PRIMARY KEY,
                meaning TEXT,
                usage TEXT,
                etymology TEXT,
                word_break TEXT,
                picture TEXT,
                did_you_know_facts TEXT,
                synonyms TEXT,
                antonyms TEXT,
                additional_facts TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            self.db.query_execute(create_table_query)
            log.info("Vocab table created")
        except Exception as e:
            log.error("Error creating vocab table", error=str(e))
            raise CustomException("Error creating vocab table : ", e) from e

    def insert_word(self, json_data):
        try :
            self.db.insert_json("vocab", json_data)
        except Exception as e:
            log.error(f"Error inserting word {json_data["word"]}", error=str(e))
            raise CustomException(f"Error inserting word {json_data["word"]} : ", e) from e

    def get_word(self, word):
        select_query = "SELECT * FROM vocab WHERE word = ?;"
        return self.db.query_fetch(select_query, (word,))

    def close(self):
        self.db.close()

if __name__ == "__main__":
    vocab_db_mgr = VocabDBManager(db_path=os.path.join("data","vocab.db"))

    # Insert sample word
    vocab_db_mgr.insert_word(
        {
        "word":"abandon",
        "meaning":"to leave behind or give up",
        "usage":"He had to abandon his car in the snow.",
        "etymology":"from Old French abandoner, from a bandon 'control, power'",
        "word_break":"a-ban-don",
        "picture":"http://example.com/abandon.jpg",
        "did_you_know_facts":"The word 'abandon' can also mean to act without restraint.",
        "synonyms":"forsake, desert, leave",
        "antonyms":"keep, maintain, continue",
        "additional_facts":"1) Homograph: 'abandon' can be a noun meaning complete lack of inhibition. 2) Often used in legal contexts.",
        #"created_at": "2025-09-20T23:25:10.934833Z"
        }
    )

    # Retrieve and print the word details
    word_details = vocab_db_mgr.get_word("abandon")
    print(word_details)

    # Close the database connection
    vocab_db_mgr.close()