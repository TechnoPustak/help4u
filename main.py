from flask_mail import Mail, Message
from flask import Flask, render_template, request, session, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

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
def signup():
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
        sign_user = login.query.filter_by(username=session.get('username')).first()
        sign_email = login.query.filter_by(email=email).first()
        if sign_user:
            flash('Username Used.')
        elif sign_email:
            flash('Already an account with this email.')
        elif session.get('password')!=rpassword:
            flash('Password and repeat password are different.')
        else:
            token = s.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', sender='factsworld1109@gmail.com', recipients=[email])
            link = url_for('verify', token=token, _external=True)
            msg.body = 'Your link is {} but go on this link from the same device used for registration.'.format(link)
            mail.send(msg)
            return render_template('box.html', email=email)
    return render_template('signup.html', msg=lol, title='Sign up')

@app.route("/verify/<token>")
def verify(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        username = session.get('username')
        first_name = session.get('first_name')
        last_name = session.get('last_name')
        password = session.get('password')
        birthday = session.get('birthday')
        gender = session.get('gender')
        info = login(username=username, first_name=first_name, last_name=last_name, password=password, birthday=birthday, gender=gender, email=email)
        db.session.add(info)
        db.session.commit()
        flash('Your account has been created successfully.')
        return redirect('/login')
    except SignatureExpired:
        return 'Your link expired.'
    except BadSignature:
        return 'No such link.'

@app.route("/forgot-password", methods=["GET", "POST"])
def passwordemail():
    if request.method == 'POST':
        email = request.form.get('code')
        token = s.dumps(email, salt='change-pass')
        msg = Message('Password Change', sender='factsworld1109@gmail.com', recipients=[email])
        link = url_for('changepass', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)
        return render_template('box.html', email=email)
    return render_template('password.html', title='Password Recovery')

@app.route('/change-password/<token>')
def changepass(token):
    try:
        email = s.loads(token, salt='change-pass', max_age=3600)
        email_user = login.query.filter_by(email=email).first()
        return 'True'
    except SignatureExpired:
        return 'False'

if __name__ == '__main__':
    app.run(debug=True)
