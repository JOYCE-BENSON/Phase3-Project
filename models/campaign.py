# models/campaign.py
import sqlite3
from models.base import Base

class Campaign(Base):
    """Model representing a charitable campaign"""
    
    TABLE_NAME = "campaigns"
    COLUMNS = [
        "name TEXT NOT NULL UNIQUE",
        "description TEXT NOT NULL",
        "goal_amount REAL NOT NULL",
        "current_amount REAL DEFAULT 0.0",
        "organization TEXT NOT NULL",
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "active INTEGER DEFAULT 1"
    ]
    
    @classmethod
    def initialize(cls):
        """Initialize the campaign table"""
        cls.create_table()
    
    @classmethod
    def create(cls, name, description, goal_amount, organization):
        """Create a new campaign with validation"""
        # Validate goal amount
        if goal_amount <= 0:
            raise ValueError("Goal amount must be greater than zero")
            
        # Check if the campaign name already exists before 
        if cls.find_by_name(name):
            raise ValueError("Campaign name already exists")
            
        # Create the campaign
        return super().create(
            name=name, 
            description=description, 
            goal_amount=goal_amount,
            current_amount=0.0,
            organization=organization
        )
    
    @classmethod
    def find_by_name(cls, name):
        """Find a campaign by name"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE name = ?"
        
        cursor.execute(sql, (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Convert row to dictionary
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        else:
            return None
    
    @classmethod
    def get_active_campaigns(cls):
        """Get all active campaigns"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE active = 1"
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
            
        return results
    
    @classmethod
    def update_current_amount(cls, campaign_id, amount):
        """Update the current amount of a campaign"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"UPDATE {cls.TABLE_NAME} SET current_amount = current_amount + ? WHERE id = ?"
        
        cursor.execute(sql, (amount, campaign_id))
        conn.commit()
        conn.close()
        
    @classmethod
    def get_campaign_donors(cls, campaign_id):
        """Get all donors for a campaign"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = """
        SELECT d.id, d.donor_id, donors.name as donor_name, d.amount, d.date
        FROM donations d
        JOIN donors ON d.donor_id = donors.id
        WHERE d.campaign_id = ?
        ORDER BY d.date DESC
        """
        
        cursor.execute(sql, (campaign_id,))
        rows = cursor.fetchall()
        conn.close()
        
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
            
        return results