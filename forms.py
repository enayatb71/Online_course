from flask_wtf import FlaskForm
from wtforms.fields import StringField,PasswordField,SubmitField,EmailField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Email, equal_to

class signup_form(FlaskForm):
    name = StringField('name', validators=[DataRequired('Name Field is Required')])
    email = EmailField('email', validators=[DataRequired('Email Field is Required'), Email('Email is invalid')])
    password = PasswordField('password', validators=[DataRequired('password Field is Required'), Length(min=6, message='password is less than 6 character')])
    confirm = PasswordField('confirm', validators=[equal_to('password',message='password not match')])

class signin_form(FlaskForm):
    email = EmailField('email', validators=[DataRequired('Email Field is Required'), Email('Email is invalid')])
    password = PasswordField('password', validators=[DataRequired('password Field is Required'), Length(min=6, message='password is less than 6 character')])

class change_password_form(FlaskForm):
    old_password = PasswordField('old_password', validators=[DataRequired('password Field is Required'), Length(min=6, message='password is less than 6 character')])     
    new_password = PasswordField('new_password', validators=[DataRequired('password Field is Required'), Length(min=6, message='password is less than 6 character')])
    confirm = PasswordField('confirm', validators=[equal_to('new_password',message='password not match')])

class add_new_user(FlaskForm):
    name = StringField('name', validators=[DataRequired('Name Field is Required')])
    email = EmailField('email', validators=[DataRequired('Email Field is Required'), Email('Email is invalid')])
    password = PasswordField('password', validators=[DataRequired('password Field is Required'), Length(min=6, message='password is less than 6 character')])

class edit_user_form(FlaskForm):
    name = StringField('name', validators=[DataRequired('Name Field is Required')])
    email = EmailField('email', validators=[DataRequired('Email Field is Required'), Email('Email is invalid')])

class add_course_from(FlaskForm):
    title = StringField('title', validators=[DataRequired('title field is required')])
    content = TextAreaField('content', validators=[DataRequired('content of course is required')])

class edit_course_form(FlaskForm):
    title = StringField('title', validators=[DataRequired('title field is required')])

class add_episode_form(FlaskForm):
    title = StringField('title', validators=[DataRequired('title field is required')])
    content = TextAreaField('content', validators=[DataRequired('content of course is required')])
    number = DecimalField('number', validators=[DataRequired('number of course is required')])

class edit_episode_form(FlaskForm):
    title = StringField('title', validators=[DataRequired('title field is required')])
    number = DecimalField('number', validators=[DataRequired('number of course is required')])