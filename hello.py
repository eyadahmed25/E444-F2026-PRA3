from flask import Flask, render_template, session, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime
import re

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
    form = NameForm()
    email_warning = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        if 'utoronto' not in email:
            email_warning = 'Please use your UofT email.'
        else:
            session['name'] = name
            session['email'] = email
            form.name.data = ''
            form.email.data = ''
            return redirect(url_for('chat'))
        form.name.data = ''
        form.email.data = ''
    return render_template('index.html', form=form, email_warning=email_warning,
                            current_time=datetime.utcnow())


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message = request.json['message']
        reply = get_bot_reply(message)
        return {'reply': reply}

    if 'name' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', name=session['name'])


def get_bot_reply(message):
    # session-backed memory dict, persists across requests for this browser
    session.setdefault('memory', {})

    name_match = re.search(r"my name is (.+)", message, re.IGNORECASE)
    if name_match:
        remembered_name = name_match.group(1).strip().rstrip('.')
        session['memory']['name'] = remembered_name
        session.modified = True  # required: mutating a nested dict doesn't auto-flag the session as changed
        return f"Nice to meet you, {remembered_name}!"

    if 'what is my name' in message.lower():
        remembered_name = session.get('memory', {}).get('name')
        if remembered_name:
            return f"Your name is {remembered_name}."
        return "I don't know your name yet. Try telling me: 'My name is ...'"

    if 'hello' in message.lower():
        return "Hello!"

    return "I don't understand."


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
