import mysql.connector
from mysql.connector import Error

def create_db():
    try:
        # Replace these with your actual MySQL connection details
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='C@sper123'
        )
        
        # Create cursor
        cursor = connection.cursor()
        
        # Create database if not exists
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_management")
        cursor.execute("USE inventory_management")
        
        # Create employee table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee (
                eid VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                gender VARCHAR(10),
                contact VARCHAR(20),
                dob VARCHAR(20),
                doj VARCHAR(20),
                pass VARCHAR(255),
                utype VARCHAR(50),
                address TEXT,
                salary VARCHAR(20)
            ) ENGINE=InnoDB
        """)
        
        # Create supplier table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS supplier (
                invoice INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                contact VARCHAR(20),
                `desc` TEXT
            ) ENGINE=InnoDB
        """)
        
        # Create category table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                cid INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100)
            ) ENGINE=InnoDB
        """)
        
        # Create product table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                pid INT AUTO_INCREMENT PRIMARY KEY,
                Category VARCHAR(100), 
                Supplier VARCHAR(100),
                name VARCHAR(100),
                price VARCHAR(20),
                qty VARCHAR(20),
                status VARCHAR(50)
            ) ENGINE=InnoDB
        """)
        
        print("Database and tables created successfully.")
        
        # Optional: Create a default user with limited privileges
        cursor.execute("""
            CREATE USER IF NOT EXISTS 'inventory_app'@'localhost' 
            IDENTIFIED BY 'secure_password_here'
        """)
        cursor.execute("""
            GRANT SELECT, INSERT, UPDATE, DELETE 
            ON inventory_management.* 
            TO 'inventory_app'@'localhost'
        """)
        
        connection.commit()

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

# Run the database creation
create_db()