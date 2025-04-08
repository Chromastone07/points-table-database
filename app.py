# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ipl.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Database Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), nullable=False)
    logo_url = db.Column(db.String(200), nullable=False)
    matches_played = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    nrr = db.Column(db.Float, default=0.0)
    points = db.Column(db.Integer, default=0)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form.get('is_admin') == 'True'  # Convert string to boolean
        
        # Check if the username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Create a new user
        new_user = User(username=username, password=hashed_password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return redirect(url_for('admin_redirect'))
            return redirect(url_for('index'))
        flash('Invalid username or password', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin_redirect')
@login_required
def admin_redirect():
    if current_user.is_admin:
        return render_template('admin_redirect.html')  # Gives options to go to dashboard or index
    return redirect(url_for('index'))


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    teams = Team.query.all()
    return render_template('admin_dashboard.html', teams=teams)

@app.route('/add-team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        team_name = request.form['team_name']
        logo_url = request.form['logo_url']
        new_team = Team(team_name=team_name, logo_url=logo_url)
        db.session.add(new_team)
        db.session.commit()
        flash('Team added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))  # Redirect to index page to display the team
    return render_template('add_team.html')



@app.route('/edit-team/<int:team_id>', methods=['GET', 'POST'])
@login_required
def edit_team(team_id):
    if not current_user.is_admin:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))

    team = Team.query.get_or_404(team_id)

    if request.method == 'POST':
        # Update team stats from the form
        team.matches_played = request.form['matches_played']
        team.wins = request.form['wins']
        team.losses = request.form['losses']
        team.nrr = request.form['nrr']
        team.points = request.form['points']

        db.session.commit()
        flash(f'Stats for {team.team_name} have been updated!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_team.html', team=team)


@app.route('/remove-team/<int:team_id>', methods=['GET'])
@login_required
def remove_team(team_id):
    if not current_user.is_admin:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    team = Team.query.get_or_404(team_id)
    
    # Delete the team from the database
    db.session.delete(team)
    db.session.commit()
    
    flash(f'{team.team_name} has been removed!', 'success')
    return redirect(url_for('admin_dashboard'))



@app.route('/remove-stats/<int:team_id>', methods=['GET'])
@login_required
def remove_stats(team_id):
    if not current_user.is_admin:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('index'))
    
    team = Team.query.get_or_404(team_id)
    
    # Reset team stats to zero
    team.matches_played = 0
    team.wins = 0
    team.losses = 0
    team.nrr = 0.0
    team.points = 0
    
    db.session.commit()
    flash(f'Stats for {team.team_name} have been reset!', 'success')
    return redirect(url_for('admin_dashboard'))





@app.route('/index')
def index():
    teams = Team.query.all()
    return render_template('index.html', teams=teams)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
