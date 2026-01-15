
from database import Database
from FileSystem import FileSystem     
from pathlib import Path   
import sys

class FileSystemRepo:
    def __init__(self):
        self.db = Database()
        self.list_object = []
        self.list_path = []
        
    def get_list_dir(self,path):
        with self.db as conn:
            curr = conn.cursor()
            try:
                self.list_object = []
                self.list_path = []
                curr.execute(f"SELECT pg_ls_dir('{path}')")
                temp = [row[0] for row in curr.fetchall()]
                for row in temp:
                    tmp_path = path +"/"+ row
                    curr.execute("SELECT (pg_stat_file(%s)).*",(path,))
                    columns = [desc[0] for desc in curr.description]
                    stat = dict(zip(columns, curr.fetchone()))
                    self.list_object.append(FileSystem(row, tmp_path, stat['size'], stat['access'], stat['modification'], stat['change'] ,stat['isdir']))
                    self.list_path.append(tmp_path)
            finally:
                conn.close()
                
    def get_list_data_by_name(self):
        return [data.name for data in self.list_object]
    
    def stat(self, path):
        with self.db as conn:
            curr = conn.cursor()
            curr.execute("SELECT (pg_stat_file(%s)).*",(path,))
            columns = [desc[0] for desc in curr.description]
            data = dict(zip(columns, curr.fetchone()))
        return data
    
    def get_object(self, name):
        return next(f for f in self.list_object if f.name == name)
    
    def stat_object(self, name):
        obj = self.get_object(name)
        print(obj.name)
        
    def read_file(self, name):
        obj = self.get_object(name)
        with self.db as conn:
            curr = conn.cursor()
            curr.execute("SELECT pg_read_binary_file(%s)",(obj.name,))
            data = curr.fetchone()
            
            if data and data[0] is not None:
                content = data[0].tobytes()
                folder = Path.home()/"Downloads"
                filepath = folder/obj.name
                
                total_size = len(content)
                chunk_size=1024 * 64
                written = 0
                with open(filepath, 'wb') as f:
                    for i in range(0, total_size, chunk_size):
                        chunk = content[i:i+chunk_size]
                        f.write(chunk)
                        written += len(chunk) 
                        percent = written / total_size * 100
                        sys.stdout.write(
                            f"\rDownloading {obj.name} [{percent:6.2f}%]"
                        )
                        sys.stdout.flush()
                print("\nDownload complete ✔")
            else :
                content = "Can't read file"
