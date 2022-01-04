from flask_wtf import FlaskForm 
from flask_wtf.file import FileField ,FileAllowed
from flask_login import current_user
from wtforms import StringField , PasswordField , SubmitField , BooleanField ,TextAreaField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError
from flaskblog.models import User



class RegistrationForm(FlaskForm):

	username  = StringField('Username'
		                   ,validators = [DataRequired(),Length(min=2,max=20)] )

	email = StringField('Email',
						validators=[DataRequired(),Email()])

	password = PasswordField('Password',
								validators = [DataRequired(),Length(min=8,max=20)])

	confirm_password = PasswordField('Confirm password',
									validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_username(self,username):
		user  = User.objects(username=username.data).first()
		if user :
			raise ValidationError('Username is taken . Use different username')

	def validate_email(self,email):
		email = User.objects(email=email.data).first()
		if email :
			raise ValidationError('Email is taken . Use different email ')



class LoginForm(FlaskForm):

	email = StringField('Email',
						validators = [DataRequired(),Email()])
	password = PasswordField('Confirm Password',
								validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):

	username  = StringField('Username'
		                   ,validators = [DataRequired(),Length(min=2,max=20)] )

	email = StringField('Email',
						validators=[DataRequired(),Email()])

	picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField(' Update ')

	def validate_username(self,username):
		if username.data != current_user.username:
			user  = User.objects(username=username.data).first()
			if user :
				raise ValidationError('That Username is taken . Use different username')

	def validate_email(self,email):
		if 	email.data != current_user.email:
			user = User.objects(email=email.data).first()
			if user :
				raise ValidationError('That new email is taken . Use different email ')


class RequestResetForm(FlaskForm):

	email = StringField('Email',
						validators=[DataRequired(),Email()])

	submit = SubmitField('Request Password Reset')

	def validate_username(self,username):
		user  = User.objects.get(username=username.data)
		if user is None :
			raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):

	password = PasswordField('Password',validators=[DataRequired()])

	confirm_password = PasswordField('confirm Password',
										validators=[DataRequired(),EqualTo('password')])

	submit = SubmitField('Reset Password')
