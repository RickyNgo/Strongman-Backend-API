from typing import List
from athletemodel import AthleteModel
from contestmodel import ContestModel
from resultmodel import ResultModel
from recordmodel import RecordModel
from fastapi import FastAPI
import uvicorn
from pymongo import MongoClient
from configparser import ConfigParser
import logging

app = FastAPI()
config = ConfigParser()
config.read('config.ini')
logging.basicConfig(format="%(asctime)s - %(message)s", filename="api_log.txt",
                    encoding='utf-8', level=config['LOGGING']['LEVEL'])
client = MongoClient(config['MONGODB']['URL'])

db = client.strongman
athletes = db.athletes
contests = db.contests
results = db.results
records = db.records


@app.get('/')
def index():
    return {'message': 'Welcome to this application',
            'num_athletes': athletes.count_documents({}),
            'num_contests': contests.count_documents({}),
            'num_results': results.count_documents({}),
            'num_records': records.count_documents({})}


@app.get('/athletes', response_model=List[AthleteModel])
def get_athletes():
    try:
        return [doc for doc in athletes.find({})]
    except Exception:
        logging.info("DB Operation error")
        return []


@app.get('/contests', response_model=List[ContestModel])
def get_contests():
    try:
        return [doc for doc in contests.find({})]
    except Exception:
        logging.info("DB Operation error")
        return []


@app.get('/results', response_model=List[ResultModel])
def get_results():
    try:
        return [doc for doc in results.find({})]
    except Exception:
        logging.info("DB Operation error")
        return []


@app.get('/records', response_model=List[RecordModel])
def get_records():
    try:
        return [doc for doc in records.find({})]
    except Exception:
        logging.info("DB Operation error")
        return []


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080,
                log_level="debug")
