from utils.db_manager import SQLiteManager
import os
import pandas as pd
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from collections import defaultdict

class TestDBManager:
    def __init__(self, db_path=os.path.join("data","vocab_testset.db")):
        self.db_path = db_path
        self.db = SQLiteManager(db_path=db_path)
        if not self.db.table_exists("vocab_testset"):
            self.create_table()    
        self.testset_columns = self.db.get_column_names("vocab_testset")

    def create_table(self):
        try :
            create_table_query = """
            CREATE TABLE IF NOT EXISTS vocab_testset (
            testtype INTEGER NOT NULL,
            testno INTEGER NOT NULL,
            words TEXT NOT NULL,
            location TEXT NOT NULL,
            PRIMARY KEY (testtype,testno)
            );
            """
            self.db.query_execute(create_table_query)
            log.info("vocab_testset table created")
        except Exception as e:
            log.error("Error creating vocab_testset table", error=str(e))
            raise CustomException("Error creating vocab_testset table : ", e) from e

    def insert_test(self, dict_data):
        try :
            input_data = { col : dict_data[col] for col in self.testset_columns }
            self.db.insert_json("vocab_testset", input_data)
        except Exception as e:
            log.error(f"Error inserting test", error=str(e))
            raise CustomException(f"Error inserting test : ", e) from e

    def get_all_test_summary(self):
        select_query = """SELECT testtype, max(testno) as last_test, count(testno) as test_count 
        FROM vocab_testset GROUP BY testtype;"""
        return self.db.query_fetch_all(select_query)

    def get_test_summary(self, test_type):
        select_query = """SELECT testtype, max(testno) as last_test, count(testno) as test_count 
        FROM vocab_testset WHERE testtype = ? GROUP BY testtype;"""
        return self.db.query_fetch(select_query, (test_type,))
    
    def get_all_tests(self, test_type):
        select_query = "SELECT * FROM vocab_testset where testtype = ?;"
        return self.db.query_fetch_all(select_query, (test_type,))
    
    def reset_test(self):
        clear_query = "DELETE FROM vocab_testset WHERE TRUE;"
        self.db.query_execute(clear_query)
        return True


    def close(self):
        self.db.close()

if __name__ == "__main__":
    test_db_mgr = TestDBManager(db_path=os.path.join("data","vocab_testset.db"))

    # Insert sample tests
    test_data = [{'testtype': 1, 'testno': 1, 'words': 'rip1 sadder forgery clutch', 'location': 'test1.txt'},
                 {'testtype': 1, 'testno': 2, 'words': 'rip2 sadder forgery clutch', 'location': 'test2.txt'},
                 {'testtype': 2, 'testno': 1, 'words': 'rip3 sadder forgery clutch', 'location': 'test3.txt'}]
    for test_dict in test_data:
        test_db_mgr.insert_test(test_dict)

    # Retrieve and print the word details
    test_summary = test_db_mgr.get_test_summary(1)
    print(test_summary)

    # fetch all words
    all_tests = test_db_mgr.get_all_tests(1)
    print(all_tests)

    # reset words points for test
    reset_test = test_db_mgr.reset_test()
    print("reset_test : {}".format(reset_test))

    # Close the database connection
    test_db_mgr.close()