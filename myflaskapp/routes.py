from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .extensions import db

# Define a blueprint for routes
main = Blueprint('main', __name__)

# Home page route
@main.route('/')
def index():
    # If the user is logged in, redirect to the dashboard
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

# Registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please try a different one.', 'danger')
            return redirect(url_for('main.register'))
        
        # Hash the password for security
        hashed_password = generate_password_hash(password, method='sha256')
        
        # Create and add the new user
        new_user = User(name=name, username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        # Log the user in automatically after registration
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        
        # Redirect to the success page
        flash('Registration successful!', 'success')
        return redirect(url_for('main.success'))
    
    return render_template('register.html')

@main.route('/success')
def success():
    return render_template('success.html')

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Authenticate user
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('main.login'))
    
    return render_template('login.html')

# Dashboard route
@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('main.login'))
    
    username = session.get('username')
    return render_template('dashboard.html', username=username)

# Logout route
@main.route('/logout')
def logout():
    session.clear()  # Clear session to log out the user
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))