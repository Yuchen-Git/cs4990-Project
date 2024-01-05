import mysql.connector
from mysql.connector import Error

class Mysql_Method_Api:
    #initialize the object
    def __init__(self, host, user, password, db=None):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
    #create connection to the database
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
            
    #create tables if not exist
    # def create_tables(self, db_name):
    #     try:
    #         cursor = self.connection.cursor()
    #         cursor.execute(f"USE {db_name}")
    #         cursor.execute("CREATE TABLE IF NOT EXISTS guest (guest_id INT AUTO_INCREMENT PRIMARY KEY, guestname VARCHAR(255), number_of_guest INT, email VARCHAR(255), Reservation_date DATE, Reservation_time TIME, phone VARCHAR(255)))")
    #         cursor.execute("CREATE TABLE IF NOT EXISTS table (table_id INT AUTO_INCREMENT PRIMARY KEY, guest_id INT, number_of_guest INT(255), Reservation_date DATE, Reservation_time TIME, guestname VARCHAR(255), FOREIGN KEY (user_id) REFERENCES guest(user_id), FOREIGN KEY (guestname) REFERENCES guest(guestname), FOREIGN KEY (Reservation_time) REFERENCES guest(Reservation_time) FOREIGN KEY (Reservation_date) REFERENCES guest(Reservation_date), FOREIGN KEY (number_of_guest) REFERENCES guest(number_of_guest))")
    #         cursor.execute("CREATE TABLE IF NOT EXISTS reservations (reservation_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, guestname VARCHAR(255), number_of_guest INT(255), table_id INT, email VARCHAR(255), Reservation_date DATE, FOREIGN KEY (Reservation_date) REFERENCES table(Reservation_date)FOREIGN KEY (email) REFERENCES guest(email), FOREIGN KEY (number_of_guest) REFERENCES table(number_of_guest), FOREIGN KEY (guestname) REFERENCES table(guestname), FOREIGN KEY (user_id) REFERENCES table(user_id), FOREIGN KEY (table_id) REFERENCES table(table_id))")
    #         print(f"tables has created or already exist")
    #     except Error as e:
    #         print(f"Error creating tables: {e}")
    def create_tables(self, db_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"USE {db_name}")

            # Create guest table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS guest (
                    guest_id INT AUTO_INCREMENT PRIMARY KEY,
                    guestname VARCHAR(255),
                    number_of_guests INT,
                    email VARCHAR(255),
                    reservation_date DATE,
                    reservation_time TIME,
                    phone VARCHAR(255)
                )
            """)

            # Create dining_table (formerly 'table') table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS dining_table (
                    table_id INT AUTO_INCREMENT PRIMARY KEY,
                    guest_id INT,
                    number_of_guests INT,
                    guestname VARCHAR(255)
                    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
                    FOREIGN KEY (number_of_guests) REFERENCES guest(number_of_guests),
                    FOREIGN KEY (guestname) REFERENCES guest(guestname),


                )
            """)

            # Create reservations table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reservations (
                    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
                    guest_id INT,
                    number_of_guests INT,
                    table_id INT,
                    reservation_date DATE,
                    reservation_time TIME,
                    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
                    FOREIGN KEY (table_id) REFERENCES dining_table(table_id),
                    FOREIGN KEY (reservation_time) REFERENCES guest(reservation_time),
                    FOREIGN KEY (reservation_date) REFERENCES guest(reservation_date),
                )
            """)

            print("Tables have been created or already exist")
        except Error as e:
            print(f"Error creating tables: {e}")

    #insert data into the table for guest
    def insert_guest(self, guestname, number_of_guest, password, email, Reservation_date, Reservation_time, phone):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO guest (guestname, number_of_guest, password, email, Reservation_date, Reservation_time, phone) VALUES ('{guestname}', '{number_of_guest}', '{password}', '{email}', '{Reservation_date}', '{Reservation_time}', '{phone}')")
            self.connection.commit()
            print(f"guest {guestname} has been added")
        except Error as e:
            print(f"Error inserting guest: {e}")
    # insert data into the table for table
    def insert_table(self, number_of_guest, Reservation_date, Reservation_time, guestname):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"INSERT INTO table (number_of_guest, Reservation_date, Reservation_time, guestname) VALUES ('{number_of_guest}', '{Reservation_date}', '{Reservation_time}', '{guestname}')")
            self.connection.commit()
            print(f"table has been added")
        except Error as e:
            print(f"Error inserting table: {e}")
    
    
    