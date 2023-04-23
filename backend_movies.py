from datetime import datetime

import elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS
import utils
import yaml
import sqlite3
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

with open("config.yml") as f:
    config = yaml.safe_load(f)
    API_KEY = config["API_KEY"]
    host = config["ES_HOST"]

es = elasticsearch.Elasticsearch([host], timout=30)

DB_NAME = "movie_operations.db"
TABLE_NAME = "movie_operations"
conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist
c.execute(f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                title TEXT,
                release_year INTEGER,
                timestamp TEXT,
                operation TEXT,
                operation_input TEXT
            )""")
conn.commit()


@app.route("/search", methods=["GET"])
def search():
    title = request.args.get("title")
    actor = request.args.get("actor")
    genre = request.args.get("genre")
    year = request.args.get("year")

    resp = utils.search_movies(es, title, actor, genre, year)
    movies = utils.parse_movie_list(resp, API_KEY)

    return jsonify(movies)


@app.route("/add_operation", methods=["POST"])
def add_movie_operation():
    params = request.json["params"]
    title = params.get("title")
    release_year = params.get("release_year")
    operation = params.get("operation")
    operation_input = params.get("input")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"""INSERT INTO {TABLE_NAME} 
                (title, release_year, timestamp, operation, operation_input) 
                VALUES 
                (
                "{title}", {release_year}, "{timestamp}", "{operation}", "{operation_input}"
                )
                """
    print(query)
    c.execute(query)
    conn.commit()

    return jsonify({"status": "success"})


@app.route("/get_movies", methods=["GET"])
def get_movies_by_operation():
    operation = request.args.get("operation")
    query = f"""
      SELECT * FROM {TABLE_NAME} WHERE operation = "{operation}" ORDER BY timestamp DESC

     """
    print(query)
    c.execute(query)
    rows = c.fetchall()

    data = []
    for row in rows:
        res = {"title": row[0], "release_year": row[1], "activity_time": row[2]}
        if operation == "rate":
            res["detail"] = row[4]
        else:
            if operation == "review":
                res["detail"] = row[5]
            else:
                res["detail"] = "NA"
        data.append(res)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
