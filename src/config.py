from pydantic_settings import BaseSettings
from enum import Enum
from typing import Literal, Optional

class AppEnvironment(str,Enum):
    PROD = "prod"
    DEV = "dev"
    
class Settings(BaseSettings):
    ENV: Literal["prod","dev"] = "prod"
    DATA_DIR: str = "data"
    MODELS_DIR: str ="models"
    RESULTS_DIR: str ="results"
    LOGS_DIR: str ="logs"
    SAMPLE_SIZE: Optional[int] = None
    REUSE_PREPROCESSED_DATA: bool = False
    REUSE_PREGENERATED_EMBEDDINGS: bool = False
    DATABASE_USERNAME: str = "postgres"
    DATABASE_NAME: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_HOST: str = "54.196.62.32"
    DATABASE_PORT: str = "5432" 
    TEXT_SECTION_TYPE: Optional[Literal["sentence","paragraph"]] = None
    TRAIN_DATA_INPUT_TYPES: list = ["title"]
    TRAIN_DATA_INPUT_TYPES.sort(reverse=True)
    SEARCH_INDEX_TYPE: str = "annoy"
    ANNOY_N_TREES: int = 50
    ANNOY_METRIC: Literal["euclidean","manhattan","angular"] = "euclidean"
    SENTENCE_TRANSFORMER_MODEL_TYPE: str = "all-MiniLM-L6-v2"
    RELEVANCE_SCORE_ROUNDING: int = 2
    RELEVANCE_SCORE_THRESHOLD: float = 0.4
    
    @property
    def FORMAT_SEARCH_INDEX(self):
        search_index = f"{self.TEXT_SECTION_TYPE}_" + "_".join(self.TRAIN_DATA_INPUT_TYPES) + f".{self.SEARCH_INDEX_TYPE}"
        return search_index
    @property
    def FORMAT_DATABASE_URL(self):
        database_url = f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}"
        return database_url
    @property
    def GET_ANNOY_SIZE(self):
        if self.SENTENCE_TRANSFORMER_MODEL_TYPE == "all-MiniLM-L6-v2":
            annoy_size = 384
            return annoy_size
        elif self.SENTENCE_TRANSFORMER_MODEL_TYPE=="distilbert-base-nli-stsb-mean-tokens":
            annoy_size = 768
            return annoy_size
        elif self.SENTENCE_TRANSFORMER_MODEL_TYPE=="bert-base-nli-mean-tokens":
            annoy_size = 768
            return annoy_size
        else:
            raise Exception("Invalid SENTENCE_TRANSFORMER_MODEL_TYPE")

settings = Settings()

assert settings.TRAIN_DATA_INPUT_TYPES in [["title"],["text"],["title","text"]], "Data input types must be in title or text or both"

if settings.TEXT_SECTION_TYPE=="sentence":
    assert "title" not in settings.TRAIN_DATA_INPUT_TYPES, "title is not supported for sentence section type"
    settings.TRAIN_DATA_INPUT_TYPES = settings.TRAIN_DATA_INPUT_TYPES.sort(reverse=True)
    
