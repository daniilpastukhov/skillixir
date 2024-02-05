import os
from dotenv import load_dotenv

from pymongo import MongoClient

from pkg import Scraper, construct_query


load_dotenv()


mongo_client = MongoClient(os.environ['MONGO_URI'])
db = mongo_client['linkedin']
collection = db['jobs']

def on_data(data):
    collection.insert_one(data._asdict())

scraper = Scraper(on_data_callback=on_data)
query = construct_query(search_query='Machine Learning Engineer', locations=['Europe'], limit=5)
scraper.run(query)
