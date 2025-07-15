from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ChatForm(FlaskForm):
    # require the user to choose a model so the route logic doesn't
    # attempt to split an empty value when no models are enabled
    model   = SelectField("LLM", validators=[DataRequired()])
    prompt  = TextAreaField("Prompt", validators=[DataRequired()])
    submit  = SubmitField("Send")
