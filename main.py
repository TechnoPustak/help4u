import string
import random
from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, session, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import SignatureExpired
# import smtplib

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'factsworld1109@gmail.com'
app.config['MAIL_PASSWORD'] = 'pnhnywcnwixzhhie'
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)
s = URLSafeTimedSerializer('my-secret')
sslify = SSLify(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kiympnjddnapxr:c3802988090175e2d6f23d27f2f8ef078d7dfea85a76968cb364d41ea72d7a13@ec2-54-154-101-45.eu-west-1.compute.amazonaws.com/d9h0lkg28n6udh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super-secret-key"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return login.query.get(username)

# def sendEmail(to, content):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     server.login('factsworld1109@gmail.com', 'pnhnywcnwixzhhie')
#     server.sendmail('factsworld1109@gmail.com', to, content)
#     server.close()

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
        username = request.form.get('uid').lower()
        email = request.form.get('uid')
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
    lol = None
    if request.method == 'POST':
        session["username"] = request.form.get('username').lower()
        session["first_name"] = request.form.get('first_name')
        session["last_name"] = request.form.get('last_name')
        session["password"] = request.form.get('password')
        rpassword = request.form.get('rpassword')
        session["birthday"] = request.form.get('birthday')
        session["gender"] = request.form.get('gender')
        email = request.form.get('email')
        session["about"]= request.form.get('about')
        sign_user = login.query.filter_by(username=session.get('username')).first()
        sign_email = login.query.filter_by(email=session.get('email')).first()
        if sign_user:
            lol = 'Username Used.'
        elif sign_email:
            lol = 'Already an account with this email.'
        elif session.get('password')!=rpassword:
            lol='Password and repeat password are different.'
        else:
            token = s.dumps(email, salt='email-confirm')
            # N = 7
            # res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
            # session['random'] = res
            msg = Message('Confirm Email', sender='factsworld1109@gmail.com', recipients=[email])
            link = url_for('verify', token=token, external=True)
            msg.body = 'Your link is {}'.format(link)
            mail.send(msg)
            return link
    return render_template('index.html', msg=lol, title='Sign up')

@app.route("/verify/<token>")
def verify(token):
    # to = session.get('email')
    # content = f'Your verification code is {session.get("random")}.'
    # sendEmail(to, content)
    # if request.method == 'POST':
    #     code = request.form.get('code')
    #     if code == session['random']:
    #         username = session.get('username')
    #         first_name = session.get('first_name')
    #         last_name = session.get('last_name')
    #         password = session.get('password')
    #         birthday = session.get('birthday')
    #         gender = session.get('gender')
    #         email = session.get('email')
    #         about = session.get('about')
    #         info = login(username=username, first_name=first_name, last_name=last_name, password=password, birthday=birthday, gender=gender, email=email, about=about)
    #         try:
    #             db.session.add(info)
    #             db.session.commit()
    #             session.pop('random')
    #             return 'Added'
    #         except:
    #             return 'Something went wrong your credentials not uploaded.'
    #     else:
    #         return 'Wrong'
    # return render_template('verify.html', title='Email verification', email=session.get('email'))
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        return True
    except SignatureExpired:
        return False

@app.route("/forgot-password", methods=["GET", "POST"])
def passwordemail():
    if request.method == 'POST':
        to = request.form.get('code')
        N = 30
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
        session['password-change'] = res
        content = "You can change your help4you account password from the following link :- https://help4you.herokuapp.com/change-password/"+str(res)
        sendEmail(to, str(content))
        return content
    return render_template('password.html', title='Password Recovery')

if __name__ == '__main__':
    app.run(debug=True)
