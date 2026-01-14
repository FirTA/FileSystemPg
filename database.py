import psycopg2
import os

class Database:
    def __enter__(self):
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return self.conn
    
    def __exit__(self, exc_type, exc, tb):
        self.conn.close()