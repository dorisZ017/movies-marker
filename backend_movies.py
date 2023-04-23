import elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS
import movies_utils
import op_utils
import yaml

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

with open("config.yml") as f:
    config = yaml.safe_load(f)
    API_KEY = config["API_KEY"]
    host = config["ES_HOST"]

es = elasticsearch.Elasticsearch([host], timout=30)

op_utils.setup()


@app.route("/search", methods=["GET"])
def search():
    title = request.args.get("title")
    actor = request.args.get("actor")
    genre = request.args.get("genre")
    year = request.args.get("year")

    resp = movies_utils.search_movies(es, title, actor, genre, year)
    movies = movies_utils.parse_movie_list(resp, API_KEY)

    return jsonify(movies)


@app.route("/add_operation", methods=["POST"])
def add_movie_operation():
    params = request.json["params"]
    op_utils.insert_operation(params)

    return jsonify({"status": "success"})


@app.route("/get_movies", methods=["GET"])
def get_movies_by_operation():
    operation = request.args.get("operation")
    data = op_utils.get_movies(operation)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
