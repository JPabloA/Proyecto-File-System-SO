import datetime
from .file import File
from tkinter import messagebox


class Directory:
    def __init__(self, name):
        self.name = name
        self.creationDate = datetime.datetime.now()
        self.files = {}
        self.directories = {}

    # To create a file in the directory
    def createFile (self, fileName, fileExtension, fileContent):
        if fileName in self.files:
            messagebox.showwarning("Nombre debe ser unico", "Ya existe un archivo con el mismo nombre")

        newFile = File(fileName, fileExtension, fileContent)
        self.files[fileName] = newFile

    def createDirectory (self, directoryName: str):
        if directoryName in self.files or directoryName in self.directories:
            return None

        newDirectory = Directory(directoryName)
        self.directories[directoryName] = newDirectory
        return newDirectory

    def getDirectoryName(self):
        return self.name

    def listDirectory(self):
        contentList = []
        for dirName in self.directories:
            contentList.append(f"[DIR] {dirName}")
        for file in self.files.values():
            contentList.append(f"[FILE] {file.name}.{file.extension}")
        return contentList

    def findFiles(self, name: str) -> list[str]:
        search_result = []

        for file in self.files.values():
            fullFile_name = f"{file.name}.{file.extension}"
            if name in fullFile_name:
                search_result.append(f"{file.name}.{file.extension}")

        return search_result

    def changeFileNameInDict(self, oldName, newName):
        element = self.files.pop(oldName)
        self.files[newName] = element

    def clearDirectory(self):
        self.directories = {}
        self.files = {}

    def getFiles(self):
        return self.files

    def getDirectories(self):
        return self.directories

    def removeDirectory(self, name):
        if name in self.directories:
            self.directories.pop(name)

    def removeFile(self, name):
        if name in self.files:
            self.files.pop(name)

    def __getDirectorySize(self, selected_dir, total_size: int = 0):
        for file in selected_dir.files.values():
            total_size += file.size

        for s_dir in selected_dir.directories.values():
            total_size = self.__getDirectorySize( s_dir, total_size )

        return total_size

    def viewProperties(self):
        dir_total_size = self.__getDirectorySize( self )
        return {
            "name": self.name,
            "creationDate": self.creationDate.strftime("%Y-%m-%d %H:%M:%S"),
            "number_items": len( self.files ) + len( self.directories ),
            "total_size": dir_total_size
        }

    def print_tree(self, directory, indent=0, tree: str = ""):
        tree += (' ' * indent + f"[DIR] {directory.getDirectoryName()}\n")
        for file in directory.getFiles().values():
            tree += (' ' * (indent + 4) + f"[FILE] {file.name}.{file.extension}\n")
        for subdirectory in directory.getDirectories().values():
            tree = self.print_tree(subdirectory, indent + 4, tree)
        return tree