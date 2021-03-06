import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail
from bson import json_util , ObjectId
import json
from flask import Flask, jsonify







def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/profile_pics',picture_fn)
    form_picture.save(picture_path)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)


    return picture_fn

def save_post_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _ ,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path,'static/post_pics',picture_fn)
    form_picture.save(picture_path)

    output_size = (600,400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)


    return picture_fn
def send_reset_email(user):
    
    token = user.get_reset_token()
    
    msg = Message('Password Reset request ' ,
                  sender = 'dankm4324@gmail.com' ,
                  recipients = [user.email] )
    msg.body = f'''To reset your password , visit the following link:
{url_for('users.reset_token',token=token ,_external=True)}

If you did not make this request , ignore it.
'''
    mail.send(msg)