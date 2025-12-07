import re

import MySQLdb
from flask import Flask, request, session, render_template, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'dev'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '22mysql@V03'
app.config['MYSQL_DB'] = 'dinhlogin'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['logged_in'] = True
            session['username'] = account['username']
            session['id'] = account['id']
            return render_template('index.html', msg = 'Logged in successfully!')
        else:
            msg = 'Incorrect username or password'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = "Account already exists"
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            msg = 'Email address is not valid'
        elif not re.match(r'^[0-9a-zA-Z_-]+', username):
            msg = 'Username must be alphanumeric'
        elif not username or not password or not email:
            msg = 'Username or password is empty'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'Account created'
    return render_template('register.html', msg=msg)
if __name__ == '__main__':
    app.run(debug=True)
