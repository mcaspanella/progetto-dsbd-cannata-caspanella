import psycopg2

def connect_POSTGRES():
    conn = psycopg2.connect(database='project_DSBD',
                            user="admin",
                            host='pipeline_dsbd-postgres-1',
                            password="admin",
                            port='5432')
    print("Database connected successfully")
    
    return conn