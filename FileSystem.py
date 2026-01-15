class FileSystem:
    def __init__(self, name, path, size, last_access, last_modification, last_change ,is_directory):
        self.name = name
        self.path = path
        self.size = size
        self.last_access = last_access
        self.last_modification = last_modification
        self.last_change = last_change
        self.is_directory = is_directory
        
    
    def __str__(self):
        icon = "📁" if self.is_directory else "📄"
        size = "-" if self.is_directory else f"{self.size} B"
        mod = self.last_modification.strftime("%Y-%m-%d %H:%M")
        return f"{icon} {self.name:<50} {size:>10} {mod}"
