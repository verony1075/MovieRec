from flask import Flask, request, jsonify, render_template, g
from imdb import Cinemagoer
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'instance/app.db'

ia = Cinemagoer()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/search')
def search():
    query = request.args.get('query', '')
    if query:
        results = ia.search_movie(query)
        suggestions = []
        for result in results:
            movie = ia.get_movie(result.movieID)
            suggestions.append({
                'title': movie.get('title'),
                'year': movie.get('year'),
                'poster': movie.get('full-size cover url')
            })
        return jsonify(suggestions)
    return jsonify([])

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()  # Initialize the database if it doesn't exist
    app.run(debug=True)
