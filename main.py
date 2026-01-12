import psycopg2
import os
from dotenv import load_dotenv

class File():
    def __init__(self, extention):
        self.extention = extention
    
class Folder:
    def __init__(self):
        pass
    
class FileSystem:
    def __init__(self, name, path, size, last_access, last_modification, last_change ,is_directory):
        self.path = path
        self.name = name
        self.size = size
        self.last_access = last_access
        self.last_modification = last_modification
        self.last_change = last_change
        self.is_directory = is_directory
    
    def __str__(self):
        icon = "📁" if self.is_directory else "📄"
        size = "-" if self.is_directory else f"{self.size} B"
        # mod = self.last_modification("%Y-%m-%d %H:%M")

        return f"{icon} {self.name:<50} {size:>10} "
        
class utilty:
    def __init__(self,conn):
        self.cursor = conn.cursor()
        
    def list_dir(self,path):
        self.cursor.execute(f"SELECT pg_ls_dir('{path}')")
        return [row[0] for row in self.cursor.fetchall()]
    
    def stat(self, path):
        self.cursor.execute(f"SELECT (pg_stat_file('{path}')).*")
        columns = [desc[0] for desc in self.cursor.description]
        data = dict(zip(columns, self.cursor.fetchone()))
        # print(data)
        return data

def print_list(data):
        for i in data:
            print(i)

def order(data, reverse = False):
    return sorted(data, key=str.lower,reverse=reverse)

def FileTreeOrder(data, reverse = False):
    file = []
    folder = []
    
    for a in data:
        if '.' in a:
            file.append(a)
        else:
            folder.append(a)
    
    file = order(file, reverse)
    folder = order(folder, reverse)
    
    return folder+file


if __name__ == '__main__':
    load_dotenv()
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    
    while True:
        curr = utilty(conn)
        db_fetch = curr.list_dir(f'{os.getenv('ROOT_PATH')}')
        # print_list(FileTreeOrder(db_fetch, False))
        list_object = []
        for row in db_fetch:
            stat = curr.stat(f'{os.getenv('ROOT_PATH')}'+row)
            fs = FileSystem(row, row, stat['size'], stat['access'], stat['modification'], stat['change'] ,stat['isdir'])
            list_object.append(fs)
        
        print_list(list_object)
        # print(curr.stat('/u01/CSV/MPO04030925G.029'))
        break