import os
from string import Template
import time

from dotenv import load_dotenv
from llama_cpp import Llama
from pymongo import MongoClient

load_dotenv()

CONTENT_TEMPLATE = Template('''
Postition: $title.
Company: $company.
Location: $location.
Description: $description.
''')

MAX_LENGTH = 4096

mongo_client = MongoClient(os.environ['MONGO_URI'])
db = mongo_client['linkedin']
source_collection = db['jobs']
target_collection = db['jobs_vectors']

llm = Llama(model_path='/workspaces/skillixir/models/llama-2-7b.Q4_K_M.gguf', embedding=True, n_ctx=MAX_LENGTH)

for doc in source_collection.find():
    start_time = time.time()
    content = CONTENT_TEMPLATE.substitute(
        title=doc['title'],
        company=doc['company'],
        location=doc['location'],
        description=doc['description']
    )[:MAX_LENGTH]
    doc['embedding'] = llm.create_embedding(doc['description'])
    if target_collection.find_one({'_id': doc['_id']}):
        target_collection.update_one({'_id': doc['_id']}, {'$set': doc})
    else:
        target_collection.insert_one(doc)
    print(f'Elapsed time: {time.time() - start_time} seconds')
