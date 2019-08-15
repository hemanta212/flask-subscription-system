from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms.validators import (DataRequired, Email, Length, EqualTo,
                                ValidationError)
from flask_subscription_system.models import Blog


class RegisterForm(FlaskForm):
    '''
    Form for signing up the user
    Attributes:
        email [str]: email of the user
        submit [submit]: submit field
    Methods:
        validate_id(): checks if blog_id is already registered
    '''

    name = StringField("Blog name", validators=[DataRequired()])
    blog_id = StringField("Blog id", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[
        DataRequired(), Length(min=3)])
    confirm_password = PasswordField("confirm password", validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_blog_id(self, blog_id):
        '''
        Checks if email is already registered and raises a
        ValidationError and flashes a warning if so
        '''
        duplicate_blog = Blog.query.filter_by(blog_id=blog_id.data).first()
        if duplicate_blog and duplicate_blog.verified:
            raise ValidationError('Blog_id already used! Try another.')


class SubscriptionForm(FlaskForm):
    '''
    Form for signing up the user
    Attributes:
        email [str]: email of the user
        submit [submit]: submit field
    Methods:
        validate_email(): checks if email is already registered
    '''

    email = StringField("Email address", validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')


class PostForm(FlaskForm):
    '''
    Form for signing up the user
    Attributes:
        email [str]: email of the user
        submit [submit]: submit field
    Methods:
        validate_email(): checks if email is already registered
    '''

    subject = StringField("Subject", validators=[DataRequired()])
    topic = StringField("Topic", validators=[DataRequired()])
    content = TextField("Content")
    submit = SubmitField('Subscribe')
