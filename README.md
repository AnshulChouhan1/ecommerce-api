# ElevaStore E-Commerce

A full-stack e-commerce web application built with Python, Flask, and SQLite. Features a custom API for mock order tracking, an admin dashboard, user authentication, and shopping cart functionality.

## Features

- **User Authentication:** Registration, Login, and Password Hashing using Flask-Bcrypt & Flask-Login.
- **Product & Cart System:** Dynamic browsing and real-time stock management. Add items to your cart and place robust orders.
- **Order Tracking:** A built-in mock RESTful API that the frontend actively hits using the `requests` library to fetch JSON shipment statuses.
- **Admin Dashboard:** Left-nav tabbed system for managing Users, Products, and Order tracking statuses seamlessly.
- **Premium Design:** Features a custom CSS styling layout mirroring a modern aesthetic with glassmorphism without the use of dense frontend frameworks.

## Quickstart

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository** (if applicable) and navigate to the root directory.

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database:**
   This command will build the `.db` file and automatically seed mock products, an Admin account, and a Customer account so you can dive right in:
   ```bash
   python init_db.py
   ```

5. **Run the Application:**
   ```bash
   python run.py
   ```
   Open `http://127.0.0.1:5000` in your web browser.

### Test Credentials (Created by `init_db.py`)
- **Admin User:** `admin@elevastore.com` / `password123`
- **Customer User:** `user@test.com` / `password123`

## Project Structure
- `app/` - The core application package containing Flask Blueprints (`auth`, `main`, `admin`, `api`, `mock_api`).
- `config.py` - Sets configuration variables.
- `run.py` - Standard point of execution for the app.
- `init_db.py` - Script to generate the SQLite schemas and upload pre-filled dummy data.
