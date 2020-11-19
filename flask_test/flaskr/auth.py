#create a blueprint named auth
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth') #name tell the blueprint where it is being defined, url prefix is added to the beginning of all URLs associated with the blueprint



@bp.route('/register', methods=('GET', 'POST')) #when flask recieves a request to /auth/register
def register():
    if request.method == 'POST': #if the user submitted the form validate the input
        username = request.form['username'] #request form is a special type of dict mapping
        password = request.form['password']
        db = get_db()
        error = None

        if not username: #validate that the fields aren't empty
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute( #validate that the username and password don't exist already
                'INSERT INTO user (username, password) VALUES (?, ?)', #? is a place holder for user submitted data
                (username, generate_password_hash(password))
            )
            db.commit() #if validation is successful insert new entry into the database
            return redirect(url_for('auth.login'))

        flash(error) #if validation fails

    return render_template('auth/register.html') #when the user navigates tothe address or there is a validation error the template is rendered



@bp.route('/login', methods=('GET', 'POST')) #when flask recieves a request to /auth/login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password): #securely checks the passwords match
            error = 'Incorrect password.'

        if error is None: #when validation is successful user id is stored in a new session, a cookie is sent to the browser with this data for subsequent requests
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')



@bp.before_app_request #runs before any request if the user id is stored in the session and gets teh users data from the database
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()



@bp.route('/logout') #removes the user from the session
def logout():
    session.clear()
    return redirect(url_for('index'))



def login_required(view): #a function to wrap around another for when a user is required to be logged in
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

