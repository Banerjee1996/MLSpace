from flask import Flask, jsonify
#from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from mongoengine import connect
from bson.json_util import ObjectId
import json
from flask.json import JSONEncoder


from mongoengine.base import BaseDocument
from mongoengine.queryset.base import BaseQuerySet

class MongoEngineJSONEncoder(JSONEncoder):
    def default(self,obj):
        if isinstance(obj,BaseDocument):
            return json_util._json_convert(obj.to_mongo())
        elif isinstance(obj,BaseQuerySet):
            return json_util._json_convert(obj.as_pymongo())
        return JSONEncoder.default(self, obj)



db = MongoEngine() # Database framework 
bcrypt = Bcrypt()  # Encyption of password
login_manager = LoginManager()  # Login session manager 
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail( ) #Mail Class



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    connect('flaskblog')
    #db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    
    app.json_encoder = MongoEngineJSONEncoder
    

    return app

'''
Sqlalchemy


from flaskblog import db
from flaskblog.models import User,Post
user = User.query.all() # send all users in DB
user = User.query.first() # send the first ()

# code to see the user DB and post DB
app = create_app()
from flaskblog.models import User,Post
with app.app_context():
    user = User.query.all()
   


'''