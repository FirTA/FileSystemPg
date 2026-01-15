import psycopg2
import os
from MenuOperations import clear, start_menu, option_detail, detail,  Action
from dotenv import load_dotenv
from InquirerPy import inquirer
from database import Database
from FileSystemRepo import FileSystemRepo

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

def search_object(data, key, value):
    for d in data:
        if getattr(d, key) == value:
            return d
    return None



if __name__ == '__main__':
    load_dotenv()
    
    state = {
        "db_status" : "connected",
        "root" : os.getenv("ROOT_PATH"),
        "current_path" : os.getenv("ROOT_PATH"),
    }
    start_menu(state)
    
    file_system = FileSystemRepo()
    while True :
        clear()
        print( state["current_path"])
        if state['root'] == state["current_path"]:
            file_system.get_list_dir(state['root'])
        else :
            file_system.get_list_dir(state['current_path'])
    
        ls = FileTreeOrder(file_system.get_list_data_by_name())
        ls.insert(0,'-- EXIT --')
        clear()
        if state['current_path'] == state['root']:
            option = inquirer.select(
                message = f"{state['current_path']}", 
                choices = ls,
                default = 2
            ).execute()
        else :
            ls.insert(1,"..")
            option = inquirer.select(
                message = f"{state['current_path']}", 
                choices = ls,
                default = 3
            ).execute()
            if option == "..":
                state['current_path'] = "/".join(state['current_path'].split("/")[:-1])
                continue
        if option == '-- EXIT --':
            break
        obj = file_system.get_object(option)
        if obj.is_directory:
            state['current_path'] = obj.path
        else :
            state['current_path'] = obj.path
            while True:
                clear()
                act = option_detail(state['current_path'])
                if act == Action.BACK:
                    state['current_path'] = "/".join(state['current_path'].split("/")[:-1])
                    break
                    
                if act == Action.DETAIL:
                        print(state['current_path'])
                        stat = file_system.get_object(obj.name)
                        print(stat)
                        inquirer.select(
                            message = f"<- ", 
                            choices = [{"name":"Back", "value" : Action.BACK}],
                        ).execute()

                
                if act == Action.DOWNLOAD:
                    file_system.read_file(obj.name)
                    input("Press Enter to continue...")
                    clear()