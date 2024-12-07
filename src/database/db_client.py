from sqlalchemy import MetaData, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql import text
from src.database.models import initialize_tables, create_table
import pandas as pd

class Client:
    def __init__(self, engine, schema_name):
        self.schema = schema_name
        self.engine = engine
        self.meta = MetaData(schema=self.schema)
        self.Session = scoped_session(sessionmaker(self.engine))

        self._initialize_tables_if_not_exists()

    def _initialize_tables_if_not_exists(self):
        inspector = Inspector.from_engine(self.engine)

        schemas = inspector.get_schema_names()
        if self.schema not in schemas:
            with self.engine.connect() as connection:
                connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{self.schema}"'))
                connection.commit()
                
        existing_tables = inspector.get_table_names(schema=self.schema)
        required_tables = ["news_article"]

        missing_tables = [table for table in required_tables if table not in existing_tables]

        if missing_tables:
            initialize_tables(
                engine=self.engine, 
                schema=self.schema
            )

    def create_table(
        self,
        data_path:str,
        **kwargs
    ):
        
        try:
            session = self.Session()
            session.connection(execution_options={"schema_translate_map": {None: self.meta.schema}})
            create_table(
                session=session,
                data_path=data_path,
                **kwargs
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()