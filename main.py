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
database_name = "reservation_sys_db"

#set tables value for initialize tables
size_of_table = 10
number_of_tables = 10

def main():
    #create a instance for establishment the connection to the database
    db = Mysql_Method_Api(db_host, db_user, db_password,database_name)
    #create table for tables in db
    db.initialize_tables(database_name, size_of_table,number_of_tables)


    #create reservation table in db
    db.create_Reservation_tables(database_name)
    db.close_connection()




if __name__ == "__main__":
    main()
