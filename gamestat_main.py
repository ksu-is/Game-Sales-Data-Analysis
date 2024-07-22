from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'

db = SQLAlchemy(app)

class Games(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return '<Game %r>' % self.id
    
def import_excel_data(file_path):
    data = pd.read_excel(file_path)
    for _, row in data.iterrows():
        game = Games(name=row['title'])  
        db.session.add(game)
    db.session.commit()

@app.route('/')
def index():
    return render_template('GameStat.html')

@app.route('/Games')
def games():
    page = request.args.get('page', 1, type=int)
    per_page = 100
    games_list = Games.query.paginate(page = page, per_page = per_page, error_out = False)
    return render_template('Games.html', games=games_list)

@app.route('/action')
def action():
    return render_template('Action.html')

@app.route('/adventure')
def adventure():
    return render_template('Adventure.html')

@app.route('/role-playing')
def role_playing():
    return render_template('Role-Playing.html')

@app.route('/sports')
def sports():
    return render_template('Sports.html')

@app.route('/misc')
def misc():
    return render_template('Misc.html')

@app.route('/about')
def about():
    return render_template('About.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        import_excel_data('c:/Users/leben/OneDrive/Documents/GitHub/Game-Sales-Data-Analysis/vgchartz-2024.xlsx')
        print("Database tables created.")
    app.run(debug = True)

