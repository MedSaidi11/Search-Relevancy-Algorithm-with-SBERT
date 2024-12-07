from src import utils
from src import preprocessor
from src import embeddings
from src.config import settings
import numpy as np

logger = utils.logger

lookup = utils.load_article_lookup()

def index_to_content(index:int, input_data_type=settings.TRAIN_DATA_INPUT_TYPES)->str:
    assert isinstance(index, int), f"index: {index} {type(index)}"
    assert isinstance(input_data_type, list)
    assert isinstance(input_data_type[0], str)
    embs1 = []
    embs2 = []
    if input_data_type==["title"]:
        title = lookup[index]["title"]
        return embeddings.get_embeddings_from_lemmatized_sentences([preprocessor.preprocess_text(title)])
    elif input_data_type==["text"]:
        text = lookup[index]["text"]
        return embeddings.get_embeddings_from_lemmatized_sentences([preprocessor.preprocess_text(text)])
    else:
        assert "title" in input_data_type
        assert "text" in input_data_type
        title = lookup[index]["title"]
        text = lookup[index]["text"]
        embs1 = embeddings.get_embeddings_from_lemmatized_sentences([preprocessor.preprocess_text(title)])
        embs2 = embeddings.get_embeddings_from_lemmatized_sentences([preprocessor.preprocess_text(text)])
        return embs1 + embs2

def compute_relevance_score(v1:np.ndarray, v2:np.ndarray)->float:
    assert isinstance(v1, np.ndarray)
    assert isinstance(v2, np.ndarray)
    assert v1.shape == v2.shape, f"v1.shape: {v1.shape}, v2.shape: {v2.shape}"
    assert v1.shape[0] > 0
    return round(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)), settings.RELEVANCE_SCORE_ROUNDING)
    

def search(index, queries:list, k:int, ids_mapper:dict, sections_stats:dict)->list:
    assert isinstance(queries, list)
    assert isinstance(queries[0], str)
    assert isinstance(k, int)
    assert k > 0

    logger.info(f"Searching index for {len(queries)} queries...")

    _k = max(k, int(sections_stats["mean"] + sections_stats["std"])*k)
    _queries = list(map(lambda x: preprocessor.preprocess_text(x), queries))
    embs = embeddings.get_embeddings_from_lemmatized_sentences(_queries)
    _results = index.search(embs, _k, ids_mapper["section_id_to_article_id"])
    
    results = []
    for i in range(len(_results)):
        logger.info("Proceesing query:" + queries[i])
        result = {
            "query": queries[i]
        }
        result["results"] = []
        skip = set()
        for j in range(len(_results[i])):
            if len(result["results"])>=k:
                break
            article_id = _results[i][j][0]
            if article_id in skip:
                logger.info(f"Duplicate result - Skipping: {article_id}")
                continue
            res_emb = index_to_content(article_id, settings.TRAIN_DATA_INPUT_TYPES)[0]
            relevance_score = compute_relevance_score(np.asarray(embs[i]).T, np.asarray(res_emb))
            if relevance_score < settings.RELEVANCE_SCORE_THRESHOLD:
                logger.info(f"Relevance score below threshold - Skipping: {article_id}")
                continue
            result["results"].append({
                "article_id": article_id,
                "score": relevance_score,
                "title": lookup[int(article_id)]["title"],
                "category": lookup[int(article_id)]["category"],
                "subcategory": lookup[int(article_id)]["subcategory"]
            })
            skip.add(_results[i][j][0])
        results.append(result)
    
    logger.info(f"Search complete.")
    return results

    

