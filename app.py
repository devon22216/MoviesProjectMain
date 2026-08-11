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
        # Filter movies where title contains search term
        movies = conn.execute("SELECT * FROM Movie WHERE Title LIKE ? LIMIT 50;", (f"%{query}%",)).fetchall()
    else:
        # Default display of top 20 movies
        movies = conn.execute("SELECT * FROM Movie LIMIT 20;").fetchall()
        
    conn.close()
    return render_template("index.html", movies=movies, query=query)

if __name__ == "__main__":
    app.run(debug=True)