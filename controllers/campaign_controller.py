# controllers/campaign_controller.py
from models.campaign import Campaign

class CampaignController:
    """Controller for campaign-related operations"""
    
    @staticmethod
    def create_campaign(name, description, goal_amount, organization):
        """Create a new campaign"""
        
        if not name or not description or not organization:
            return False, "Name, description, and organization are required"
            
        try:
            
            goal_amount = float(goal_amount)
            if goal_amount <= 0:
                return False, "Goal amount must be greater than zero"
                
            # Now I want to Create  a new campaign
            campaign_id = Campaign.create(
                name=name,
                description=description,
                goal_amount=goal_amount,
                organization=organization
            )
            return True, f"Campaign created successfully with ID: {campaign_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Campaign creation failed: {str(e)}"
    
    @staticmethod
    def get_all_campaigns():
        """Get all campaigns"""
        try:
            campaigns = Campaign.get_all()
            return True, campaigns
        except Exception as e:
            return False, f"Could not retrieve campaigns: {str(e)}"
    
    @staticmethod
    def get_active_campaigns():
        """Get all active campaigns"""
        try:
            campaigns = Campaign.get_active_campaigns()
            return True, campaigns
        except Exception as e:
            return False, f"Could not retrieve active campaigns: {str(e)}"
    
    @staticmethod
    def get_campaign_details(campaign_id):
        """Get details of a specific campaign"""
        try:
            campaign = Campaign.find_by_id(campaign_id)
            if campaign:
                # Here I'm Calculating progress percentage
                if campaign['goal_amount'] > 0:
                    campaign['progress'] = (campaign['current_amount'] / campaign['goal_amount']) * 100
                else:
                    campaign['progress'] = 0
                    
                return True, campaign
            else:
                return False, "Campaign not found"
        except Exception as e:
            return False, f"Could not retrieve campaign details: {str(e)}"
    
    @staticmethod
    def get_campaign_donors(campaign_id):
        """Get donors who have contributed to a campaign"""
        try:
            donors = Campaign.get_campaign_donors(campaign_id)
            return True, donors
        except Exception as e:
            return False, f"Could not retrieve campaign donors: {str(e)}"