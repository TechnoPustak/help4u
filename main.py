import string
import random
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
import smtplib

app = Flask(__name__)
sslify = SSLify(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super-secret-key"
db = SQLAlchemy(app)
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('factsworld1109@gmail.com', 'pnhnywcnwixzhhie')
    server.sendmail('factsworld1109@gmail.com', to, content)
    server.close()


class login(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    birthday = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(100), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    msg = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        rpassword = request.form.get('rpassword')
        email = request.form.get('email')
        sign_user = login.query.filter_by(username=username).first()
        sign_email = login.query.filter_by(email=email).first()
        if sign_user:
            msg = 'Username Used.'
        elif sign_email:
            msg = 'Already an account with this email.'
        elif password!=rpassword:
            msg='Password and repeat password are different.'
        else:
            session['email'] = email
            return redirect('/verify/email')
    return render_template('index.html', msg=msg, title='Sign up')

@app.route("/verify/email")
def verify():
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase + string.digits, k = N))
    session['random'] = res
    print(res, session.get('email'))
    to = session.get('email')
    content = f'Your verification code is {res}'
    sendEmail(to, content)
    return render_template('verify.html', title='Email verification', email=session.get('email'))

if __name__ == '__main__':
    app.run(debug=True)
