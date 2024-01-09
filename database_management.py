import mysql.connector
from mysql.connector import Error

class Mysql_Method_Api:
    #initialize the object
    def __init__(self, host, user, password, database_name, size_of_table, number_of_tables, table_name):
        self.host = host
        self.user = user
        self.password = password
        #create connection to the database
        if self.create_connection():
            self.create_database(database_name)
            self.initialize_tables(database_name, size_of_table, number_of_tables, table_name)
            self.create_Reservation_tables(database_name)
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
            #self.connection.cursor().execute(f"USE {db_name}")
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
            #return True
        except Error as e:
            print(f"Error creating database: {e}")
            #return False

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
    def check_if_table_exists(self, db_name, table_name):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT * FROM information_schema.tables
        WHERE table_schema = %s AND table_name = %s;
        """,(db_name, table_name))
        result = cursor.fetchone()

        return result is not None

    #initialize tables then insert default value, and commit changes then close the cursor
    def initialize_tables(self, db_name, size_of_each_table, num_of_tables, table_name):
        if not self.check_if_table_exists(db_name, table_name):
            cursor = self.connection.cursor()
            cursor.execute(f"USE {db_name}")

            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                table_unique_ID INT AUTO_INCREMENT PRIMARY KEY,
                table_size VARCHAR(255),
                num_of_guest INT,
                is_Available BOOLEAN
                );
            """)
        if self.is_table_empty(table_name):
            self.insert_table(size_of_each_table, num_of_tables,)
            self.connection.commit()

    def is_table_empty(self, table_name):

        cursor = self.connection.cursor()
        cursor.execute("USE reservation_sys_db")

        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.close()
        return count == 0

    #internal called def that insert default value to the table
    def insert_table(self, size_of_each_table,num_of_tables):
        cursor = self.connection.cursor()
        for i in range(num_of_tables):
            cursor.execute("""
            INSERT INTO tables (table_size, is_Available, num_of_guest )
            VALUES (%s, %s, %s)
            """,(size_of_each_table, True , 0))

    def make_reservations(self, guest_phone_number, guest_name, num_of_guest, reservation_date, reservation_time, table_unique_ID):
        """make reservation,  first check if there exist a reservation, if not, then create a new also update the table status"""
        try:
            cursor = self.connection.cursor()
            # check whether already have reservation
            cursor.execute("USE reservation_sys_db")

            cursor.execute("SELECT reservation_time, reservation_date FROM reservations WHERE phone_number = %s",
                           (guest_phone_number,))
            existing_reservation = cursor.fetchone()

            if existing_reservation:
                existing_reservation_time, existing_reservation_date = existing_reservation
                print(f"You had reservation on {existing_reservation_date} at {existing_reservation_time} .")
                return False
            else:
                # insert new reservation
                cursor.execute(
                    "INSERT INTO reservations (phone_number, guest_name, num_of_guest, reservation_date, reservation_time, table_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (guest_phone_number, guest_name, num_of_guest, reservation_date, reservation_time, table_unique_ID))

                # update tables
                cursor.execute("UPDATE tables SET is_available = %s, num_of_guest = %s WHERE table_unique_ID = %s",
                               (False, num_of_guest, table_unique_ID))

                # commit changes
                self.connection.commit()
                print(f"reservation successful：{reservation_date} {reservation_time}，reserved for：{num_of_guest}")
                return True
        except Exception as e:
            # roll back for any error
            self.connection.rollback()
            print(f"error occur when creating new reservation: {e}")
            return False

    def check_available_tables(self):
        """Checks for available tables and returns their IDs."""
        try:
            cursor = self.connection.cursor()
            # Query to find available tables
            cursor.execute("SELECT table_unique_ID FROM tables WHERE is_available = TRUE")

            available_tables = cursor.fetchall()  # Fetch all matching records

            if available_tables:
                # Extracting table IDs from the query result
                available_table_ids = [table[0] for table in available_tables]
                return available_table_ids
            else:
                # No tables available
                return False
        except Exception as e:
            print(f"Error occurred while checking for available tables: {e}")
            return False

    def cancel_reservation_by_phone_number(self, phone_number):
        """Cancels a reservation based on the phone number."""
        try:
            cursor = self.connection.cursor()
            cursor.execute("USE reservation_sys_db")
            # Check if the reservation exists
            cursor.execute("SELECT * FROM reservations WHERE phone_number = %s", (phone_number,))
            reservation = cursor.fetchone()

            if reservation:
                # Cancel the reservation
                cursor.execute("DELETE FROM reservations WHERE phone_number = %s", (phone_number,))

                # Update the table status (assuming the table ID is stored in reservation[5])
                table_unique_ID = reservation[5]
                cursor.execute("UPDATE tables SET is_available = %s, num_of_guest = 0 WHERE table_unique_ID = %s",
                               (True, table_unique_ID))

                # Commit the transaction
                self.connection.commit()
                print(f"Reservation for phone number {phone_number} has been cancelled.")
                return True
            else:
                print("No matching reservation found.")
                return False
        except Exception as e:
            # Rollback the transaction in case of any error
            self.connection.rollback()
            print(f"Error occurred during reservation cancellation: {e}")
