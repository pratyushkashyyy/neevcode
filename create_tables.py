import sqlite3

def create_tables():
    connection = sqlite3.connect("neevcode.db")
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(80) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        phone_no VARCHAR(20) UNIQUE NOT NULL
    );
    """)

    # Create product table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name VARCHAR(100) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        image_url TEXT,
        description TEXT,
        level VARCHAR(50),
        classes TEXT,
        audience TEXT,
        rating DECIMAL(3, 2)
    );
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
