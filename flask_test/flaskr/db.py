#connects to database
import sqlite3

import click
from flask import current_app, g #g is an object unique to each request so that stored data can be accessed by multiple functions during the request, current_app points to the flask app handling the request 
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect( #points to the  file at DATABASE
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #returns rowns that behave like dicts so we can access columns by name

    return g.db


def close_db(e=None): #checks if a connection has been created, by checking if g.db was set
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: #opens a file relative to the current package, the flaskr package
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db) #called when cleaning up after a response
    app.cli.add_command(init_db_command) #a new command that is called with the flask command

