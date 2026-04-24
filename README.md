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

## Mock API Documentation
The application features internal APIs that simulate a third-party shipping/tracking backend. 

### 1. Get Latest Order Status
`GET /latest-order/<user_id>`
Returns the real-time shipping status and product breakdown of a user's most recent order.
**Example Response:**
```json
{
  "order_id": 1,
  "product": "2x Smart Watch Series X, 1x Shoes",
  "status": "Out for delivery",
  "user_id": 12,
  "user_name": "John Doe"
}
```

### 2. Get Order Items array
`GET /order-items/<order_id>`
Returns a comprehensive line-item array of individual products within a specific order.
**Example Response:**
```json
[
  {
    "order_item_id": 1,
    "price_per_unit": 199.5,
    "product_id": 2,
    "product_name": "Smart Watch Series X",
    "quantity": 2,
    "subtotal": 399.0,
    "user_name": "John Doe"
  }
]
```

## Project Structure
- `app/` - The core application package containing Flask Blueprints (`auth`, `main`, `admin`, `api`, `mock_api`).
- `config.py` - Sets configuration variables.
- `run.py` - Standard point of execution for the app.
- `init_db.py` - Script to generate the SQLite schemas and upload pre-filled dummy data.
