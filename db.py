import mysql.connector

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",# connecting to local mysql server
        user="root",
        password="Anushroot",  # Change if needed
        database="SecureHer"
    )
