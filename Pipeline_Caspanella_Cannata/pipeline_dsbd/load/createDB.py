import psycopg2
import math 
import connect
from sqlalchemy import create_engine

conn = connect.connect_POSTGRES()
cur = conn.cursor() 

def create_table(table_name):
    query = """
                CREATE TABLE IF NOT EXISTS {} (metrics_name VARCHAR(150) PRIMARY KEY
                );""".format(table_name) 
                
    cur.execute(query)
    conn.commit()
    
    print("Table Created successfully")
              
        
def add_metrics(table_name, dataset):
    engine=create_engine("postgresql://admin:admin@pipeline_dsbd-postgres-1/project_DSBD")
    for column in dataset.columns:
        query = """
                ALTER TABLE {}  
                ADD COLUMN IF NOT EXISTS {} FLOAT
                ;""".format(table_name, column)
        
        cur.execute(query)
    conn.commit()
    print("Column Added")

    dataset.to_sql(table_name, engine, if_exists='replace', method='multi')
    print("Metrics added")
    