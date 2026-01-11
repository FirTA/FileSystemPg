import psycopg2
import os
from dotenv import load_dotenv


def list_dir(curr, path):
    curr.execute(f"SELECT pg_ls_dir('{path}')")
    return curr.fetchone()


if __name__ == '__main__':
    load_dotenv()
    print('test')
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

    
    with conn.cursor() as cur:
        while True:
            inp = input('root path : ')  
            db_fetch = list_dir(cur, f'{inp}')
            print(db_fetch)