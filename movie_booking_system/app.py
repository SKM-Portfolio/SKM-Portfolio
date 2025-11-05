from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'movie_booking'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not all([username, password, email]):
        return jsonify({'error': 'Missing required fields'}), 400

    hashed_password = generate_password_hash(password)

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                       (username, hashed_password, email))
        db.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            # Don't return the password hash in the response
            user.pop('password_hash', None)
            return jsonify({'message': 'Login successful', 'user': user}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

@app.route('/movies', methods=['GET'])
def get_movies():
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
        return jsonify(movies), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

@app.route('/shows', methods=['GET'])
def get_shows():
    movie_id = request.args.get('movie_id')
    theater_id = request.args.get('theater_id')

    query = """
        SELECT s.show_id, m.title, t.name as theater_name, s.show_time, s.ticket_price
        FROM shows s
        JOIN movies m ON s.movie_id = m.movie_id
        JOIN theaters t ON s.theater_id = t.theater_id
    """
    params = []
    if movie_id:
        query += " WHERE s.movie_id = %s"
        params.append(movie_id)
    if theater_id:
        query += " AND s.theater_id = %s" if movie_id else " WHERE s.theater_id = %s"
        params.append(theater_id)

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, tuple(params))
        shows = cursor.fetchall()
        return jsonify(shows), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

@app.route('/book', methods=['POST'])
def book_ticket():
    data = request.get_json()
    user_id = data.get('user_id')
    show_id = data.get('show_id')
    num_tickets = data.get('num_tickets')

    if not all([user_id, show_id, num_tickets]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # Get ticket price
        cursor.execute("SELECT ticket_price FROM shows WHERE show_id = %s", (show_id,))
        show = cursor.fetchone()
        if not show:
            return jsonify({'error': 'Show not found'}), 404

        total_price = show['ticket_price'] * num_tickets

        # Create booking
        cursor.execute("INSERT INTO bookings (user_id, show_id, num_tickets, total_price) VALUES (%s, %s, %s, %s)",
                       (user_id, show_id, num_tickets, total_price))
        db.commit()

        return jsonify({'message': 'Booking successful'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

if __name__ == '__main__':
    app.run(debug=True)
