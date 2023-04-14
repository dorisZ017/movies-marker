import elasticsearch
from elasticsearch_dsl import Search
from flask import Flask, request, jsonify
from flask_cors import CORS
import utils

es = elasticsearch.Elasticsearch(["http://localhost:9200"], timout=30)

utils.es_setup(es, "")  # TODO filename

app = Flask(__name__)
CORS(app)


def build_search(title=None, actor=None, genre=None, year=None):
    s = Search()
    if title:
        s = s.query("wildcard", title=f"*{title}*")
    if actor:
        s = s.query("wildcard", actors=f"*{actor}*")
    if genre:
        s = s.query("wildcard", genre=f"*{genre}*")
    if year:
        s = s.query("match", year=year)
    return s


def search_movies(title=None, actor=None, genre=None, year=None):
    search = build_search(title, actor, genre, year)
    res = search.using(es).index("movies").execute()
    return res


@app.route("/search", methods=["GET"])
def search():
    title = request.args.get("title")
    actor = request.args.get("actor")
    genre = request.args.get("genre")
    year = request.args.get("year")

    movies = search_movies(title, actor, genre, year)

    return jsonify({
        "hits": {
            "hits": movies
        }
    })


if __name__ == "__main__":
    app.run(debug=True)
