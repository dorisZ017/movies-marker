
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def search_movies(search):
    es = Elasticsearch()
    res = search.using(es).index("movies").execute()
    return res

def build_search(title=None, actor=None, genre=None, year=None):
    s = Search()
    if title:
        s = s.query("match", title=title)
    if actor:
        s = s.query("wildcard", actors=f"*{actor}*")
    if genre:
        s = s.query("wildcard", genre=f"*{genre}*")
    if year:
        s = s.query("match", year=year)
    return s


def filter_movies(title=None, actor=None, genre=None, year=None):
    search = build_search(title, actor, genre, year)
    return search_movies(search)

