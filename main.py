from datetime import datetime

from database_management import Mysql_Method_Api

from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# use os.getenv to read the environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
#declaration
size_of_table = 10
number_of_tables = 10
table_name = "tables"
database_name = "reservation_sys_db"

#temp value for testing make reservation def
guest_Phone_number = '8888888887'
guest_name = 'grace'
num_of_guest = '8'
reservation_date = '2024-01-01'
reservation_time = '18:30:00'
table_unique_ID = '5'

def main():
    #create a instance for establishment the connection to the database
    db = Mysql_Method_Api(db_host, db_user, db_password,database_name)
    #create table for tables in db
    db.initialize_tables(database_name, size_of_table, number_of_tables, table_name)


    #create reservation table in db
    db.create_Reservation_tables(database_name)

    #make a reservation for test
    db.make_reservations(guest_Phone_number, guest_name, num_of_guest, reservation_date, reservation_time,table_unique_ID)

    #delet a reservation for testing purposes
    db.cancel_reservation_by_phone_number(guest_Phone_number)

    #check available tables for testing purposes
    available_table_ids = db.check_available_tables()
    print(available_table_ids)

    #close connection to db
    db.close_connection()




if __name__ == "__main__":
    main()
