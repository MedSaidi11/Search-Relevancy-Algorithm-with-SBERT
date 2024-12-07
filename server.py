from fastapi import FastAPI
from pydantic import BaseModel
import datetime
import os
from src import utils
from src.config import settings
from src import build_index
from src import search
from src import preprocessor
from src import embeddings
import pandas as pd
logger = utils.logger

def build():
    logger.info("Executing the pipeline...")
    if not settings.REUSE_PREPROCESSED_DATA:
        assert os.path.exists(os.path.join(settings.DATA_DIR, "processed", f"{settings.TEXT_SECTION_TYPE}_{'_'.join(settings.TRAIN_DATA_INPUT_TYPES)}_processed.csv")), f'Preprocessed data not found! Please set REUSE_PREPROCESSED_DATA to False in config.py and run the pipeline again.'
        logger.info("Reusing processed data...")
        r = dict()
        r["path_to_processed_text"] = os.path.join(settings.DATA_DIR, "processed", f"{settings.TEXT_SECTION_TYPE}_{'_'.join(settings.TRAIN_DATA_INPUT_TYPES)}_processed.csv")
        r["path_to_article_ids"] = os.path.join(settings.MODELS_DIR, f"{settings.TEXT_SECTION_TYPE}_" + "_".join(settings.TRAIN_DATA_INPUT_TYPES) + "_ids.json")
    else:
        logger.info("Collecting and preprocessing data ...")
        output_filename = utils.get_raw_data_from_aws_postgres()
        r = preprocessor.preprocess_data(output_filename, section_by=settings.TEXT_SECTION_TYPE, input_types=settings.TRAIN_DATA_INPUT_TYPES, sample_size=settings.SAMPLE_SIZE)
    pdf = pd.read_csv(r["path_to_processed_text"])
    logger.info("Building title index ...")
    if not settings.REUSE_PREGENERATED_EMBEDDINGS:
        data = dict(zip(pdf["section_id"].values.tolist(),embeddings.get_embeddings_from_lemmatized_sentences(pdf["text"].values.tolist())))
        utils.save_json(data, os.path.join(settings.DATA_DIR, "processed", f"{settings.TEXT_SECTION_TYPE}_" + "_".join(settings.TRAIN_DATA_INPUT_TYPES) + "_embeddings.json"))
    else:
        assert os.path.exists(os.path.join(settings.DATA_DIR, "processed", f"{settings.TEXT_SECTION_TYPE}_" + "_".join(settings.TRAIN_DATA_INPUT_TYPES) + "_embeddings.json")), "Embeddings not found. Please set REUSE_PREGENERATED_EMBEDDINGS to False in config.py and run the pipeline again."
    _embeddings = utils.load_json(os.path.join(settings.DATA_DIR, "processed", f"{settings.TEXT_SECTION_TYPE}_" + "_".join(settings.TRAIN_DATA_INPUT_TYPES) + "_embeddings.json"))
    index = build_index.init_index(index_type=settings.SEARCH_INDEX_TYPE)
    index.build(_embeddings, os.path.join(settings.MODELS_DIR, settings.SEARCH_INDEX_TYPE))
    logger.info("Pipeline completed successfully!")
    index.load(os.path.join(settings.MODELS_DIR, settings.SEARCH_INDEX_TYPE))
    ids_mapper = utils.load_json(os.path.join(settings.MODELS_DIR, f"{settings.TEXT_SECTION_TYPE}_{'_'.join(settings.TRAIN_DATA_INPUT_TYPES)}_ids.json"))
    sections_stats = utils.load_json(os.path.join(settings.MODELS_DIR, f"{settings.TEXT_SECTION_TYPE}_{'_'.join(settings.TRAIN_DATA_INPUT_TYPES)}_stats.json"))["sections_by_article"]
    return index, ids_mapper, sections_stats

class SearchRequest(BaseModel):
    query: list[str] 
    k: int 

app = FastAPI()

index, ids_mapper, sections_stats = build()

@app.get('/ping')
def health():
    return({"status": "ok", "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

@app.post('/search')
def search_relevant_articles(request: SearchRequest):
    try:
        query = request.query
        k = request.k
        results = search.search(index, query, k, ids_mapper, sections_stats)
        return {"message":"success", "data":results}
    except Exception as e:
        return {"message":"failed", "error":str(e)}
    

