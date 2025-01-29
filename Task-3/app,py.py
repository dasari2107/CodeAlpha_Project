from flask import Flask, request, render_template_string, redirect, url_for, flash
import sqlite3
from markupsafe import escape

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key


# Database initialization
def init_db():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()


# Home Route
@app.route('/')
def home():
    return '''
        <h1>Welcome to the App!</h1>
        <a href="/login">Login</a>
        <a href="/hello">Say Hello</a>
    '''


# Secure Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Use parameterized queries to prevent SQL injection
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return "Logged in successfully!"
        else:
            flash("Invalid credentials!")  # Flashing error message
            return redirect(url_for('login'))  # Redirect to login page on failure

    return 
# Secure Route to prevent XSS
@app.route('/hello')
def hello():
    name = request.args.get('name', 'World')
    safe_name = escape(name)  # Use escape to prevent XSS
    return render_template_string('<h1>Hello, {{ name }}</h1>', name=safe_name)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
