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


def search_movies(title=None, actor=None, genre=None, year=None):
    search = utils.build_search(title, actor, genre, year)
    res = search.using(es).index("movies").execute()
    return res


@app.route("/search", methods=["GET"])
def search():
    title = request.args.get("title")
    actor = request.args.get("actor")
    genre = request.args.get("genre")
    year = request.args.get("year")

    res = search_movies(title, actor, genre, year)
    try:
        movies = res.hits.hits
    except Exception:
        return jsonify([])

    for movie in movies:
        try:
            poster_url = utils.get_imdb_poster(movie["_source"].imdb_url, API_KEY)
            movie["_source"]["poster_url"] = poster_url
        except Exception:
            movie["_source"]["poster_url"] = ""

    return jsonify(movies)


if __name__ == "__main__":
    app.run(debug=True)
