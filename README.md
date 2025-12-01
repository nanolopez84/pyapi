# Python Flask REST API example
#### _Simple Python/Flask REST API that connects to a dockerized MongoDB database_

## Prerequisites
- Install Docker
https://docs.docker.com/engine/install/
- Install Python
https://www.python.org/downloads/
- Setup Python Virtual Environment
```
python -m venv .venv
source .venv/bin/activate
cd api
pip install -r requirements.txt
```

## How to Run
### API
- In a terminal run the dockerized database
```
docker run --name mongo-instance -p 27017:27017 -d mongo
```
- Start the Python/Flask API service
```
python pyapi.py
```

- Try these endpoints with a REST client (cURL, Postman, etc)
_You may import the `pyapi.postman_collection.json` file into Postman_
_In Postman, set the {{base_url}} variable to http://127.0.0.1:5000/api/v1
```
POST    http://127.0.0.1:5000/api/v1/candidate {"name": "John", "age": 35}
GET     http://127.0.0.1:5000/api/v1/candidates
GET     http://127.0.0.1:5000/api/v1/candidate/<candidateId>
PATCH   http://127.0.0.1:5000/api/v1/candidate/<candidateId> {"_id": <candidateId>, "name": "Johnathan"}
DELETE  http://127.0.0.1:5000/api/v1/candidate/<candidateId>
```

### Run tests
- In a terminal run the dockerized database
```
docker run --name mongo-instance -p 27017:27017 -d mongo
```
- Start the API
```
python pyapi.py testdb
```
- Open another terminal and execute the tests
```
cd api
python -m unittest discover -v
```
