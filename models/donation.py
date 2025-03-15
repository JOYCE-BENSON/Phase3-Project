# models/donation.py
import sqlite3
from datetime import datetime
from models.base import Base
from models.campaign import Campaign

class Donation(Base):
    """Model representing a donation from a donor to a campaign"""
    
    TABLE_NAME = "donations"
    COLUMNS = [
        "donor_id INTEGER NOT NULL",
        "campaign_id INTEGER NOT NULL",
        "amount REAL NOT NULL",
        "date TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "FOREIGN KEY (donor_id) REFERENCES donors (id)",
        "FOREIGN KEY (campaign_id) REFERENCES campaigns (id)"
    ]
    
    @classmethod
    def initialize(cls):
        """Initialize the donation table"""
        cls.create_table()
    
    @classmethod
    def create(cls, donor_id, campaign_id, amount):
        """Create a new donation with validation"""
        # Validating the amount
        if amount <= 0:
            raise ValueError("Donation amount must be greater than zero")
            
        # Check if donor and campaign exist
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        # Check for donor
        cursor.execute("SELECT id FROM donors WHERE id = ?", (donor_id,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError("Donor does not exist")
            
        # Check for the campaign
        cursor.execute("SELECT id FROM campaigns WHERE id = ?", (campaign_id,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError("Campaign does not exist")
            
        conn.close()
        
        # Create the donation
        donation_id = super().create(
            donor_id=donor_id, 
            campaign_id=campaign_id, 
            amount=amount,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Then now Update campaign current amount
        Campaign.update_current_amount(campaign_id, amount)
        
        return donation_id
    
    @classmethod
    def get_donations_by_donor(cls, donor_id):
        """Get all donations made by a donor"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE donor_id = ? ORDER BY date DESC"
        
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
    def get_donations_by_campaign(cls, campaign_id):
        """Get all donations made to a campaign"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        
        sql = f"SELECT * FROM {cls.TABLE_NAME} WHERE campaign_id = ? ORDER BY date DESC"
        
        cursor.execute(sql, (campaign_id,))
        rows = cursor.fetchall()
        conn.close()
        
        
        columns = [column[0] for column in cursor.description]
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
            
        return results