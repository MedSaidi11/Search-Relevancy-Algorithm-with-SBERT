import annoy
from src import utils
from src.config import settings

logger = utils.logger

class AnnoyIndexer:
    def __init__(self):
        self.index = None

    def build(self, embs_obj:dict, index_path:str):
        assert isinstance(embs_obj, dict)
        assert isinstance(index_path, str)
        indices = list(embs_obj.keys())
        embeddings = list(embs_obj.values())
        
        assert len(embeddings[0])==settings.GET_ANNOY_SIZE, f"Embedding size {len(embeddings[0])} does not match ANNOY_SIZE {settings.GET_ANNOY_SIZE}"
        
        self.index = annoy.AnnoyIndex(settings.GET_ANNOY_SIZE, settings.ANNOY_METRIC)
        for i, embedding in zip(indices, embeddings):
            self.index.add_item(int(i), embedding)
        self.index.build(settings.ANNOY_N_TREES)
        self.save(index_path)

    def search(self, query_embeddings:list, k:int, ids_lookup:dict=None)->list:
        assert isinstance(query_embeddings, list)
        assert isinstance(k, int)
        assert isinstance(ids_lookup, dict) or ids_lookup is None
        results = []
        for query in query_embeddings:
            result = self.index.get_nns_by_vector(query, k, include_distances=True)
            ids = list(map(lambda x: ids_lookup[str(x)], result[0]))
            if settings.ANNOY_METRIC == "angular":
                res = sorted(set(zip(ids, result[1])), key=lambda x: x[1], reverse=True)
            elif settings.ANNOY_METRIC == "euclidean":
                res = sorted(set(zip(ids, result[1])), key=lambda x: x[1], reverse=False)
            else:
                raise ValueError(f"Unknown metric: {settings.ANNOY_METRIC}")
            results.append(res)
        return results

    def save(self, index_path:str):
        assert isinstance(index_path, str)
        self.index.save(index_path)

    def load(self, index_path:str):
        assert isinstance(index_path, str)
        self.index = annoy.AnnoyIndex(settings.GET_ANNOY_SIZE, settings.ANNOY_METRIC)
        self.index.load(index_path)

def init_index(index_type:str)->object:
    assert isinstance(index_type, str)
    assert index_type in ["annoy"]
    return AnnoyIndexer()