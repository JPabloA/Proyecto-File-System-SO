import datetime
from file import File


class Directory:
    def __innit__(self, name):
        self.name = name
        self.creationDate = datetime.now()
        self.files = {}
        self.directories = {}

# To create a file in the directory
def createFile (self, fileName, fileExtension, fileContent):
    if fileName in self.files:
        raise ValueError("A file with this name already exists.")
    newFile = File(fileName, fileExtension, fileContent)
    self.files[fileName] = newFile

def createDirectory (self, directoryName):
    if directoryName in self.files or directoryName in self.directories:
        raise ValueError("A file or directory with this name already exists.")
    newDirectory = Directory(directoryName)
    self.directories[directoryName] = newDirectory;
    
def listDirectory(self):
    contentList = []
    for dirName in self.directories:
        contentList.append(f"[DIR] {dirName}")
    for fileName in self.files:
        contentList.append(f"[FILE] {fileName}")
    return contentList

def remove_file(self, name):
    if name in self.files:
        del self.files[name]
    else:
        raise ValueError("File not found.")

def remove_directory(self, name):
    if name in self.directories:
        if self.directories[name].directories or self.directories[name].files:
            raise ValueError("Directory is not empty.")
        del self.directories[name]
    else:
        raise ValueError("Directory not found.")
    
# TODO: Move and Find element

# ? find siempre va desde la raiz (Por el momento la implementacion esta unicmanete desde la raiz y no desde el punto actual)
# TODO: Hace falta meterle tambien la parte de busqueda por extension????
def findElement(self, name):
    foundPaths = []
    
    # Archivos del directorio actual
    if name in self.files:
        foundPaths.append(f"{self.name}/{name}")
    
    # Directorios del directorio actual
    for dirName,subdir in self.directories:
        if dirName == name:
            foundPaths.append(f"{self.name}/{dirName}")
        # Parte recursiva
        foundPaths += subdir.findElement(name)