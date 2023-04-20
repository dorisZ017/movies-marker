import elasticsearch
from flask import Flask, request, jsonify
from flask_cors import CORS
import utils
import yaml

with open("config.yml") as f:
    config = yaml.safe_load(f)
    API_KEY = config["API_KEY"]
    host = config["ES_HOST"]

es = elasticsearch.Elasticsearch([host], timout=30)

app = Flask(__name__)
CORS(app)


@app.route("/search", methods=["GET"])
def search():
    title = request.args.get("title")
    actor = request.args.get("actor")
    genre = request.args.get("genre")
    year = request.args.get("year")

    resp = utils.search_movies(es, title, actor, genre, year)
    movies = utils.parse_movie_list(resp, API_KEY)

    return jsonify(movies)


if __name__ == "__main__":
    app.run(debug=True)
