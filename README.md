
# Restaurant Reservation System

This is a simple restaurant reservation system built using Python, MySQL, and FastAPI.

## Features

- **Database Management**: Implemented through `database_management.py`, this file manages connections, and operations on a MySQL database.
- **FastAPI Interface**: The `FastApi_BluePrint.py` file provides API endpoints for creating reservations, canceling reservations, and checking available tables.

## Installation

1. Ensure Python and MySQL are installed on your system.
2. Clone or download this project to your local machine.
3. Install the required dependencies:
   ```bash
   pip install mysql-connector-python fastapi uvicorn python-dotenv
   ```

## Setting Up Environment Variables

Create a `.env` file and set the following environment variables:

```
DB_HOST=your_database_host
DB_USER=your_database_username
DB_PASSWORD=your_database_password
```

## Running the Project

1. Start the FastAPI server:
   ```bash
   uvicorn FastApi_BluePrint:app --reload
   ```
2. Visit `http://127.0.0.1:8000/docs` to view and test the API endpoints.

## Usage Guide

- **Create Reservation**: Use the `/make_reservation/` endpoint to create a reservation.
- **Cancel Reservation**: Use the `/cancel_reservation/` endpoint to cancel a reservation.
- **Check Available Tables**: Use the `/check_available_tables/` endpoint to see currently available tables.

## Contributing
