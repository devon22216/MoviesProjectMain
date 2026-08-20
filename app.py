import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("MoviesProject.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    query = request.args.get("search", "")
    conn = connect_db()
    
    if query:
        movies = conn.execute("SELECT * FROM Movie WHERE Title LIKE ? LIMIT 50;", (f"%{query}%",)).fetchall()
    else:
        movies = conn.execute("SELECT * FROM Movie LIMIT 20;").fetchall()
        
    # SQL Aggregate queries for stats box
    stats = conn.execute("SELECT COUNT(*) as total, ROUND(AVG(Rating), 1) as avg_rating FROM Movie;").fetchone()
    
    conn.close()
    return render_template("index.html", movies=movies, query=query, stats=stats)

@app.route("/top-rated")
def top_rated():
    conn = connect_db()
    movies = conn.execute("SELECT * FROM Movie WHERE Rating >= 9.0 ORDER BY Rating DESC;").fetchall()
    
    # SQL Aggregate queries for stats box here too
    stats = conn.execute("SELECT COUNT(*) as total, ROUND(AVG(Rating), 1) as avg_rating FROM Movie;").fetchone()
    
    conn.close()
    return render_template("index.html", movies=movies, query="", stats=stats)

if __name__ == "__main__":
    app.run(debug=True)