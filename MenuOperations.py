import os
from InquirerPy import inquirer

class Action:
    EDIT = 'EDIT'
    ENTER = 'ENTER'
    EXIT = 'EXIT'
    DOWNLOAD = "DOWNLOAD"
    BACK = "BACK"
    DETAIL = "DETAIL"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
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
            new_path = input("Enter Root Path : ").strip()
            if not new_path.startswith('/'):
                print("Path must be absolute!")
                input("Press Enter to continue.........")
                continue
            state['root'] = new_path
        else:
            return
        
def option_detail(path):
    menu = [
        {"name":"Back to List", "value" : Action.BACK},
        {"name":"Download", "value" : Action.DOWNLOAD},
        {"name":"Detail", "value" : Action.DETAIL},
    ]
    
    return inquirer.select(
        message = f"{path}", 
        choices = menu,
    ).execute()

def detail(stat,path):
    print(path)

    return inquirer.select(
        message = f"<- ", 
        choices = [{"name":"Back", "value" : Action.BACK}],
    ).execute()
