from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .Config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine= create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base= declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#can delete this as now sqlalchemy is connecting to the database 
#while psycopg2 allowed user to connect to database.
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='PythonFastAPI', user='postgres',
                            password='Pass@7875word', cursor_factory=RealDictCursor)
    
        cursor=conn.cursor()
        print("Database connection was successful.")
        break
    except Exception as error:
        print("Connection to database failed.")
        print("Error:", error)
        time.sleep(3)