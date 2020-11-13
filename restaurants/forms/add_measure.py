import wtforms as f
from flask_wtf import FlaskForm


class MeasureForm(FlaskForm):
    """Form created to allow the operator to add precaution measures,
    selected from a specific list

    """

    list_measure = ["Hand sanitizer", "Plexiglass", "Spaced tables",
                    "Sanitized rooms", "Temperature scanners"]
    measure = f.SelectField('Measure', choices=list_measure, default=1)
    display = ['measure']
