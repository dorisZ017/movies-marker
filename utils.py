import requests
import re
from elasticsearch_dsl import Search
import csv


# Gets the imdb id from imdb url
def get_id(imdb_url):
    matched = re.findall("/title/(.*)/", imdb_url)
    if len(matched) >= 1:
        return matched[0]
    return ""


# Fetch movie info from OMDB api using the idmb url and api key
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


# Gets the URI to the poster picture of the given imdb url and api key
def get_imdb_poster(imdb_url, api_key):
    try:
        resp = parse_and_fetch(imdb_url, api_key)
        poster_url = resp.json()["Poster"]
        return poster_url
    except Exception as ex:
        print(ex)
        return ""


# Builds a search query with parameters
def build_search(title=None, actor=None, genre=None, year=None):
    s = Search()
    if title:
        s = s.query("match_phrase", title=title)
    if actor:
        s = s.query("match_phrase", actors=actor)
    if genre:
        s = s.query("wildcard", genres=f"*{genre}*")
    if year:
        s = s.query("match", year=year)
    print(s.to_dict())
    return s


# Inserts movies data from the file to the ElasticSearch instance
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


# Given search parameters, search movies from Elastic Search instance
def search_movies(es, title=None, actor=None, genre=None, year=None):
    s = build_search(title, actor, genre, year)
    res = s.using(es).index("movies").execute()
    return res


# Given the ElasticSearch response, gets the movie poster URI
# also converts the response to be serializable
def parse_movie_list(resp, api_key):
    try:
        movies = [x.to_dict() for x in resp.hits.hits]
    except Exception as ex:
        print(ex)
        return []
    for movie in movies:
        try:
            poster_url = get_imdb_poster(movie["_source"]["imdb_url"], api_key)
            movie["_source"]["poster_url"] = poster_url
        except Exception as ex:
            print(ex)
            movie["_source"]["poster_url"] = ""
    return movies
