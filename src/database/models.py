from sqlalchemy import (
    Column, String, Text, JSON, Float, Integer, DateTime, func
)
from sqlalchemy.orm import declarative_base
import pandas as pd

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_article"
    
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, nullable=True)
    category = Column(String)
    subcategory = Column(String)
    title = Column(String)
    published_date = Column(DateTime(timezone=True), server_default=func.now())
    text = Column(Text)
    source = Column(String)
    
def create_table(
    session,
    data_path:str,
    **kwargs
):
    try:
        article = session.query(NewsArticle).first()
        if article:
            return True
        else:
            data = pd.read_csv(data_path)
            for _, row in data.iterrows():
                article = NewsArticle(
                    id=row["id"],
                    article_id=row["article_id"],
                    category=row["category"],
                    subcategory=row["subcategory"],
                    title=row["title"],
                    published_date=row["published_date"],
                    text=row["text"],
                    source=row["source"]
                )
                session.add(article)
    except Exception as e:
        raise e

def initialize_tables(engine, schema=None):
    if schema:
        for table in Base.metadata.tables.values():
            table.schema = schema    
    Base.metadata.create_all(engine)