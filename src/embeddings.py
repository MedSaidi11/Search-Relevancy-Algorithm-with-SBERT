from sentence_transformers import SentenceTransformer
from src.config import settings
from src import utils

logger = utils.logger

model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL_TYPE)

def get_embeddings_from_lemmatized_sentences(sentences:list, batch_size:int=32)->list:
    assert isinstance(sentences, list)
    assert isinstance(batch_size, int)
    embeddings = model.encode(sentences, show_progress_bar=False, device="cpu", batch_size=batch_size)
    return embeddings.tolist()
