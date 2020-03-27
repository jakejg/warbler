from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class MessageForm(FlaskForm):
    """Form for adding/editing messages."""

    text = TextAreaField('text', validators=[DataRequired()])


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditUserForm(FlaskForm):
    """Form for editing a user's profile"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[Email()])
    image_url = StringField('Image URL')
    header_image_url = StringField('Image URL')
    bio = StringField('Bio')
    password = PasswordField('Password', validators=[Length(min=6)])
    
class LikeMessage(FlaskForm):
    """Form for liking a message"""

    like_unlike = BooleanField()