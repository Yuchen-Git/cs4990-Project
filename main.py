from database_api import MysqlApi

from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Now you can use os.getenv to read the environment variables
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


database_name = "reservation_sys_db"

def main():
    # Create a MySQL_API object
    db = MysqlApi(db_host, db_user, db_password)
    
    #try to create a connection to the database
    if db.create_connection():
        db.create_database(database_name)
    else:
        print("Error! cannot create the database connection.")
    db.create_tables(database_name)
    db.close_connection()

if __name__ == "__main__":
    main()
