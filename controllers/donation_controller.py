# controllers/donation_controller.py
from models.donation import Donation

class DonationController:
    """Controller for donation-related operations"""
    
    @staticmethod
    def make_donation(donor_id, campaign_id, amount):
        """Make a donation to a campaign"""
        try:
            # To Convert amount to float
            amount = float(amount)
            if amount <= 0:
                return False, "Donation amount must be greater than zero"
                
            # Create donation
            donation_id = Donation.create(
                donor_id=donor_id,
                campaign_id=campaign_id,
                amount=amount
            )
            
            return True, f"Thank you for your donation of ${amount:.2f}! Donation ID: {donation_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Donation failed: {str(e)}"
    
    @staticmethod
    def get_donation_details(donation_id):
        """Get details of a specific donation"""
        try:
            donation = Donation.find_by_id(donation_id)
            if donation:
                return True, donation
            else:
                return False, "Donation not found"
        except Exception as e:
            return False, f"Could not retrieve donation details: {str(e)}"
    
    @staticmethod
    def get_donations_by_donor(donor_id):
        """Get all donations made by a donor"""
        try:
            donations = Donation.get_donations_by_donor(donor_id)
            return True, donations
        except Exception as e:
            return False, f"Could not retrieve donor donations: {str(e)}"
    
    @staticmethod
    def get_donations_by_campaign(campaign_id):
        """Get all donations made to a campaign"""
        try:
            donations = Donation.get_donations_by_campaign(campaign_id)
            return True, donations
        except Exception as e:
            return False, f"Could not retrieve campaign donations: {str(e)}"