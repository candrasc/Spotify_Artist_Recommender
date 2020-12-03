from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired



class SubmissionForm(FlaskForm):
    artist_name = StringField('Artist Name', [validators.Length(min=1)])
    num_recos = StringField('Number of recommendations')
    Submit = SubmitField('Submit')
