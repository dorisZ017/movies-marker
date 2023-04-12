import requests

API_KEY = "dcfd9cf8"

def get_resp(title, year = None):
    params = {
        "apikey": API_KEY,
        "t": title
    }
    if year:
        params["y"] = year

    resp = requests.get("http://www.omdbapi.com/", params)
    return resp

def get_url(resp):
    id = resp.json()["imdbID"]
    return "https://www.imdb.com/title/{}/".format(id)

def get_imdb_url(title, year = None):
    resp = get_resp(title, year)
    return get_url(resp)

