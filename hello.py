from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    email = None
    email_warning = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        if 'utoronto' not in email:
            email_warning = 'Please use your UofT email.'
            email = None
        form.name.data = ''
        form.email.data = ''
    return render_template('index.html', form=form, name=name, email=email,
                            email_warning=email_warning, current_time=datetime.utcnow())
