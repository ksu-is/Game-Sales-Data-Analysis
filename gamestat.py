from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'GameStat Home'

@app.route('/Games/')
def games():
    return 'Games'

if __name__ == '__main__':
    app.run(debug = True)


