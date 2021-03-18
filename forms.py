from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms_validators import NotEqualTo


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    private = BooleanField('Private Account')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UserEditForm(FlaskForm):
    """Form for editing current user."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    header_image_url = StringField('(Optional) Header Image URL')
    bio = StringField('Bio')
    private = BooleanField('Private Account')
    
    password = PasswordField('Password', validators=[Length(min=6)])

class ResetPasswordForm(FlaskForm):
    """Form for updating current user's password"""

    curr_password = PasswordField('Current Password', validators=[Length(min=6)])

    new_password = PasswordField('New Password', validators=[Length(min=6), 
    EqualTo('confirm', message='Passwords must match'), 
    NotEqualTo('curr_password', message='New password must be different than current')])

    confirm = PasswordField('Confirm New Password', validators=[Length(min=6)])