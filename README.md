# Phase3-Project
# GiveConnect

GiveConnect is a command-line interface (CLI) application that connects donors with charitable causes. It allows donors to browse campaigns, make donations, and track their giving history.

## Features

- **Donor Management**
  - Register new donor accounts
  - Login with email and password
  - View donation history
  - View donor profile

- **Campaign Management**
  - Browse active campaigns
  - View campaign details
  - Track campaign progress

- **Donation Management**
  - Make donations to campaigns
  - Track donation history

## Installation


2. Install dependencies using Pipenv:
   ```
   pipenv install
   ```

3. Activate the virtual environment:
   ```
   pipenv shell
   ```

4. Run the application:
   ```
   python main.py
   ```

## Usage

### Main Menu

When you start the application, you'll see the main menu with the following options:
1. Login
2. Register
3. Exit

### Registration

To register as a new donor:
1. Select "Register" from the main menu
2. Enter your name, email, and password
3. Confirm your password

### Login

To login as an existing donor:
1. Select "Login" from the main menu
2. Enter your email and password

### Donor Menu

After logging in, you'll have access to the donor menu with the following options:
1. Browse Campaigns
2. View My Donation History
3. View My Profile
4. Logout

### Making a Donation

To make a donation:
1. Select "Browse Campaigns" from the donor menu
2. Choose a campaign to donate to
3. Enter the donation amount

## Project Structure

```
giveconnect/
├── README.md
├── Pipfile
├── main.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── donor.py
│   ├── campaign.py
│   └── donation.py
├── controllers/
│   ├── __init__.py
│   ├── donor_controller.py
│   ├── campaign_controller.py
│   └── donation_controller.py
└── views/
    ├── __init__.py
    └── cli.py
```

## Database Schema

The application uses SQLite with the following tables:

### Donors
- id (primary key)
- name
- email (unique)
- password
- created_at

### Campaigns
- id (primary key)
- name (unique)
- description
- goal_amount
- current_amount
- organization
- created_at
- active

### Donations
- id (primary key)
- donor_id (foreign key)
- campaign_id (foreign key)
- amount
- date

## Contributing

Contributions are welcome! Please feel free to submit a Pull ReqUEST