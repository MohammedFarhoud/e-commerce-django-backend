# e-commerce-django-backend
E-commerce project backend API using Django Rest Framework
# Django Project README
![Project Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)
## Description
This is a Django backend project for an e-commerce application. It provides the API endpoints required for managing products, categories, user accounts, shopping carts, and orders and wishlist and paymment method stripe. The project is built using Django and Django Rest Framework.
## Development Environment Setup

To set up the development environment for this project, follow these steps:

### Prerequisites

- Python 3.9 or higher
- Django 3.2 or higher
- Virtualenv (optional but recommended)

### Installation
1. Clone the repository: `git clone git@github.com:MohammedFarhoud/e-commerce-django-backend.git'
2. Navigate to the project directory: `cd your-project`
3. Create and activate a virtual environment (optional): `virtualenv env && source env/bin/activate`
4. Install the project dependencies: `pip install -r requirements.txt`
### Configuration

1. Create a `.env` file in the project root directory.
2. Configure the necessary environment variables in the `.env` file, such as database credentials and API keys.
### Database Setup

1. Run database migrations: `python manage.py migrate`
2. (Optional) Load initial data fixtures: `python manage.py loaddata initial_data.json`


## Running the Project

To run the Django project locally, follow these steps:

1. Activate the virtual environment (if used): `source env/bin/activate`
2. Start the development server: `python manage.py runserver`
3. Open your web browser and visit: `http://localhost:8000/`


To install the Stripe CLI on Debian and Ubuntu-based distributions:

1. Add Stripe CLI’s GPG key to the apt sources keyring:
curl -s https://packages.stripe.dev/api/security/keypair/stripe-cli-gpg/public | gpg --dearmor | sudo tee /usr/share/keyrings/stripe.gpg

2. Add CLI’s apt repository to the apt sources list:
echo "deb [signed-by=/usr/share/keyrings/stripe.gpg] https://packages.stripe.dev/stripe-cli-debian-local stable main" | sudo tee -a /etc/apt/sources.list.d/stripe.list

3. Update the package list:
 sudo apt update
4. Install the CLI:
sudo apt install stripe

5. login in cli 
stripe login

6. Use the --forward-to flag to send all Stripe events in test mode to your local webhook endpoint. To disable HTTPS certificate verification, use the --skip-verify flag.

stripe listen --forward-to localhost:8000/api/webhook

## Project Structure

The project structure follows the standard Django app structure:

- `manage.py`: The Django project management script.
- `your_project/`: The project's main directory.
  - `settings.py`: Django project settings.
  - `urls.py`: URL configuration for the project.
  - `your_app/`: The main app directory.
    - `models.py`: Database models for the app.
    - `views.py`: Views and API endpoints for the app.
    - `serializers.py`: Serializers for converting models to JSON.
    - `tests.py`: Unit tests for the app.
