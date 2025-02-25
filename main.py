import requests
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


def init_db():
    """Initialize the database."""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')
    conn.commit()
    conn.close()


@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return jsonify({"message": "User registered successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists!"})
    finally:
        conn.close()


@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    """Fetch data from an external API."""
    response = requests.get('https://jsonplaceholder.typicode.com/posts')
    if response.status_code == 200:
        return jsonify(response.json())
    return jsonify({"error": "Failed to fetch data"})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
