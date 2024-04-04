# Clothing & Accessories E-Commerce Backend

# Introduction
This project is a Flask-based API for a retail website, providing backend functionality for user authentication, product management, transactions, and more.

# Contributers
Amrita Kondeti, Gabrielle Glasgow, Jason Fearnall, Max Ross

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Project Structure](#getting-started)
- [Functionality](#functionalilty)

## Getting Started

To set up the project locally, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/product-retail-api.git

2. Install the required dependencies using pipq
   pip install -r requirements.txt

3. Initialize the SQLite Database

    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade

4. Run the flask development server: 
    python app.py


## Project Structure
- app.py: Main Flask application file containing routes and application setup.
- models.py: SQLAlchemy models for database tables.
- data_import.py: Module for importing data into the database.
- tests/: Directory containing unit tests for the application.
- static/ and templates/: Directories for static files and HTML templates (if applicable).

## Functionality
The API provides the following functionality
- User Authentication and management 
- Product management : CRUD operations, sorting, querying
- Transaction management
- Review management: Add, view, and manage product reviews

