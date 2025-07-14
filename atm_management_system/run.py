import subprocess
import sys
import os
from threading import Thread
import time

def run_server():
    """Runs the server in a subprocess."""
    server_path = os.path.join("server", "main.py")
    subprocess.run([sys.executable, server_path])

def run_client():
    """Runs the client in a subprocess."""
    client_path = os.path.join("client", "main.py")
    subprocess.run([sys.executable, client_path])

if __name__ == "__main__":
    # Change the working directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Initialize the database
    database_path = os.path.join("database", "database.py")
    subprocess.run([sys.executable, database_path])

    # Run the server in a separate thread
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Give the server a moment to start
    time.sleep(2)

    # Run the client
    run_client()
