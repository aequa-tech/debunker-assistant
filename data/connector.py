from sqlalchemy import create_engine, MetaData, Table
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
    
    
    def read_table(self,name,engine,query:str='SELECT * FROM {}'):

        metadata = MetaData()
        metadata.reflect(bind=engine)

        # Replace 'your_table' with the name of the table you want to open
        table_name = name

        # Access the table object
        table = metadata.tables.get(table_name)

        with engine.connect() as connection:
            result = connection.execute(query.format(name))
            rows = result.fetchall()

        return rows
    




