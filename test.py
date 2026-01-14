from InquirerPy import inquirer

if __name__ == '__main__':
    # name = inquirer.text(
    #     message = "masukan nama :"
    # ).execute()
    
    # name = inquirer.confirm(
    #     message = "masukan nama :",
    #     default = True
    # ).execute()
    
    name = inquirer.select(
        message = "Pilih Menu :",
        choices = ['1','2','3','5','12','14'],
        default=3,
        max_height= "50%"
    ).execute()
    
    # name = inquirer.checkbox(
    #     message = "Pilih Menu :",
    #     choices = ['1','2','3']
    # ).execute()
    
    
    
    
    print(name)