from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    console = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    critic_score = db.Column(db.Float, nullable=True)
    total_sales = db.Column(db.Float, nullable=False)
    release_date = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<Game %r>' % self.id

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
        db.session.add(game)
    db.session.commit()

@app.route('/')
def index():
    return render_template('GameStat.html')

@app.route('/Games')
def games():
    page = request.args.get('page', 1, type = int)
    per_page = 100
    games_list = Games.query.paginate(page = page, per_page = per_page, error_out = False)
    return render_template('Games.html', games = games_list)

@app.route('/action')
def action():
    page = request.args.get('page', 1, type = int)
    per_page = 100
    action_games_query = Games.query.filter_by(genre = 'Action')
    action_games = action_games_query.paginate(page = page, per_page = per_page, error_out = False)
    return render_template('Action.html', games = action_games)

@app.route('/adventure')
def adventure():
    page = request.args.get('page', 1, type = int)
    per_page = 100
    adventure_games_query = Games.query.filter_by(genre = 'Adventure')
    adventure_games = adventure_games_query.paginate(page = page, per_page = per_page, error_out = False)
    return render_template('Adventure.html', games = adventure_games)

@app.route('/role-playing')
def role_playing():
    page = request.args.get('page', 1, type = int)
    per_page = 100
    roleplaying_games_query = Games.query.filter_by(genre = 'Role-Playing')
    roleplaying_games = roleplaying_games_query.paginate(page = page, per_page = per_page, error_out = False)
    return render_template('Role-Playing.html', games = roleplaying_games)

@app.route('/sports')
def sports():
    page = request.args.get('page', 1, type = int)
    per_page = 100
    sports_games_query = Games.query.filter_by(genre = 'Sports')
    sports_games = sports_games_query.paginate(page = page, per_page = per_page, error_out = False)
    return render_template('Role-Playing.html', games = sports_games)

@app.route('/misc')
def misc():
    page = request.args.get('page', 1, type = int)
    per_page = 100
    misc_games_query = Games.query.filter_by(genre = 'Misc')
    misc_games = misc_games_query.paginate(page = page, per_page = per_page, error_out = False)
    return render_template('Misc.html', games = misc_games)

@app.route('/about')
def about():
    return render_template('About.html')

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        import_excel_data('c:/Users/leben/OneDrive/Documents/GitHub/Game-Sales-Data-Analysis/vgchartz-2024.xlsx')
        print("Database tables created and data imported.")
    app.run(debug=True)