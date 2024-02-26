from sqlalchemy import create_engine, MetaData, Table, Column, Text, Date, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from typing import Tuple,List
import logging as log
import psycopg2

log.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=log.INFO,
    datefmt='%d/%m/%Y %H:%M:%S'
)


class Connector:
    def __init__(self):
        pass

    def engine_postgres(self,user:str,passw:str,host,db:str):
        user = user
        passw = passw
        host = host
        db = db

        connection_string = f'postgresql+psycopg2://{user}:{passw}@{host}/{db}'

        engine = create_engine(connection_string)

        return engine
    

    def engine_sqlite(self,path:str):
        
        connection_string = f'sqlite:///{path}'
        engine = create_engine(connection_string)

        return engine

    
    def check_connection(self,engine):

        try:
            connection = engine.connect()
            connection.close()

            log.info("Connected to the database")
        except Exception as e:
            log.info(f"Unable to connect to the database for the following error: {e}")
    
    
    def open_table(self,name,engine):

        metadata = MetaData()
        

        # Replace 'your_table' with the name of the table you want to open
        table_name = name

        # Access the table object
        table = Table(table_name, metadata, autoload_with=engine)
        #table = metadata.tables.get(table_name)

        
        return table
    
    def create_table(self,name,engine,cols:List[Tuple]):
        
        data_types = {'integer':Integer,'text':Text,'bool':Boolean,'date':Date}
        metadata = MetaData()

        columns = list()
        for col in cols:
            columns.append(Column(col[0],data_types[col[1]]))

        table_name = name

        table = Table(table_name, metadata, *columns)

        table = metadata.create_all(engine)
        
        return table
    
    def check_table(self,name,engine):

        metadata = MetaData()
        metadata.reflect(bind=engine)

        table_name = name

        if table_name in metadata.tables:
            log.info('The table exists')

            return True

        else:
            log.info('The table exists')
            
            return False
        


    
    




