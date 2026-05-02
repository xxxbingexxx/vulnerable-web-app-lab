from flask import Flask, request, redirect, url_for, session, render_template
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('comments'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        # SECURE: parameterized query
        query = "SELECT * FROM users WHERE username = ?"
        print(f"[DEBUG] Executing query: {query} | Params: ({username},)")
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = user['username']
            return redirect(url_for('comments'))
        else:
            error = "Invalid credentials"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        comment = request.form['comment']
        # VULNERABLE: directly inserting user input
        cursor.execute("INSERT INTO comments (username, comment) VALUES (?, ?)", 
                      (session['username'], comment))
        conn.commit()

    cursor.execute("SELECT * FROM comments")
    comments = cursor.fetchall()
    conn.close()

    return render_template('comments.html', 
                         username=session['username'], 
                         comments=comments)

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(debug=True)