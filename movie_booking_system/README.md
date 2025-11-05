# Online Movie Booking System

This project is a Python-based online movie booking system, similar to BookMyShow. It uses Flask for the backend API and MySQL for the database.

## Setup Instructions

### 1. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 2. Set Up the Database

1.  **Install MySQL:** If you don't have MySQL installed, download and install it from the official website.
2.  **Update Credentials:** Open `database.py` and `app.py` and replace the placeholder credentials (`your_username` and `your_password`) with your MySQL username and password.
3.  **Create the Database:** Run the `database.py` script to create the `movie_booking` database and the required tables:

    ```bash
    python database.py
    ```

### 3. Run the Application

1.  **Start the Flask Server:**

    ```bash
    python app.py
    ```

    The server will start on `http://127.0.0.1:5000`.

2.  **Use the Command-Line Interface (CLI):**

    Open a new terminal and run the `cli.py` script to interact with the application:

    ```bash
    python cli.py
    ```

## API Endpoints

*   `POST /register`: Register a new user.
*   `POST /login`: Log in an existing user.
*   `GET /movies`: Get a list of all movies.
*   `GET /shows`: Get a list of shows (can be filtered by `movie_id` and `theater_id`).
*   `POST /book`: Book a ticket for a show.
