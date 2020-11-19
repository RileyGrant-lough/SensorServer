#application setup
import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) #creates flask instance, __name__ is the name of the curretn Python module, instance relative config tells the app that the config files are in the instance folder
    app.config.from_mapping( #default configuration for the app
        SECRET_KEY='dev',  #change 'dev' to a random number before deploying, keeps data safe
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), #path to the instance folder, where the database file will be saved
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app


