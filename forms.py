from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextField, IntegerField, SelectField, TextAreaField
from wtforms import validators, ValidationError
from wtforms.widgets import PasswordInput

class SignUpForm(FlaskForm):
    city = StringField('Current City')
    email = TextField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    name = TextField('Username', [validators.Required(), validators.Length(min=2, max=100)])
    password = StringField('Password', widget=PasswordInput(hide_value=False))
    pronouns = StringField('Personal Pronouns')
    race = StringField('Race/Ethnicity')
    submit = SubmitField("Sign Up")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

class SignInForm(FlaskForm):
    email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
    password = StringField('Password', widget=PasswordInput(hide_value=False))
    submit = SubmitField("Log In")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

class CitySearchForm(FlaskForm):
    city = StringField('City', [validators.Required("Please choose a city.")])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

class CreateMoveForm(FlaskForm):
    move_type = SelectField('Type', choices=[('jobs', 'Jobs'), ('entertainment', 'Entertainment'), ('hair', 'Hair'), ('religious', 'Religious'),('kids', 'Kids'),('housing', 'Housing'),('etc', 'Etc.')])
    city = SelectField('City', choices=[('Atlanta', 'Atlanta'), ('Boston', 'Boston'), ('Minneapolis', 'Minneapolis'), ('San Francisco', 'San Francisco')])
    text = TextAreaField("So what's the move?", [validators.Required("Please enter your move.")])
    submit = SubmitField("Share move")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

class CommentForm(FlaskForm):
    text = TextAreaField('Enter your comment', [validators.Required("Please choose a comment.")])
    submit = SubmitField("Post comment")

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
