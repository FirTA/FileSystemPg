import psycopg2
import os
from dotenv import load_dotenv
from InquirerPy import inquirer
from database import Database

class Action:
    EDIT = 'EDIT'
    ENTER = 'ENTER'
    EXIT = 'EXIT'
    DOWNLOAD = "DOWNLOAD"
    BACK = "BACK"
    DETAIL = "DETAIL"

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
        
class FileSystemRepo:
    def __init__(self, db: Database):
        self.db = db.cursor()
        self.list_dir = []
        
    def get_list_dir(self,path):
        self.db.execute(f"SELECT pg_ls_dir('{path}')")
        temp = [row[0] for row in self.db.fetchall()]
        for row in temp:
            self.db.execute(f"(SELECT pg_stat_file('{path+row}')).*")
            columns = [desc[0] for desc in self.db.description]
            print(columns)
            stat = dict(zip(columns, self.db.fetchone()))
            print(stat)
            self.list_dir.append(FileSystem(row, row, stat['size'], stat['access'], stat['modification'], stat['change'] ,stat['isdir']))
                
    
    def stat(self, path):
        with self.db as curr:
            curr.execute(f"SELECT (pg_stat_file('{path}')).*")
            columns = [desc[0] for desc in curr.description]
            data = dict(zip(columns, curr.fetchone()))
        return data

def print_list(data):
        for i in data:
            print(i)

def order(data, reverse = False):
    return sorted(data, key=str.lower,reverse=reverse)

def order(data, key, reverse =False):
    return sorted(data,key=lambda obj:getattr(obj,key).lower(), reverse=reverse)

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

def list_object_order(data, key, reverse):
    files = []
    folders = []
    
    for a in data:
        if a.is_directory:
            folders.append(a)
        else:
            files.append(a)
    
    file = order(file, key, reverse)
    folder = order(folder, key, reverse)
    
    return file+folder

def option_detail(path):
    menu = [
        {"name":"Back to List", "value" : Action.BACK},
        {"name":"Download", "value" : Action.DOWNLOAD},
        {"name":"Detail", "value" : Action.DETAIL},
        {"name":"Exit", "value" : Action.EXIT},
    ]
    
    return inquirer.select(
        message = f"{path}", 
        choices = menu,
    ).execute()

def start_menu(state):
    while True:
        clear()
        print("Welcome to FileSystemPg")
        print(f"Root : {state['root']}\n")
        menu = [
            {"name":f"Edit Root Path : {state['root']}", "value" : Action.EDIT},
            {"name":"Explore", "value" : Action.ENTER},
        ]
        option = inquirer.select(
            message = "", 
            choices = menu,
        ).execute()
        
        if option == Action.EDIT:
            state['root'] = input("Enter Root Path : ")
            clear()
        else:
            return

def search_object(data, key, value):
    for d in data:
        if getattr(d, key) == value:
            return d
    return "not found"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    load_dotenv()
    
    state = {
        "db_status" : "connected",
        "root" : os.getenv("ROOT_PATH"),
    }
    start_menu(state)
    
    with Database() as db :
        get_dir = FileSystemRepo(db)
        get_dir.get_list_dir(state['root'])
        print(get_dir.list_dir)
    
    


    
    # while True:
    #     current_path = f'{os.getenv('ROOT_PATH')}'
    #     curr = utility(conn)
    #     db_fetch = curr.list_dir(current_path)
    #     list_object = []
    #     for row in db_fetch:
    #         stat = curr.stat(current_path+row)
    #         fs = FileSystem(row, row, stat['size'], stat['access'], stat['modification'], stat['change'] ,stat['isdir'])
    #         list_object.append(fs)
            
    #     list_object = list_object_order(list_object, 'name', False)
    #     choices = [data.name for data in list_object]
    #     select_detail = inquirer.select(
    #         message = current_path,
    #         choices = choices,
    #         default=3,
    #         max_height= "50%"
    #     ).execute()
        
    #     obj = search_object(list_object, 'name', select_detail)
    #     if obj.is_directory:
    #         db_fetch = curr.list_dir(current_path+obj.name)
    #         print(db_fetch)
    #         break

        
    #     option = option_detail()
    #     if option == "Back to List":
    #         False
    #     else:
    #         break