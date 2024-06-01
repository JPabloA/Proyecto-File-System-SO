from file import File
from directory import Directory

class FileSystem:
    def __innit__(self):
        self.root = Directory("root");
        self.currentDirectory = self.root
        self.disk = None
        
def create_disk(self, sector_count, sector_size):
    self.disk = VirtualDisk(sector_count, sector_size)