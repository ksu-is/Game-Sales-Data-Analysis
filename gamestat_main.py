from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('GameStat.html')

@app.route('/Games')
def games():
    return render_template('Games.html')

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
    app.run(debug = True)

