import string
import random
from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
import smtplib

app = Flask(__name__)
sslify = SSLify(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://tRGvxd7v5H:gubRkugtXh@remotemysql.com/tRGvxd7v5H'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super-secret-key"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return login.query.get(username)

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('factsworld1109@gmail.com', 'pnhnywcnwixzhhie')
    server.sendmail('factsworld1109@gmail.com', to, content)
    server.close()


class login(UserMixin, db.Model):
    def get_id(self):
        return (self.username)
    username = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    birthday = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(100), nullable=False)

    def __str__(self):
         return f'{self.username}: {self.first_name}'

@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        pass
        username = request.form.get('username').lower()
        email = request.form.get('username')
        password = request.form.get('password')
        user = login.query.filter_by(username=username).first()
        user1 = login.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return current_user.username
        elif user1 and user1.password == password:
            login_user(user1)
            return current_user.username
        else:
            return 'Not Available.'
    return render_template('login.html', title='Login')

@app.route("/", methods=["GET", "POST"])
def index():
    msg = None
    if request.method == 'POST':
        session["username"] = request.form.get('username').lower()
        session["first_name"] = request.form.get('first_name')
        session["last_name"] = request.form.get('last_name')
        session["password"] = request.form.get('password')
        rpassword = request.form.get('rpassword')
        session["birthday"] = request.form.get('birthday')
        session["gender"] = request.form.get('gender')
        session["email"] = request.form.get('email')
        session["about"]= request.form.get('about')
        sign_user = login.query.filter_by(username=session.get('username')).first()
        sign_email = login.query.filter_by(email=session.get('email')).first()
        if sign_user:
            msg = 'Username Used.'
        elif sign_email:
            msg = 'Already an account with this email.'
        elif session.get('password')!=rpassword:
            msg='Password and repeat password are different.'
        else:
            N = 7
            res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
            session['random'] = res
            return redirect('/verify')
    return render_template('index.html', msg=msg, title='Sign up')

@app.route("/verify", methods=["GET", "POST"])
def verify():
    to = session.get('email')
    content = f'Your verification code is {session.get("random")}.'
    sendEmail(to, content)
    if request.method == 'POST':
        code = request.form.get('code')
        if code == session['random']:
            username = session.get('username')
            first_name = session.get('first_name')
            last_name = session.get('last_name')
            password = session.get('password')
            birthday = session.get('birthday')
            gender = session.get('gender')
            email = session.get('email')
            about = session.get('about')
            info = login(username=username, first_name=first_name, last_name=last_name, password=password, birthday=birthday, gender=gender, email=email, about=about)
            try:
                db.session.add(info)
                db.session.commit()
                return 'Added'
            except:
                return 'Something went wrong your credentials not uploaded.'
        else:
            return 'Wrong'
    return render_template('verify.html', title='Email verification', email=session.get('email'))

if __name__ == '__main__':
    app.run(debug=True)
