# controllers/donor_controller.py
from models.donor import Donor

class DonorController:
    """Controller for donor-related operations"""
    
    @staticmethod
    def register_donor(name, email, password, confirm_password):
        """Register a new donor"""
        
        if not name or not email or not password:
            return False, "All fields are required"
            
        if password != confirm_password:
            return False, "Passwords do not match"
            
        try:
            # Create new donor
            donor_id = Donor.create(name=name, email=email, password=password)
            return True, f"Donor registered successfully with ID: {donor_id}"
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login(email, password):
        """Login a donor"""
        try:
            donor = Donor.authenticate(email, password)
            if donor:
                return True, donor
            else:
                return False, "Invalid email or password"
        except Exception as e:
            return False, f"Login failed: {str(e)}"
    
    @staticmethod
    def get_donation_history(donor_id):
        """Get a donor's donation history"""
        try:
            history = Donor.get_donation_history(donor_id)
            return True, history
        except Exception as e:
            return False, f"Could not retrieve donation history: {str(e)}"
    
    @staticmethod
    def get_donor_profile(donor_id):
        """Get a donor's profile"""
        try:
            donor = Donor.find_by_id(donor_id)
            if donor:
                # Add total donations to profile
                donor['total_donated'] = Donor.get_total_donated(donor_id)
                return True, donor
            else:
                return False, "Donor not found"
        except Exception as e:
            return False, f"Could not retrieve donor profile: {str(e)}"