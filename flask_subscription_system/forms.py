from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Email, Length, EqualTo,
                                ValidationError)
from flask_subscription_system import db
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

        print("FORM:: Validation....")
        duplicate_blog = Blog.query.filter_by(blog_id=blog_id.data).first()
        print("Duplicate_blog", str(duplicate_blog))
        if duplicate_blog and not duplicate_blog.is_expired():
            raise ValidationError('Blog_id already used! Try another.')

        if duplicate_blog and duplicate_blog.is_expired():
            print("FORM:: deleting blog")
            db.session.delete(duplicate_blog)
            db.session.commit()
        print("FORM: exiting")


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

    blog_id = StringField("blog-id", validators=[DataRequired()])
    password = PasswordField("password", validators=[
        DataRequired(), Length(min=3)])
    subject = StringField("Subject", validators=[DataRequired()])
    topic = StringField("Topic", validators=[DataRequired()])
    content = TextAreaField("Content")
    submit = SubmitField('Publish')

    def validate_user(self, blog_id, password):
        '''
        Checks if email is already registered and raises a
        ValidationError and flashes a warning if so
        '''

        blog = Blog.query.filter_by(blog_id=blog_id.data).first()
        if blog and bcrypt.check_password_hash(blog.password, password.data):
            return

        raise ValidationError("Invalid username or password match")
