from fastapi import FastAPI, HTTPException
from database_management import Mysql_Method_Api
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# Initialize the database connection
db = Mysql_Method_Api(db_host, db_user, db_password, db_name)

# Define data models for FastAPI
class Reservation(BaseModel):
    guest_phone_number: str
    guest_name: str
    num_of_guest: int
    reservation_date: str
    reservation_time: str
    table_unique_ID: int

class CancelReservation(BaseModel):
    phone_number: str

# Create FastAPI app
app = FastAPI()

@app.post("/make_reservation/")
def make_reservation(reservation: Reservation):
    result = db.make_reservations(reservation.guest_phone_number, reservation.guest_name, reservation.num_of_guest, reservation.reservation_date, reservation.reservation_time, reservation.table_unique_ID)
    if result:
        return {"message": "Reservation successful"}
    else:
        raise HTTPException(status_code=400, detail="Reservation failed")

@app.delete("/cancel_reservation/")
def cancel_reservation(cancel: CancelReservation):
    result = db.cancel_reservation_by_phone_number(cancel.phone_number)
    if result:
        return {"message": "Reservation cancelled"}
    else:
        raise HTTPException(status_code=404, detail="Reservation not found")

@app.get("/check_available_tables/")
def check_available_tables():
    available_tables = db.check_available_tables()
    if available_tables:
        return {"available_tables": available_tables}
    else:
        return {"message": "No tables available"}
