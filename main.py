from flask_mail import Mail, Message
import json
import time
import convertcode
from flask import Flask, render_template, request, session, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
    c.seek(0)
    database = json.load(c)["database"]
    c.seek(0)
    statics = json.load(c)["statics"]

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['email']
app.config['MAIL_PASSWORD'] = params['email-password']
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)

s = URLSafeTimedSerializer('my-secret')
sslify = SSLify(app)

# heroku pg:psql postgresql-spherical-80201 --app help4you
app.config['SQLALCHEMY_DATABASE_URI'] = f"{database['app']}://{database['user']}:{database['password']}@{database['host']}/{database['database']}"
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
    password = db.Column(db.String(1000), nullable=False)
    birthday = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(), nullable=False)


class posts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(50000), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(100), nullable=False)


class answers(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(50000), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    question_id = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(100), nullable=False)


@app.errorhandler(401)
def unauthorized(e):
    return redirect('/login')


@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == 'POST':
        username = request.form.get('uid').lower()
        email = request.form.get('uid')
        password = request.form.get('password')
        user = login.query.filter_by(username=username).first()
        user1 = login.query.filter_by(email=email).first()
        if user and convertcode.decodecode(user.password) == password:
            login_user(user, remember=True)
            return redirect('/dashboard')
        elif user1 and convertcode.decodecode(user1.password) == password:
            login_user(user1, remember=True)
            return redirect('/dashboard')
        else:
            flash('Entered Credentials are wrong.', 'danger')
            return render_template('login.html', title='Login', params=params)
    return render_template('login.html', title='Login', params=params)


@app.route("/", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        session["username"] = request.form.get('username').lower()
        session["first_name"] = request.form.get('first_name')
        session["last_name"] = request.form.get('last_name')
        session["password"] = request.form.get('password')
        rpassword = request.form.get('rpassword')
        session["birthday"] = request.form.get('birthday')
        session["gender"] = request.form.get('gender')
        email = request.form.get('email')
        sign_user = login.query.filter_by(
            username=session.get('username')).first()
        sign_email = login.query.filter_by(email=email).first()
        if sign_user:
            flash('Username Used.')
        elif sign_email:
            flash('Already an account with this email.')
        elif session.get('password') != rpassword:
            flash('Password and repeat password are different.')
        else:
            token = s.dumps(email, salt='email-confirm')
            msg = Message(
                'Confirm Email', sender='factsworld1109@gmail.com', recipients=[email])
            link = url_for('verify', token=token, _external=True)
            msg.body = 'Your link is {} but go on this link from the same device and browser used for registration.'.format(
                link)
            mail.send(msg)
            return render_template('box.html', email=email)
    return render_template('signup.html', title=f"{params['title']}: Sign Up for a new account", params=params)


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    questions = posts.query.filter_by().all()
    users = login.query.filter_by().all()
    if request.method == 'POST':
        username = current_user.username
        post = request.form.get('question')
        subject = request.form.get('subject')
        grade = request.form.get('grade')
        info = posts(username=username, post=post,
                     subject=subject, time=time.time(), grade=grade)
        db.session.add(info)
        db.session.commit()
        return redirect('/dashboard')
    return render_template("dashboard.html", title=f"{params['title']}: Ask and Answer Questions", questions=questions, users=users, time=time.time())


@app.route('/answer/<int:sno>', methods=["GET", "POST"])
@login_required
def answer(sno):
    users = login.query.filter_by().all()
    question = posts.query.filter_by(sno=sno).first()
    myanswers = answers.query.filter_by(question_id=str(sno)).all()
    if request.method == 'POST':
        myanswer = request.form.get('answer')
        answer_info = answers(
            answer=myanswer, username=current_user.username, question_id=sno, time=time.time())
        db.session.add(answer_info)
        db.session.commit()
        return redirect('/answer/'+str(sno))
    if question:
        return render_template('answer.html', title=f"{params['title']}: Give Answers", question=question, time=time.time(), users=users, sno=sno, answers=myanswers)
    else:
        return redirect('/dashboard')


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
        encpass = convertcode.convertcode(password)
        profile_pic = statics['profile_pic']
        info = login(username=username, first_name=first_name, last_name=last_name, password=encpass,
                     birthday=birthday, gender=gender, email=email, profile_pic=profile_pic)
        db.session.add(info)
        db.session.commit()
        flash('Your account has been created successfully.', 'success')
        return redirect('/login')
    except SignatureExpired:
        return 'Your link has been expired.'
    except BadSignature:
        return 'No such link.'


@app.route("/forgot-password", methods=["GET", "POST"])
def passwordemail():
    if request.method == 'POST':
        email = request.form.get('code')
        token = s.dumps(email, salt='change-pass')
        msg = Message('Password Change',
                      sender='factsworld1109@gmail.com', recipients=[email])
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


@app.route("/google4a74fd24a326259f.html")
def googlesearchverify():
    return render_template('google4a74fd24a326259f.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You has been logged out successfully. ', 'success')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
