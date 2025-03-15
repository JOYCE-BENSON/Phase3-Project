# views/cli.py
import os
import time
from controllers.donor_controller import DonorController
from controllers.campaign_controller import CampaignController
from controllers.donation_controller import DonationController

class CLI:
    """Command Line Interface for the GiveConnect application"""
    
    def __init__(self):
        self.current_donor = None
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a formatted header"""
        self.clear_screen()
        print("=" * 60)
        print(f"  {title}")
        print("=" * 60)
        print()
    
    def pause(self):
        """Pause for user input"""
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the main application loop"""
        while True:
            choice = self.show_main_menu()
            
            if choice == '1':
                self.login()
            elif choice == '2':
                self.register()
            elif choice == '3':
                print("\nThank you for using GiveConnect! Goodbye.")
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause()
    
    def show_main_menu(self):
        """Display the main menu"""
        self.print_header("GiveConnect - Connect with Causes That Matter")
        
        print("Main Menu")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        return input("\nEnter your choice (1-3): ")
    
    def register(self):
        """Register a new donor"""
        self.print_header("Register as a Donor")
        
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        confirm_password = input("Confirm your password: ")
        
        success, message = DonorController.register_donor(name, email, password, confirm_password)
        
        if success:
            print(f"\nSuccess! {message}")
            print("You can now login with your credentials.")
        else:
            print(f"\nRegistration failed: {message}")
        
        self.pause()
    
    def login(self):
        """Login a donor"""
        self.print_header("Donor Login")
        
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        
        success, result = DonorController.login(email, password)
        
        if success:
            self.current_donor = result
            print(f"\nWelcome back, {self.current_donor['name']}!")
            self.donor_menu()
        else:
            print(f"\nLogin failed: {result}")
            self.pause()
    
    def donor_menu(self):
        """Display the donor menu"""
        while True:
            self.print_header(f"Welcome, {self.current_donor['name']}")
            
            print("Donor Menu")
            print("1. Browse Campaigns")
            print("2. View My Donation History")
            print("3. View My Profile")
            print("4. Logout")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.browse_campaigns()
            elif choice == '2':
                self.view_donation_history()
            elif choice == '3':
                self.view_profile()
            elif choice == '4':
                self.current_donor = None
                print("\nYou have been logged out.")
                self.pause()
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause()
    
    def browse_campaigns(self):
        """Browse available campaigns"""
        while True:
            self.print_header("Browse Campaigns")
            
            success, campaigns = CampaignController.get_active_campaigns()
            
            if not success:
                print(f"Error: {campaigns}")
                self.pause()
                return
            
            if len(campaigns) == 0:
                print("No active campaigns available.")
                self.pause()
                return
            
            print("ID | Name | Organization | Progress | Goal")
            print("-" * 60)
            
            for campaign in campaigns:
                progress = (campaign['current_amount'] / campaign['goal_amount']) * 100 if campaign['goal_amount'] > 0 else 0
                print(f"{campaign['id']} | {campaign['name']} | {campaign['organization']} | ${campaign['current_amount']:.2f} ({progress:.1f}%) | ${campaign['goal_amount']:.2f}")
            
            print("\nOptions:")
            print("1. View Campaign Details")
            print("2. Make a Donation")
            print("3. Return to Donor Menu")
            
            choice = input("\nEnter your choice (1-3): ")
            
            if choice == '1':
                campaign_id = input("Enter campaign ID to view details: ")
                self.view_campaign_details(campaign_id)
            elif choice == '2':
                campaign_id = input("Enter campaign ID to donate to: ")
                self.make_donation(campaign_id)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
                self.pause()
    
    def view_campaign_details(self, campaign_id):
        """View details of a specific campaign"""
        self.print_header("Campaign Details")
        
        try:
            campaign_id = int(campaign_id)
        except ValueError:
            print("Invalid campaign ID.")
            self.pause()
            return
        
        success, campaign = CampaignController.get_campaign_details(campaign_id)
        
        if not success:
            print(f"Error: {campaign}")
            self.pause()
            return
        
        progress = (campaign['current_amount'] / campaign['goal_amount']) * 100 if campaign['goal_amount'] > 0 else 0
        
        print(f"Name: {campaign['name']}")
        print(f"Organization: {campaign['organization']}")
        print(f"Description: {campaign['description']}")
        print(f"Goal: ${campaign['goal_amount']:.2f}")
        print(f"Current Amount: ${campaign['current_amount']:.2f} ({progress:.1f}%)")
        print(f"Created: {campaign['created_at']}")
        
        print("\nOptions:")
        print("1. Make a Donation")
        print("2. Return to Campaign List")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == '1':
            self.make_donation(campaign_id)
        elif choice != '2':
            print("Invalid choice.")
            self.pause()
    
    def make_donation(self, campaign_id):
        """Make a donation to a campaign"""
        self.print_header("Make a Donation")
        
        try:
            campaign_id = int(campaign_id)
        except ValueError:
            print("Invalid campaign ID.")
            self.pause()
            return
        
        success, campaign = CampaignController.get_campaign_details(campaign_id)
        
        if not success:
            print(f"Error: {campaign}")
            self.pause()
            return
        
        print(f"You are donating to: {campaign['name']}")
        
        amount_str = input("Enter donation amount: $")
        
        try:
            amount = float(amount_str)
        except ValueError:
            print("Invalid amount. Please enter a number.")
            self.pause()
            return
        
        success, message = DonationController.make_donation(
            self.current_donor['id'],
            campaign_id,
            amount
        )
        
        if success:
            print(f"\n{message}")
        else:
            print(f"\nError: {message}")
        
        self.pause()
    
    def view_donation_history(self):
        """View donor's donation history"""
        self.print_header("My Donation History")
        
        success, donations = DonorController.get_donation_history(self.current_donor['id'])
        
        if not success:
            print(f"Error: {donations}")
            self.pause()
            return
        
        if len(donations) == 0:
            print("You have not made any donations yet.")
            self.pause()
            return
        
        print("ID | Date | Campaign | Amount")
        print("-" * 60)
        
        for donation in donations:
            print(f"{donation['id']} | {donation['date']} | {donation['campaign_name']} | ${donation['amount']:.2f}")
        
        self.pause()
    
    def view_profile(self):
        """View donor's profile"""
        self.print_header("My Profile")
        
        success, profile = DonorController.get_donor_profile(self.current_donor['id'])
        
        if not success:
            print(f"Error: {profile}")
            self.pause()
            return
        
        print(f"Name: {profile['name']}")
        print(f"Email: {profile['email']}")
        print(f"Total Donations: ${profile['total_donated']:.2f}")
        print(f"Member Since: {profile['created_at']}")
        
        self.pause()