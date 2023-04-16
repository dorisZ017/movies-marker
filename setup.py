import elasticsearch
import yaml
import utils
import argparse

parser = argparse.ArgumentParser(description="Creating ElasticSearch instance and inserting data")
parser.add_argument("--overwrite", action=argparse.BooleanOptionalAction, default=False)
args = parser.parse_args()

with open("config.yml") as f:
    config = yaml.safe_load(f)
    es_host = config["ES_HOST"]
    data_file = config["MOVIE_DATA_PATH"]

es = elasticsearch.Elasticsearch(["es_host"], timout=30)

try:
    es.indices.create("movies")
    utils.insert_movies(es, data_file)
except elasticsearch.exceptions.RequestError as ex:
    if ex.error == 'resource_already_exists_exception':
        if args.overwrite:
            print("Overwriting existing movies database")
            es.indices.delete("movies")
            es.indices.create("movies")
            utils.insert_movies(es, data_file)
    else:
        raise ex

print("Setup completed")
