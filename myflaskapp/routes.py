from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import User
from .extensions import db

# Define a blueprint for routes
main = Blueprint('main', __name__)

# Home page route
@main.route('/')
def index():
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
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please try a different one.')
            return redirect(url_for('main.register'))
        
        # Create and add the new user
        new_user = User(name=name, username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        # Redirect to dashboard after registration
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        return redirect(url_for('main.dashboard'))
    
    return render_template('register.html')

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Authenticate user
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('main.login'))
    
    return render_template('login.html')

# Dashboard route
@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('main.login'))
    
    username = session.get('username')
    return render_template('dashboard.html', username=username)

# Logout route
@main.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.login'))