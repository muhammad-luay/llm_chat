from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ChatForm(FlaskForm):
    model   = SelectField("LLM")
    prompt  = TextAreaField("Prompt", validators=[DataRequired()])
    submit  = SubmitField("Send")
