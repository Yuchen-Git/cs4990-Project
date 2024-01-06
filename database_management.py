import mysql.connector
from mysql.connector import Error

class Mysql_Method_Api:
    #initialize the object
    def __init__(self, host, user, password, database_name, db=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        #create connection to the database
        if self.create_connection():
            self.create_database(database_name)
    def create_connection(self,db_name=None):
        try:
            if db_name:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=db_name
                )
            else:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
            return True
        except Error as e:
            print(f"database connected error...")
            return False
    #close connection
    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
    #create database if not exist
    def create_database(self, database_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"database {database_name} has created or already exist")
        except Error as e:
            print(f"Error creating database: {e}")

    def create_Reservation_tables(self, db_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"USE {db_name}")
            # Create reservations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    phone_number VARCHAR(255),
                    guest_name VARCHAR(255),
                    num_of_guest INT,
                    reservation_date DATE,
                    reservation_time TIME,
                    table_id INT,
                    PRIMARY KEY(phone_number),
                    FOREIGN KEY(table_id) REFERENCES tables(table_unique_ID)
                )
            """)

            print("Tables have been created or already exist")
        except Error as e:
            print(f"Error creating tables: {e}")
    #initialize tables then insert default value, and commit changes then close the cursor
    def initialize_tables(self, db_name,size_of_each_table,num_of_tables):
        cursor = self.connection.cursor()
        cursor.execute(f"USE {db_name}")
        #create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tables (
            table_unique_ID INT AUTO_INCREMENT PRIMARY KEY,
            table_size VARCHAR(255),
            num_of_guest INT,
            is_Available BOOLEAN
            );
       """)
        self.insert_table(size_of_each_table,num_of_tables)
        #commit changes after insertion
        self.connection.commit()

    #internal called def that insert default value to the table
    def insert_table(self, size_of_each_table,num_of_tables):
        cursor = self.connection.cursor()
        for i in range(num_of_tables):
            cursor.execute("""
            INSERT INTO tables (table_size, is_Available)
            VALUES (%s, %s)
            """,(size_of_each_table, True))

