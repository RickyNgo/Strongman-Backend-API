from bs4 import BeautifulSoup
from configparser import ConfigParser
import requests
import re
from pymongo import MongoClient, UpdateOne
import logging

config = ConfigParser()
config.read('config.ini')
logging.basicConfig(format="%(asctime)s - %(message)s", filename="scrape_log.txt",
                    encoding='utf-8', level=config['LOGGING']['LEVEL'])

client = MongoClient(config['MONGODB']['URL'])
db = client.strongman
athletes = db.athletes
contests = db.contests
results = db.results
records = db.records


def get_athletes():
    page = requests.get(config['URLS']['athletes'])
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('tr')
    rows.pop(0)
    res = []
    id_pattern = r"(\d+)"
    for row in rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[1].find('a').get('href')).group(0)
        res.append({
            "athlete_id": id,
            "first_name": cells[1]['data-sort'],
            "last_name": cells[2]['data-sort'],
            "country": cells[3].text,
            "active": cells[4].text,
            "intl_contests": cells[5].text,
            "intl_wins": cells[6].text,
            "wsms": cells[7].text,
            "wsm_finals": cells[8].text,
            "wsm_wins": cells[9].text
        })

    logging.info(f"{len(res)} athlete documents scraped...")
    upserts = [UpdateOne({"athlete_id": x["athlete_id"]}, {"$set": x},
                         upsert=True) for x in res]

    logging.info("Beginning athlete upsert operation...")
    response = athletes.bulk_write(upserts)
    logging.info(
        f"Matched: {response.matched_count}, Upserted: {response.upserted_count}")


def get_contests():
    page = requests.get(config['URLS']['contests'])
    soup = BeautifulSoup(page.content, 'html5lib')
    international_rows = soup.find(id='WSMTable1').find_all('tr')
    national_rows = soup.find(id='WSMTable2').find_all('tr')
    single_event_rows = soup.find(id='WSMTable3').find_all('tr')
    international_rows.pop(0)
    national_rows.pop(0)
    single_event_rows.pop(0)
    res = []
    id_pattern = r"(\d+)"

    for row in international_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[1].find('a').get('href')).group(0)
        res.append({
            "contest_id": id,
            "name": cells[1].text.lstrip(),
            "number": cells[2].text,
            "most_recent": cells[3].text,
            "type": "International"
        })
    for row in national_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[1].find('a').get('href')).group(0)
        res.append({
            "contest_id": id,
            "name": cells[1].text.lstrip(),
            "number": cells[2].text,
            "most_recent": cells[3].text,
            "type": "National"
        })

    for row in single_event_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[1].find('a').get('href')).group(0)
        res.append({
            "contest_id": id,
            "name": cells[1].text.lstrip(),
            "number": cells[2].text,
            "most_recent": cells[3].text,
            "type": "Single Event"
        })

    logging.info(f"{len(res)} contest documents scraped...")
    upserts = [UpdateOne({"contest_id": x["contest_id"]}, {"$set": x},
                         upsert=True) for x in res]
    logging.info("Beginning contest upsert operation...")
    response = contests.bulk_write(upserts)
    logging.info(
        f"Matched: {response.matched_count}, Upserted: {response.upserted_count}")


def get_records():
    page = requests.get(config['URLS']['records'])
    soup = BeautifulSoup(page.content, 'html5lib')
    wsm_rows = soup.find(id='WSMRecordList').find_all('tr')
    event_rows = soup.find(id='StaticRecordList').find_all('tr')
    wsm_rows.pop(0)
    wsm_rows.pop(0)
    event_rows.pop(0)
    event_rows.pop(0)

    res = []
    id_pattern = r"(\d+)"

    for row in wsm_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[0].find('a').get('href')).group(0)
        res.append({
            "record_id": id,
            "record": cells[0].text,
            "athlete": cells[1].text,
            "country": cells[2].text,
            "value": cells[3].text,
            "contests": cells[4].text,
            "type": 'WSM'
        })

    for row in event_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[0].find('a').get('href')).group(0)
        res.append({
            "record_id": id,
            "record": cells[0].text,
            "athlete": cells[1].text,
            "country": cells[2].text,
            "value": cells[3].text,
            "contests": cells[4].text,
            "type": 'WSM'
        })
    logging.info(f"{len(res)} record documents scraped...")
    upserts = [UpdateOne({"record_id": x["record_id"]}, {"$set": x},
                         upsert=True) for x in res]
    logging.info("Beginning record upsert operation...")
    response = records.bulk_write(upserts)
    logging.info(
        f"Matched: {response.matched_count}, Upserted: {response.upserted_count}")


def get_results():
    page = requests.get(config['URLS']['results'])
    soup = BeautifulSoup(page.content, 'html5lib')
    international_rows = soup.find(id='WSMTable1').find_all('tr')
    national_rows = soup.find(id='WSMTable2').find_all('tr')
    single_event_rows = soup.find(id='WSMTable3').find_all('tr')
    international_rows.pop(0)
    national_rows.pop(0)
    single_event_rows.pop(0)
    res = []
    id_pattern = r"(\d+)"

    for row in international_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[1].find('a').get('href')).group(0)
        res.append({
            "result_id": id,
            "date": cells[0].text,
            "contest": cells[1].text,
            "contest_type": cells[2].text,
            "location": cells[3].text,
            "champion": cells[4].text,
            "type": 'International'
        })

    for row in national_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[1].find('a').get('href')).group(0)
        res.append({
            "result_id": id,
            "date": cells[0].text,
            "contest": cells[1].text,
            "contest_type": cells[2].text,
            "location": cells[3].text,
            "champion": cells[4].text,
            "type": 'National'
        })

    for row in single_event_rows:
        cells = row.find_all('td')
        id = re.search(id_pattern, cells[1].find('a').get('href')).group(0)
        res.append({
            "result_id": id,
            "date": cells[0].text,
            "contest": cells[1].text,
            "contest_type": cells[2].text,
            "location": cells[3].text,
            "champion": cells[4].text,
            "type": 'Single Event'
        })
    logging.info(f"{len(res)} result documents scraped...")
    upserts = [UpdateOne({"result_id": x["result_id"]}, {"$set": x},
                         upsert=True) for x in res]
    logging.info("Beginning result upsert operation...")
    response = results.bulk_write(upserts)
    logging.info(
        f"Matched: {response.matched_count}, Upserted: {response.upserted_count}")


if __name__ == '__main__':
    get_athletes()
    get_results()
    get_records()
    get_contests()
