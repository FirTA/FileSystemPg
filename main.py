import psycopg2

if __name__ == '__main__':
    print('test')
    conn = psycopg2.connect(
        dbname='mcgdata',
        user='mcgdata',
        password='mcgdata',
        host='172.31.93.221',
        port='5321'
    )
    
    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    