# movies-marker
## Setup
### Requirements:
* Python 3.9 or later
* Install Node.js and npm
* Docker
### Setup Data
Start ElasticSearch locally:
```
docker pull elasticsearch:7.10.1
docker run -d -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.10.1
```
Download data from https://www.kaggle.com/datasets/carolzhangdc/imdb-5000-movie-dataset, put its path to `config.yaml`, then run the setup script to insert data to ElasticSearch:
```
python setup.py
```
## Backend
Implementation of backend Flask server: `backend_movies.py`

Some helping functions: `utils.py`

Unit tests: `movies_test.py`

Run `pip install <package name>` as needed`

## Frontend
TODO

## Start the application:
```
cd movies-frontend
npm start
```
