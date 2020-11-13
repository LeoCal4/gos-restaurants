import wtforms as f
from flask_wtf import FlaskForm
from wtforms.fields.html5 import TimeField
from wtforms.validators import DataRequired


class TimesForm(FlaskForm):
    """Form created to allow the operator to add opening hours to his restaurant
    """
    
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    day = f.SelectField('Week Day', choices=week_days, validators=[DataRequired()])
    start_time = TimeField('Start time',
                            format='%H:%M',
                           validators=[
                               DataRequired()
                           ])
    end_time = TimeField('End time',
                        format='%H:%M',
                         validators=[
                             DataRequired()
                         ])
    display = ['day', 'start_time', 'end_time']
