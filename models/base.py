# models/base.py
import sqlite3
import os

class Base:
    """Base model class that provides common ORM functionality"""
    
    DB_PATH = "giveconnect.db"
    TABLE_NAME = None
    COLUMNS = []
    
    @classmethod
    def create_table(cls):
        """Create the table if it doesn't exist"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        # Build the table scheme using columns columns
        columns_def = ", ".join(cls.COLUMNS)
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {cls.TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columns_def}
        )
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        conn.close()
    
    @classmethod
    def create(cls, **kwargs):
        """Create a new record in the database"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        # Extract column names and values
        columns = list(kwargs.keys())
        values = list(kwargs.values())
        
        # Build the SQL query
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?"] * len(columns))
        
        sql = f"INSERT INTO {cls.TABLE_NAME} ({columns_str}) VALUES ({placeholders})"
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        
        return last_id
    
    @classmethod
    def delete(cls, record_id):
        """Delete a record by ID"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"DELETE FROM {cls.TABLE_NAME} WHERE id = ?"
        
        cursor.execute(sql, (record_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return rows_affected > 0
    
    @classmethod
    def get_all(cls):
        """Get all records"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {cls.TABLE_NAME}"
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows to dictionaries
        columns = [column[0] for column in cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
        
        return results
    
    @classmethod
    def find_by_id(cls, record_id):
        """Find a record by its ID"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?"
        
        cursor.execute(sql, (record_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Convert row to dictionary
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        else:
            return None
            
    @classmethod
    def execute_custom_query(cls, sql, params=()):
        """Execute a custom SQL query"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        # Again Convert rows to dictionaries
        columns = [column[0] for column in cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
            
        conn.close()
        return results