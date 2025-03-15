# main.py
import os
import sys
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent.absolute()

# Add current directory to the path
sys.path.insert(0, str(current_dir))

# here I'm trying to import the modules directly from the root directory- they're in the root directory
from models.donor import Donor
from models.campaign import Campaign
from models.donation import Donation
from views.cli import CLI  

def initialize_database():
    """Initialize the database and create sample data if needed"""
    # Create tables
    Donor.initialize()
    Campaign.initialize()
    Donation.initialize()
    
    # Checkingto see if I need to create sample data
    if len(Donor.get_all()) == 0:
        create_sample_data()



def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    
    # Create donors
    donor1_id = Donor.create(name="John Doe", email="john@example.com", password="password123")
    donor2_id = Donor.create(name="Jane Smith", email="jane@example.com", password="password123")
    
    # Create campaigns
    campaign1_id = Campaign.create(
        name="Clean Water Initiative",
        description="Providing clean water to communities in need",
        goal_amount=10000.00,
        organization="Water for All"
    )
    
    campaign2_id = Campaign.create(
        name="Education for Children",
        description="Supporting education for underprivileged children",
        goal_amount=5000.00,
        organization="Children's Education Fund"
    )
    
    # Create donations
    Donation.create(donor_id=donor1_id, campaign_id=campaign1_id, amount=100.00)
    Donation.create(donor_id=donor2_id, campaign_id=campaign1_id, amount=150.00)
    Donation.create(donor_id=donor1_id, campaign_id=campaign2_id, amount=75.00)
    
    print("Sample data created successfully!")

def main():
    """Main application entry point"""
    
    initialize_database()
    
    # StartING THE CLI
    cli = CLI()
    cli.run()

if __name__ == "__main__":
    main()