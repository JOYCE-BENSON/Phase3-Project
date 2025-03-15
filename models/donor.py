# models/donor.py
import re
import sqlite3
from models.base import Base

class Donor(Base):
    """Model representing a donor in the system"""
    
    TABLE_NAME = "donors"
    COLUMNS = [
        "name TEXT NOT NULL",
        "email TEXT NOT NULL UNIQUE",
        "password TEXT NOT NULL",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ]
    
    @classmethod
    def initialize(cls):
        """Initialize the donor table"""
        cls.create_table()
    
    @classmethod
    def create(cls, name, email, password):
        """Create a new donor with validation"""
        # Validate the format of the email
        if not cls.validate_email(email):
            raise ValueError("Invalid email format")
            
        # Check if that email I put above already exists
        if cls.find_by_email(email):
            raise ValueError("Email already registered")
            
        # Create the donor
        return super().create(name=name, email=email, password=password)
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @classmethod
    def find_by_email(cls, email):
        """Find a donor by email"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE email = ?"
        
        cursor.execute(sql, (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Convert row to dictionary
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        else:
            return None
    
    @classmethod
    def authenticate(cls, email, password):
        """Authenticate a donor by email and password"""
        donor = cls.find_by_email(email)
        
        if donor and donor['password'] == password:
            return donor
        return None
        
    @classmethod
    def get_donation_history(cls, donor_id):
        """Get donation history for a donor"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = """
        SELECT d.id, d.amount, d.date, c.name as campaign_name
        FROM donations d
        JOIN campaigns c ON d.campaign_id = c.id
        WHERE d.donor_id = ?
        ORDER BY d.date DESC
        """
        
        cursor.execute(sql, (donor_id,))
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows to dictionaries
        columns = [column[0] for column in cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
            
        return results
        
    @classmethod
    def get_total_donated(cls, donor_id):
        """Get total amount donated by a donor"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = "SELECT SUM(amount) FROM donations WHERE donor_id = ?"
        
        cursor.execute(sql, (donor_id,))
        total = cursor.fetchone()[0] or 0
        conn.close()
        
        return total