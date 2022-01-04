from datetime import datetime
from flask import current_app , jsonify
from flaskblog import db , login_manager 
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin # isauthenticated, isactive , isanonymous , getid  
import json
# need this for managing session

'''Load User data in Session - login manager '''
@login_manager.user_loader

def load_user(user_id):
    return User.objects.get(id =user_id)

class User(db.Document,UserMixin):

    username = db.StringField(unique=True,max_length=20)
    email = db.StringField(required= True, unique = True,max_length=120)
    image_file = db.StringField(max_length=40,required= True,default = 'profile.jpg')
    password = db.StringField(required= True,max_length=60)
    posts = db.ListField(db.ReferenceField('Post'))
    
    meta = {'allow_inheritance': True}
    
    def get_reset_token(self,expires_sec=18000):
        s = Serializer(current_app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id': str(self.pk)}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.objects.get(id = user_id)
        
    

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Document):
    '''
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable = False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    '''
    
    title = db.StringField(required= True,max_length=120)
    date_posted = db.DateTimeField(required=True,default=datetime.utcnow)
    content  = db.StringField(required= True,max_length= 500)
    author =  db.ReferenceField('User')
    
    meta = {'allow_inheritance': True}
    
    

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"



