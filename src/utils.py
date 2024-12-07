import pandas as pd
import numpy as np
import os
import re
import json
import logging

import datetime

from src.config import settings
from src.database.db_client import Client
from src.database.db_engine import db_engine
from src.database.models import *

if settings.ENV=="dev":
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
        filename=f"{settings.LOGS_DIR}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.log", 
        filemode='w'
    )
logger = logging.getLogger(__name__)

os.makedirs(os.path.join(settings.DATA_DIR, "raw"), exist_ok=True)
os.makedirs(os.path.join(settings.DATA_DIR, "processed"), exist_ok=True)
os.makedirs(settings.LOGS_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)
os.makedirs(settings.RESULTS_DIR, exist_ok=True)

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def load_article_lookup()->dict:
    df = pd.read_csv("./data/raw/raw.csv")
    df = df[["article_id", "title", "text", "category", "subcategory"]]
    df.index = df.article_id
    df = df[["title", "text", "category", "subcategory"]].drop_duplicates()
    return df.to_dict(orient="index")

def get_raw_data_from_aws_postgres(output_filename=os.path.join(settings.DATA_DIR, "raw", "raw.csv"))->str:
    logger.info("Getting raw data from AWS PostgreSQL")
    client = Client(db_engine,"News")
    client.create_table(data_path="./data/raw/raw.csv")
    session=client.Session()
    session.connection(execution_options={"schema_translate_map": {None: client.meta.schema}})
    rows = session.query(NewsArticle).all()
    data = []
    for row in rows:
        data.append({"id":row.id,"article_id":row.article_id,"category":row.category,"subcategory":row.subcategory,"title":row.title,"published_date":row.published_date,"text":row.text,"source":row.source})
    data = pd.DataFrame(data)    
    data.to_csv(output_filename, index=False)
    return output_filename
