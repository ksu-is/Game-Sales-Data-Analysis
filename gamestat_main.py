import sys
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db' # Configure the database URI for SQLite
db = SQLAlchemy(app) # Initialize the SQLAlchemy extension

# Define the Games model to represent game records in the database
class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    console = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    critic_score = db.Column(db.Float, nullable=True)
    total_sales = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String(100), nullable=True)
    
    # String representation of the Games model
    def __repr__(self):
        return '<Game %r>' % self.id

# Function to import data from an Excel file into the database
def import_excel_data(file_path):
    data = pd.read_excel(file_path)
    for _, row in data.iterrows():
        title = row['title']
        console = row['console']
        genre = row['genre']
        critic_score = row['critic_score'] if not pd.isna(row['critic_score']) else None
        total_sales = row['total_sales'] if not pd.isna(row['total_sales']) else 0.0
        release_date = row.get('release_date')
        if pd.isna(release_date):
            release_date = None
        else:
            release_date = release_date.strftime('%Y-%m-%d')  

        game = Games(
            title=title,
            console=console,
            genre=genre,
            critic_score=critic_score,
            total_sales=total_sales,
            release_date=release_date
        )
        db.session.add(game) # Add the game record to the session
    db.session.commit() # Commit the session to save changes to the database

# Route for the homepage
@app.route('/')
def index():
    return render_template('GameStat.html')

# Route to display all games with pagination
@app.route('/Games')
def games():
    page = request.args.get('page', 1, type=int)
    per_page = 100
    games_list = Games.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('Games.html', games=games_list)

# Route to display Action genre games with pagination
@app.route('/action')
def action():
    page = request.args.get('page', 1, type=int)
    per_page = 100
    action_games_query = Games.query.filter_by(genre='Action')
    action_games = action_games_query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('Action.html', games=action_games)

# Route to display Adventure genre games with pagination
@app.route('/adventure')
def adventure():
    page = request.args.get('page', 1, type=int)
    per_page = 100
    adventure_games_query = Games.query.filter_by(genre='Adventure')
    adventure_games = adventure_games_query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('Adventure.html', games=adventure_games)

# Route to display Role-Playing genre games with pagination
@app.route('/role-playing')
def role_playing():
    page = request.args.get('page', 1, type=int)
    per_page = 100
    roleplaying_games_query = Games.query.filter_by(genre='Role-Playing')
    roleplaying_games = roleplaying_games_query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('Role-Playing.html', games=roleplaying_games)

# Route to display Sports genre games with pagination
@app.route('/sports')
def sports():
    page = request.args.get('page', 1, type=int)
    per_page = 100
    sports_games_query = Games.query.filter_by(genre='Sports')
    sports_games = sports_games_query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('Sports.html', games=sports_games)  # Corrected template name

# Route to display Misc genre games with pagination
@app.route('/misc')
def misc():
    page = request.args.get('page', 1, type=int)
    per_page = 100
    misc_games_query = Games.query.filter_by(genre='Misc')
    misc_games = misc_games_query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('Misc.html', games=misc_games)

# Route for search functionality with pagination
@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)
    per_page = 100
    if query:
        search_query = Games.query.filter(
            (Games.title.ilike(f'%{query}%')) |
            (Games.console.ilike(f'%{query}%')) |
            (Games.genre.ilike(f'%{query}%'))
        )
        search_results = search_query.paginate(page=page, per_page=per_page, error_out=False)
        return render_template('Search.html', games=search_results, query=query)
    else:
        return redirect(url_for('index'))

# Route to display the About page
@app.route('/about')
def about():
    return render_template('About.html')

# Main entry point of the application
if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = 'vgchartz-2024.xlsx'  

    with app.app_context():
        db.drop_all()
        db.create_all()
        
        import_excel_data(file_path)
        print("Database tables created and data imported.")
    app.run(debug=True)
