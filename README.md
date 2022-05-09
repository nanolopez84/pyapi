# Python Flask REST API example
#### _Simple Python/Flask REST API that connects to a dockerized MongoDB database_

## Prerequisites
- Install Docker
https://docs.docker.com/engine/install/
- Install Python3
https://www.python.org/downloads/
- Install Python dependencies
```
cd api
pip3 install -r requirements.txt
```

## How to Run
### API
- In a terminal run the dockerized database
```
docker run --name mongo-instance -p 27017:27017 -d mongo
```
- Start the Python/Flask API service
```
python3 pyapi.py
```

- Try these endpoints with a REST client (cURL, Postman, etc)
_You may import the `pyapi.postman_collection.json` file into Postman_
_In Postman, set the {{base_url}} variable to http://127.0.0.1:5000/api/v1_
```
POST    http://127.0.0.1:5000/api/v1/candidate {"name": "John"}
GET     http://127.0.0.1:5000/api/v1/candidates
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
python3 pyapi.py
```
- Open another terminal and execute the tests
```
cd api
python3 -m unittest discover -v
```

