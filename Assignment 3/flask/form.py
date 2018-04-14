from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AwsForm(FlaskForm):
  	b1 = StringField('b1', validators=[DataRequired()])
    b2 = StringField('b2', validators=[DataRequired()])
    b3 = StringField('b3', validators=[DataRequired()])
    b4 = StringField('b4', validators=[DataRequired()])
    b5 = StringField('b5', validators=[DataRequired()])
    submit = SubmitField('Submit')

    
