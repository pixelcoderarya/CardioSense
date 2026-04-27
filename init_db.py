import mysql.connector
from mysql.connector import Error
import os

# Use the same config as database.py
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "masteradmin")

def run_sql_file(filename, connection):
    cursor = connection.cursor()
    with open(filename, 'r') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                try:
                    cursor.execute(command)
                except Error as e:
                    print(f"Error executing command: {e}")
    connection.commit()
    cursor.close()

def init_db():
    try:
        # Connect without database first to create it
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            print("Connected to MySQL server.")
            run_sql_file('backend/schema.sql', connection)
            print("Database initialized successfully!")
            
    except Error as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    init_db()
