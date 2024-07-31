from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class HashFieldValueForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    secondName = StringField('Second name', validators=[DataRequired()])
    username =  StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    skills = StringField('Skills', validators=[DataRequired()])
    hobby = StringField('Hobby', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserUpdateForm(FlaskForm):
    name = StringField('Name')
    secondName = StringField('Second name')
    age = StringField('Age')
    skills = StringField('Skills')
    hobby = StringField('Hobby')
    update = SubmitField('Update')
