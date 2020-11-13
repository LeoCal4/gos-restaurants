import wtforms as f
from flask_wtf import FlaskForm
from wtforms.fields.html5 import TimeField, IntegerField
from wtforms.validators import DataRequired,NumberRange


class StayTimeForm(FlaskForm):
    hours = IntegerField('Hours', default=1, validators=[DataRequired()])
    minutes = IntegerField('Minutes', default=0,validators=[DataRequired()])
    display = ['hours', 'minutes']

    
    def validate_on_submit(self):
        hours = self.hours.data
        minutes = self.minutes.data
        if hours < 0 or minutes < 0:
            return False
        else:
            return True