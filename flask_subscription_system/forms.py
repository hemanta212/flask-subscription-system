from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
#from flask_final.users.models import User


class RegisterForm(FlaskForm):
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

    test = '''\
    def validate_email(self, email):

        #Checks if email is already registered and raises a
        #ValidationError and flashes a warning if so

        duplicate_user = User.query.filter_by(email=email.data).first()
        if duplicate_user:
            flash('Email already registered. try another', 'warning')
            raise ValidationError('Email already registered. try another')
    '''
