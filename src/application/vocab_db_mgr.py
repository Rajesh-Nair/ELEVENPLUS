from utils.db_manager import SQLiteManager
import os
import pandas as pd
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from collections import defaultdict

class VocabDBManager:
    def __init__(self, db_path=os.path.join("data","vocab.db")):
        self.db_path = db_path
        self.db = SQLiteManager(db_path=db_path)
        if not self.db.table_exists("vocab"):
            self.create_table()    
        self.vocab_columns = self.db.get_column_names("vocab")

    def create_table(self):
        try :
            create_table_query = """
            CREATE TABLE IF NOT EXISTS vocab (
            word TEXT UNIQUE NOT NULL PRIMARY KEY COLLATE NOCASE,
            meaning TEXT,
            usage TEXT,
            etymology TEXT,
            word_break TEXT,
            picture TEXT,
            did_you_know_facts TEXT,
            synonyms TEXT,
            antonyms TEXT,
            additional_facts TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            points INTEGER DEFAULT 10
        );
            """
            self.db.query_execute(create_table_query)
            log.info("Vocab table created")
        except Exception as e:
            log.error("Error creating vocab table", error=str(e))
            raise CustomException("Error creating vocab table : ", e) from e

    def insert_word(self, dict_data, critical=False):
        try :
            input_data = { col : dict_data[col] for col in self.vocab_columns if col not in ['created_at', 'points'] }
            input_data['points'] = 10 if not critical else 15
            input_data['word'] = input_data['word'].lower()
            self.db.insert_json("vocab", input_data)
        except Exception as e:
            log.error(f"Error inserting word {dict_data["word"]}", error=str(e))
            raise CustomException(f"Error inserting word {dict_data["word"]} : ", e) from e

    def get_word(self, word):
        select_query = "SELECT * FROM vocab WHERE word = ?;"
        return self.db.query_fetch(select_query, (word,))
    
    def get_all_words(self):
        select_query = "SELECT word FROM vocab;"
        return [word_dict['word'] for word_dict in self.db.query_fetch_all(select_query)]

    def export_to_csv(self, export_path):
        try:
            select_query = "SELECT * FROM vocab;"
            word_dict = self.db.query_fetch_all(select_query)
            if not word_dict:
                log.warning("No data found in vocab table to export")
            df = pd.DataFrame(word_dict)
            df.to_csv(export_path, index=False)
            log.info(f"Vocab table exported to {export_path}")
        except Exception as e:
            log.error("Error exporting vocab table to CSV", error=str(e))
            raise CustomException("Error exporting vocab table to CSV", e) from e
        

    def get_all_words_for_test(self):
        select_query = "SELECT word, points FROM vocab;"
        vocab_words = self.db.query_fetch_all(select_query)
        return vocab_words
    
    def updated_words_points_for_test(self, vocab_words):
        if not vocab_words or len(vocab_words) == 0:
            return None
        update_query = """UPDATE vocab 
                        SET points = CASE word
                        """
        for word_dict in vocab_words:
            update_query += f"""
                            WHEN '{word_dict['word']}' THEN {word_dict['points']}
                        """
        update_query += """
                        END
                        WHERE word IN ({});""".format(','.join(["'{}'".format(word_dict['word']) for word_dict in vocab_words]))
        self.db.query_execute(update_query)
        return True
    
    def reset_words_points_for_test(self):
        update_query = """UPDATE vocab SET points = 10 WHERE TRUE;"""
        self.db.query_execute(update_query)
        return True

    def close(self):
        self.db.close()

if __name__ == "__main__":
    vocab_db_mgr = VocabDBManager(db_path=os.path.join("data","vocab_11plus.db"))

    # Insert sample word
    # if not vocab_db_mgr.get_word("benevolent"):
    #     vocab_db_mgr.insert_word(
    #         {
    #         'word': 'benevolent', 
    #         'meaning': 'Well meaning and kindly; characterized by or expressing goodwill or kindly feelings.', 
    #         'usage': 'The benevolent king donated a large sum of money to the orphanage.', 
    #         'etymology': "From Latin 'bene' (well) + 'volens' (wishing).", 
    #         'word_break': "Break it down as 'bene-' (good) + 'volent' (wishing) = wishing good things.", 
    #         'picture': 'Imagine a smiling person giving food to the homeless.', 
    #         'did_you_know_facts': 'Benevolence is often associated with philanthropy and charitable giving.', 
    #         'synonyms': 'kind, compassionate, generous, altruistic', 
    #         'antonyms': 'malevolent, cruel, unkind, selfish', 
    #         'additional_facts': "Benevolent is often used to describe someone in a position of power who uses that power for good. A related word is 'beneficial,' which means producing good results or effects."
    #         }

    #     )
    # else :
    #     print("Word 'abandon' already exists in the database.")

    # Retrieve and print the word details
    word_details = vocab_db_mgr.get_word("benevolent")
    print(word_details)

    # fetch all words
    print("All words : {}".format(", ".join(vocab_db_mgr.get_all_words())))

    # update words points for test
    vocab_wordds = [{'word': 'rip', 'points': 15}, 
                    {'word': 'sadder', 'points': 15}, 
                    {'word': 'forgery', 'points': 15}, 
                    {'word': 'clutch', 'points': 15}]
    update_query = vocab_db_mgr.updated_words_points_for_test(vocab_wordds)
    print("update_query : {}".format(update_query))

    # fetch all words for test
    get_all_words_for_test = vocab_db_mgr.get_all_words_for_test()
    print("get_all_words_for_test : {}".format(get_all_words_for_test))

    # reset words points for test
    reset_words_points_for_test = vocab_db_mgr.reset_words_points_for_test()
    print("reset_words_points_for_test : {}".format(reset_words_points_for_test))

    # Close the database connection
    vocab_db_mgr.close()