import mysql.connector
from mysql.connector import Error

class MySQL_API:
    def __int__(self, host, user, password, db):
        """initial database connection para"""
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def creat_connection(self):
        """creat connection to db"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db
            )
            return True
        except Error as e:
            print(f"database connected error...")
            return False

    def close_connection(self):
        """close connection"""
        if self.connection.is_connected():
            self.connection.close()

    def excute_query(self, query, params=None):
        """apply sql search"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"query error...")
            return False


    def fetch_data(self, query, params=None):
        """getting data from query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query,params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"error obtain data")
            return False


    def create_database(self, db_name):
        """create database if not exists"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"database {db_name} has created or already exist")
        except Error as e:
            print(f"error while creating database: {e}")

    def create_tables(self,db_name):
        """create table in db"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"USE {db_name}")

            #create reservation table
            create_reservations_table = """
            CREATE TABLE IF NOT EXISTS Reservations (
                ReservationID INT AUTO_INCREMENT PRIMARY KEY,
                CustomerName VARCHAR(100),
                ReservationDate DATE,
                ReservationTime TIME,
                NumberOfGuests INT
            )
            """
            cursor.execute(create_reservations_table)
        except Error as e:
            print(f"error while creating table: {e}")

