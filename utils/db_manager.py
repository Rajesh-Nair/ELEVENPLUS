import os
import sys
import sqlite3
import json
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException

class SQLiteManager:
    def __init__(self, db_path="vocab.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Ensures fetch returns dict-like rows

    def get_column_names(self, table_name):
        """Return a list of column names for the given table."""
        try:
            query = f"PRAGMA table_info({table_name});"
            cursor = self.conn.execute(query)
            columns = [row[1] for row in cursor.fetchall()]  # row[1] = column name
            return columns
        except Exception as e:
            log.error(f"Error fetching column names: {e}", table_name=table_name)
            raise CustomException("Failed to fetch column names", sys)

    def query_fetch(self, query, params=None):
        try:
            cursor = self.conn.execute(query, params or ())
            row = cursor.fetchone()
            if row:
                return dict(row)  # Return as JSON-like dict
            return None
        except Exception as e:
            log.error(f"Database error: {e}", query=query)
            raise CustomException("Database fetch failed", sys)

    def query_fetch_all(self, query, params=None):
        """Fetch all rows as JSON-like list of dicts"""
        try:
            cursor = self.conn.execute(query, params or ())
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            log.error(f"Database error: {e}", query=query)
            raise CustomException("Database fetch all failed", sys)

    def query_execute(self, query, params=None):
        try:
            self.conn.execute(query, params or ())
            self.conn.commit()
        except Exception as e:
            log.error(f"Database error: {e}", query=query)
            raise CustomException("Database execute failed", sys)

    def insert_json(self, table, data: dict):
        """Insert a JSON-like dict into a table"""
        keys = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders});"
        self.query_execute(query, tuple(data.values()))

    def update_json(self, table, data: dict, where: dict):
        """Update a table using JSON-like dicts for SET and WHERE"""
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause};"
        self.query_execute(query, tuple(data.values()) + tuple(where.values()))

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
        
    def table_exists(self, table_name):
        """Check if a table exists in the database."""
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
            return self.query_fetch(query, params=(table_name,)) is not None
        except Exception as e:
            log.error(f"Error checking table existence: {e}", table_name=table_name)
            raise CustomException("Failed to check table existence", sys)
    
    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = SQLiteManager(db_path="data/test_vocab.db")

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

    if db.table_exists("vocab"):
        print("Table 'vocab' exists.")
        print("Columns:", db.get_column_names("vocab"))
    else:
        print("Table 'vocab' does not exist.")


    # Insert sample data as JSON
    sample_data = {
        "word": "example",
        "definition": "A representative form or pattern",
        "synonyms": "instance, sample, case",
        "example": "This is an example sentence."
    }
    db.insert_json("vocab", sample_data)
    print("Sample data inserted.")

    # Update sample data as JSON
    update_data = {
        "definition": "A thing characteristic of its kind or illustrating a general rule"
    }
    db.update_json("vocab", update_data, where={"word": "example"})
    print("Sample data updated.")

    # Fetch and print data as JSON
    result = db.query_fetch("SELECT * FROM vocab WHERE word = ?;", ("example",))
    print("Fetched data:", json.dumps(result, indent=2))

    # Delete sample data
    db.query_execute("DELETE FROM vocab WHERE word = ?;", ("example",))
    print("Sample data deleted.")

    db.query_execute("DROP TABLE IF EXISTS vocab;")
    print("Table dropped.")

    db.close()
