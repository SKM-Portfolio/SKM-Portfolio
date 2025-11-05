import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")

    response = requests.post(f'{BASE_URL}/register', json={
        'username': username,
        'password': password,
        'email': email
    })

    print(response.json())

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    response = requests.post(f'{BASE_URL}/login', json={
        'username': username,
        'password': password
    })

    print(response.json())
    if response.status_code == 200:
        return response.json()['user']['user_id']
    return None

def get_movies():
    response = requests.get(f'{BASE_URL}/movies')
    print(json.dumps(response.json(), indent=2))

def get_shows():
    movie_id = input("Enter movie ID (optional): ")
    theater_id = input("Enter theater ID (optional): ")

    params = {}
    if movie_id:
        params['movie_id'] = movie_id
    if theater_id:
        params['theater_id'] = theater_id

    response = requests.get(f'{BASE_URL}/shows', params=params)
    print(json.dumps(response.json(), indent=2))

def book_ticket(user_id):
    if not user_id:
        print("You need to be logged in to book a ticket.")
        return

    show_id = input("Enter show ID: ")
    num_tickets = int(input("Enter number of tickets: "))

    response = requests.post(f'{BASE_URL}/book', json={
        'user_id': user_id,
        'show_id': show_id,
        'num_tickets': num_tickets
    })

    print(response.json())

def main():
    user_id = None
    while True:
        print("\n--- Movie Booking CLI ---")
        print("1. Register")
        print("2. Login")
        print("3. View Movies")
        print("4. View Shows")
        print("5. Book Ticket")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
        elif choice == '3':
            get_movies()
        elif choice == '4':
            get_shows()
        elif choice == '5':
            book_ticket(user_id)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
