import sqlite3

from flask import Flask
from flask import render_template, session, redirect, url_for
from flask import request
import models as dbHandler
from flask_session import Session

app = Flask(__name__)

DATABASE = 'database.db'


sess = Session()

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)


@app.route('/create_database', methods=['GET', 'POST'])
def create_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE books (title TEXT, author TEXT)')
    conn.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, admin TinyInt(1) DEFAULT 0)')
    cur = conn.cursor()
    cur.execute('INSERT INTO users (username,password,admin) VALUES ("admin","qwerty","1")')
    conn.commit()
    conn.close()
    return 'Database created. Default admin user created (username: admin, password:qwerty)'


@app.route('/', methods=['POST', 'GET'])
def home():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cur =conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password,))
        users = cur.fetchone()
        if users:
            for row in cur.execute('SELECT admin FROM users WHERE username = ? AND password = ?', (username, password,)):
                variable = row[0]
                break
            else:
                variable = 5
            if variable == 1:
                session['admin'] = "username"
                return render_template('main.html')
            elif variable == 0:
                session['user'] = "username"
                return render_template('main.html')
        else:
            msg = 'Incorrect username/password!'
    return render_template("login.html", msg=msg)

@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        return render_template("login.html")
    elif 'admin' in session:
        session.pop('admin')
        return render_template("login.html")


@app.route('/main')
def homeBooks():
    if ('user' or 'admin' in session):
        return render_template('main.html')
    return render_template('login.html')


@app.route('/addBook', methods=['POST', 'GET'])
def addBooks():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        dbHandler.insertBook(title, author)
        books = dbHandler.retrieveBooks()
        return render_template('main.html', books=books)
    else:
        return render_template('main.html')


@app.route('/addUser', methods=['POST', 'GET'])
def addUsers():
    if request.method == 'POST':
        if request.form.get('admin') == "0":
            admin = 0
        elif request.form.get('admin') == "1":
            admin = 1
        username = request.form['username']
        password = request.form['password']
        dbHandler.insertUser(username, password, admin)
        users = dbHandler.retrieveUsers()
        return render_template('users.html', users=users)
    else:
        return render_template('users.html')


@app.route('/users', methods=['POST', 'GET'])
def homeUsers():
    if ('admin' in session):
        return render_template('users.html')
    return render_template('login.html')


@app.route('/users/<user_username>', methods=['POST', 'GET'])
def homeAdminbyName(user_username):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE username = '%s'" % user_username)
    data = cur.fetchone()
    cur.execute("SELECT user_id, username, password, admin FROM users where username='%s'" % user_username)
    users = cur.fetchall();
    return render_template('admin.html', users = users)

@app.route('/users_id/<userId>', methods=['POST', 'GET'])
def homeAdminbyID(userId):
    db = sqlite3.connect(DATABASE)
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = '%s'" % userId)
    data = cur.fetchone()
    cur.execute("SELECT user_id, username, password, admin FROM users where user_id='%s'" % userId)
    users = cur.fetchall();
    return render_template('admin.html', users = users)



app.config.from_object(__name__)
app.debug = True
app.run()
