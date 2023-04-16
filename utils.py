import requests
import re
from elasticsearch_dsl import Search
import csv


def get_id(imdb_url):
    matched = re.findall("/title/(.*)/", imdb_url)
    if len(matched) >= 1:
        return matched[0]
    return ""


def parse_and_fetch(imdb_url, api_key):
    id = get_id(imdb_url)
    if id:
        params = {
            "apikey": api_key,
            "i": id
        }
        resp = requests.get("http://www.omdbapi.com/", params)
        if resp.status_code != 200:
            raise Exception(f"Failed to fetch movie info {resp.text}")
        return resp
    else:
        return None


def get_imdb_poster(imdb_url, api_key):
    try:
        resp = parse_and_fetch(imdb_url, api_key)
        poster_url = resp.json()["Poster"]
        return poster_url
    except Exception as ex:
        print(ex)
        return ""


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


def insert_movies(es, filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = {
                "imdb_id": get_id(row["movie_imdb_link"]),
                "title": row["movie_title"],
                "actors": ",".join([row["actor_1_name"], row["actor_2_name"], row["actor_3_name"]]),
                "genres": row["genres"],
                "release_year": row["title_year"],
                "imdb_url": row["movie_imdb_link"]
            }
            es.index(index="movies", body=movie)
