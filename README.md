# movies-marker
## Overview
Allow the user to search movies by certain criteria, and save movies along with operations, including like, bookmark, rate and review. After saving, user can also view their activities by operations
<img width="1320" alt="Screen Shot 2023-04-23 at 10 46 46 AM" src="https://user-images.githubusercontent.com/31834512/233878230-710085cb-b200-465f-b182-e038ab055b55.png">

### Search:
<img width="1342" alt="Screen Shot 2023-04-23 at 6 19 13 PM" src="https://user-images.githubusercontent.com/31834512/233878308-030bd750-f107-4755-ac51-47f81dc90c37.png">

### Save movies with operations:
Add rating:

<img width="382" alt="Screen Shot 2023-04-23 at 6 20 22 PM" src="https://user-images.githubusercontent.com/31834512/233878438-d58cd184-0105-4baf-9584-1c85e2935d88.png">

View rated movies:

<img width="400" alt="Screen Shot 2023-04-23 at 6 21 25 PM" src="https://user-images.githubusercontent.com/31834512/233878494-da2e85dd-623b-4f55-91f1-55b39b04ee31.png">


## Setup
### Requirements:
* Python 3.9 or later
* Install Node.js and npm
* Docker

Run `pip install -r requirements.txt` to install required python packages
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

Detailed methods to be used in backend: 
`movies_utils.py`, `op_utils.py`


Unit tests: 
`movies_test.py`, `ops_tests.py`

## Frontend
`movies-frontend/src/MovieSearch.js` for UI and handeling user requests

## Start the application:
```
python backend_movies.py
cd movies-frontend
npm start
```
