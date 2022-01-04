
import os

class Config:
    SECRET_KEY = os.environ['SECRET_KEY'] # used for  keep the client-side sessions secure and use seesions in flask 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # location of DB data
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ['EMAIL_USER']
    MAIL_PASSWORD = os.environ['EMAIL_PASS']
    MONGODB_SETTINGS = {
    'host': 'mongodb:///site.db'
    }
    
    