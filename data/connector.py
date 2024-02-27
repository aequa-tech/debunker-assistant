from sqlalchemy import create_engine, text, insert, MetaData, Table, Column, Text, Date, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Tuple,List,Dict
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

        engine = create_engine(connection_string,echo=True)

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

        metadata = MetaData(bind=engine)
        

        # Replace 'your_table' with the name of the table you want to open
        table_name = name

        # Access the table object
        table = Table(table_name, metadata,autoload=True)

        #metadata.create_all(engine)
        return table
    
    def create_table(self,name,engine,cols:List[Tuple],keys:List[Tuple]=None):
        
        ''' aggiungere chiave primaria'''

        assert len(cols) == len(keys)
        data_types = {'integer':Integer,'text':Text,'bool':Boolean,'date':Date}
        metadata = MetaData()

        columns = list()
        for col in cols:
            columns.append(Column(col[0],data_types[col[1]]))

        table_name = name

        table = Table(table_name, metadata, *columns)

        metadata.create_all(engine)

        
        
        
    
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
    
    def insert_rows(self,engine,table,data):
        print(data)
        Session = sessionmaker(bind=engine)
        
        session = Session()
        
        query = table.insert()

        query.values({'id':34,'text':'ciao ciao'})

        session.execute(query)

        session.commit()

        session.close()



    def insert(self,engine,query,data):

        with engine.connect() as conn:
            conn.execute(text(query),data)
            conn.commit()
    
    def read(self,engine,query):

        with engine.connect() as conn:

            res = conn.execute(text(query))
            result = [r for r in res]

            return result
                
        
        

    
    def read_table(self,engine,table_name,query):
        sql_query = "{} {}".format(query,table_name)
        print(sql_query)
        with engine.connect() as connection:
            result = connection.execute(text(sql_query))
            rows = result.fetchall()
        

        return rows


    
def main():
    conn = Connector()
    engine = conn.engine_postgres(user='debunker',passw='A283hnd(902!)?]',host='db.aequa-tech.com:54321',db='DA')
    
    table = conn.open_table(name='prova',engine=engine)
    
    elem = {"id":15,"text":"ciao"}
    conn.insert_rows(engine=engine,table=table,data=elem)
    
    res = conn.read_table(engine,'prova','SELECT * FROM')
    for r in res:print(r)
    
if __name__=="__main__":
    main()