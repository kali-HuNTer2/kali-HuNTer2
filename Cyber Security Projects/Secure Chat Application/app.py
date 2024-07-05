from flask import Flask, render_template_string, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_socketio import SocketIO, send, emit
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template_string(register_template, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('chat'))
        else:
            flash('Login unsuccessful. Check email and password', 'danger')
    return render_template_string(login_template, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat')
@login_required
def chat():
    return render_template_string(chat_template, username=current_user.username)

@socketio.on('message')
def handle_message(msg):
    if current_user.is_authenticated:
        message = Message(content=msg, user_id=current_user.id)
        db.session.add(message)
        db.session.commit()
        send({'msg': msg, 'user': current_user.username}, broadcast=True)
    else:
        emit('redirect', {'url': url_for('login')})

login_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Chat App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <h2>Login</h2>
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <div>
                {{ form.email.label }}<br>
                {{ form.email(size=32) }}
            </div>
            <div>
                {{ form.password.label }}<br>
                {{ form.password(size=32) }}
            </div>
            <div>
                {{ form.remember() }} {{ form.remember.label }}
            </div>
            <div>
                {{ form.submit() }}
            </div>
        </form>
        <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
    </div>
</body>
</html>
"""

register_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Chat App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <h2>Register</h2>
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <div>
                {{ form.username.label }}<br>
                {{ form.username(size=32) }}
            </div>
            <div>
                {{ form.email.label }}<br>
                {{ form.email(size=32) }}
            </div>
            <div>
                {{ form.password.label }}<br>
                {{ form.password(size=32) }}
            </div>
            <div>
                {{ form.confirm_password.label }}<br>
                {{ form.confirm_password(size=32) }}
            </div>
            <div>
                {{ form.submit() }}
            </div>
        </form>
        <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
    </div>
</body>
</html>
"""

chat_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Chat App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='main.css') }}">
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <h2>Chat Room</h2>
        <div id="chat-box">
            <div id="messages"></div>
            <input id="message-input" autocomplete="off" placeholder="Type a message..." /><button id="send-button">Send</button>
        </div>
        <script>
            document.addEventListener('DOMContentLoaded', () => {
                const socket = io.connect('http://' + document.domain + ':' + location.port);

                socket.on('message', function(data) {
                    const messages = document.getElementById('messages');
                    const messageItem = document.createElement('div');
                    messageItem.textContent = data.user + ': ' + data.msg;
                    messages.appendChild(messageItem);
                });

                const sendButton = document.getElementById('send-button');
                const messageInput = document.getElementById('message-input');
                
                sendButton.addEventListener('click', () => {
                    socket.send(messageInput.value);
                    messageInput.value = '';
                });
            });
        </script>
        <p><a href="{{ url_for('logout') }}">Logout</a></p>
    </div>
</body>
</html>
"""

css_content = """
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.container {
    background: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.flash {
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 5px;
}

.flash.success {
    background-color: #d4edda;
    color: #155724;
}

.flash.danger {
    background-color: #f8d7da;
    color: #721c24;
}

#chat-box {
    border: 1px solid #ccc;
    padding: 10px;
    margin-top: 10px;
}

#messages {
    height: 200px;
    overflow-y: scroll;
    border-bottom: 1px solid #ccc;
    margin-bottom: 10px;
    padding-bottom: 10px;
}

#message-input {
    width: calc(100% - 60px);
    padding: 10px;
}

#send-button {
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}
"""

import os
if not os.path.exists('static'):
    os.makedirs('static')
with open('static/main.css', 'w') as f:
    f.write(css_content)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
