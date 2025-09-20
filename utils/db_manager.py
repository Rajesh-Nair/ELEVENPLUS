import os
import sys
import sqlite3
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

class SQLiteManager:
    def __init__(self, db_path="vocab.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def query_fetch(self, query, params=None):
        try:
            cursor = self.conn.execute(query, params or ())
            return cursor.fetchone()
        except Exception as e:
            log.error(f"Database error: {e}", query=query)
            raise CustomException("Missing API keys", sys)

    def query_execute(self, query, params=None):
        try:
            self.conn.execute(query, params or ())
            self.conn.commit()
        except Exception as e:
            log.error(f"Database error: {e}", query=query)
            raise CustomException("Missing API keys", sys)

    def delete_db(self):
        """Close the connection and delete the database file from disk."""
        try:
            self.close()
            if os.path.exists(self.db_path):
                os.remove(self.db_path)
                log.info(f"Database file '{self.db_path}' deleted successfully.")
            else:
                log.warning(f"Database file '{self.db_path}' does not exist.")
        except Exception as e:
            log.error(f"Failed to delete database: {e}", db_path=self.db_path)
            raise CustomException("Failed to delete database", sys)
        
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    # Initialize and test the SQLiteManager
    db = SQLiteManager(db_path="data/test_vocab.db")

    # Create table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS vocab (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT UNIQUE NOT NULL,
                definition TEXT,
                synonyms TEXT,
                example TEXT
            );
    """
    db.query_execute(create_table_query)
    print("Table created.")

    # Insert sample data (safe, parameterized)
    insert_query = """
    INSERT INTO vocab (word, definition, synonyms, example) 
    VALUES (?, ?, ?, ?);
    """
    db.query_execute(insert_query, ("example", "A representative form or pattern", "instance, sample, case", "This is an example sentence."))
    print("Sample data inserted.")

    # Update sample data (safe, parameterized)
    update_fields = ["definition = ?"]
    update_query = f"UPDATE vocab SET {', '.join(update_fields)} WHERE word = ?;"
    db.query_execute(update_query, ("A thing characteristic of its kind or illustrating a general rule", "example"))
    print("Sample data updated.")

    # Fetch and print data (safe, parameterized)
    select_query = "SELECT * FROM vocab WHERE word = ?;"
    result = db.query_fetch(select_query, ("example",))
    print("Fetched data:", result)

    # Delete sample data (safe, parameterized)
    delete_query = "DELETE FROM vocab WHERE word = ?;"
    db.query_execute(delete_query, ("example",))
    print("Sample data deleted.")

    # Delete table
    drop_table_query = "DROP TABLE IF EXISTS vocab;"
    db.query_execute(drop_table_query)
    print("Table dropped.")

    # Delete the database file
    #db.delete_db()
    #print("Database file deleted.")

    # Close the database connection
    db.close()

    