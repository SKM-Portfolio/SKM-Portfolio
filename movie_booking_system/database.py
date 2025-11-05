import mysql.connector
from werkzeug.security import generate_password_hash

def create_database_and_tables():
    try:
        # Establish a connection to the MySQL server
        db = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password"
        )
        cursor = db.cursor()

        # Create the database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS movie_booking")

        # Switch to the new database
        cursor.execute("USE movie_booking")

        # Create the 'users' table with a password hash column
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        """)

        # Create the 'movies' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                genre VARCHAR(255),
                duration_minutes INT,
                release_date DATE
            )
        """)

        # Create the 'theaters' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS theaters (
                theater_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                location VARCHAR(255),
                capacity INT
            )
        """)

        # Create the 'shows' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                show_id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT,
                theater_id INT,
                show_time DATETIME,
                ticket_price DECIMAL(10, 2),
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
                FOREIGN KEY (theater_id) REFERENCES theaters(theater_id)
            )
        """)

        # Create the 'bookings' table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                show_id INT,
                num_tickets INT,
                total_price DECIMAL(10, 2),
                booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (show_id) REFERENCES shows(show_id)
            )
        """)

        print("Database and tables created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    create_database_and_tables()
