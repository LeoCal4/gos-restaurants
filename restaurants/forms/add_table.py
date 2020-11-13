import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class TableForm(FlaskForm):
    """Form created to allow the operator to add tables to his restaurant

    """
    number = f.IntegerField('Number', validators=[DataRequired()])
    max_capacity = f.IntegerField('Max capacity', validators=[DataRequired()])
    display = ['number', 'max_capacity']
