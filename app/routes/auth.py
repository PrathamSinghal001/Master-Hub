from flask import Blueprint, render_template, redirect, session, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.routes.forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/profile')
def profile():
    user_id = session.get("user_id")

    # ❌ If not logged in, redirect directly to login page
    if not user_id:
        flash("Please log in to access your profile.", "Danger")
        return redirect(url_for("auth.login"))

    # ✅ If logged in, get user info and show profile
    user = User.query.get(user_id)
    return render_template("profile.html", user=user)


# Register route
@auth_bp.route('/register', methods=["GET", "POST"])
def register():

    # for taking data from userbut this method is not safe 

    # if request.method == "POST":
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.name.data
        email = form.email.data
        password = form.password.data

        # check username & email already registered in database or not  
 
        if User.query.filter_by(username=username).first():
            flash("Username already taken by another", 'Danger')
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registers, please log-in", 'Danger')
            return redirect(url_for("auth.register")) 
        
        # passwrod hashing for security 
        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")

        # save to database
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration Succesful! you can login now", 'Success')
        return redirect(url_for("auth.login"))
    
    return render_template("register.html", form=form)

# Login route
@auth_bp.route('/login', methods=["GET", "POST"])
def login():

    # if request.method == "POST":
    #     email = request.form.get('email')
    #     password = request.form.get('password')

    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        email_existing = User.query.filter_by(email=email).first()
        if email_existing and check_password_hash(email_existing.password, password):
            session['user_id'] = email_existing.id
            session['user'] = email_existing.username
            flash("Login Successful!", 'Success')
            return redirect(url_for("main.home"))
        
        else:
            flash("Invalid Credentials! please try again", 'Danger')
            return redirect(url_for("auth.login"))
        
    return render_template("login.html", form=form)

# Logout route
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logges Out", 'Info')
    return redirect(url_for("auth.login"))