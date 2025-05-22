from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, unset_jwt_cookies, create_access_token, set_access_cookies, jwt_required, get_jwt_identity
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from utils.forms import RegisterForm, LoginForm, TwoFactorForm
import random
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['WTF_CSRF_SECRET_KEY'] = 'another_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # HTTPS yoksa False olmalı
app.config['JWT_COOKIE_CSRF_PROTECT'] = True

# Mail ayarları - Şifreyi .env dosyasına taşıman önerilir
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ureali90@gmail.com'
app.config['MAIL_PASSWORD'] = 'ysrndvxpnltotkph'
app.config['MAIL_DEFAULT_SENDER'] = 'ureali90@gmail.com'

# Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
mail = Mail(app)

# ------------------ MODELLER ------------------ #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

# ------------------ YARDIMCI ------------------ #
def send_verification_email(email, code):
    """2FA doğrulama kodunu e-posta olarak gönderir."""
    msg = Message('Your 2FA Code', recipients=[email])
    msg.body = f'Your verification code is: {code}'
    mail.send(msg)

# ------------------ ROUTES ------------------ #
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username_error = None
    email_error = None

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(username=username).first():
            username_error = "This username is already taken."
        elif User.query.filter_by(email=email).first():
            email_error = "This email address is already registered."
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form, username_error=username_error, email_error=email_error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            verification_code = str(random.randint(100000, 999999))
            session['2fa_user'] = user.username
            session['2fa_code'] = verification_code
            send_verification_email(user.email, verification_code)
            return redirect(url_for('verify_2fa'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

@app.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    form = TwoFactorForm()

    if '2fa_user' not in session or '2fa_code' not in session:
        flash('Session expired or unauthorized access.', 'warning')
        return redirect(url_for('login'))

    if form.validate_on_submit():
        entered_code = form.code.data
        if entered_code == session.get('2fa_code'):
            access_token = create_access_token(identity=session['2fa_user'])
            response = make_response(redirect(url_for('dashboard')))
            set_access_cookies(response, access_token)
            session.pop('2fa_user', None)
            session.pop('2fa_code', None)
            flash('2FA verification successful.', 'success')
            return response
        else:
            flash('Incorrect verification code.', 'danger')

    return render_template('verify_2fa.html', form=form)

@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
def logout():
    response = redirect(url_for('index'))
    unset_jwt_cookies(response)
    flash('You have been logged out.', 'info')
    return response

# ------------------ UYGULAMA BAŞLAT ------------------ #
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
