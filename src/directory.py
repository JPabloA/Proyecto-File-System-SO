import datetime
from .file import File


class Directory:
    def __init__(self, name):
        self.name = name
        self.creationDate = datetime.datetime.now()
        self.files = {}
        self.directories = {}

    # To create a file in the directory
    def createFile (self, fileName, fileExtension, fileContent):
        if fileName in self.files:
            raise ValueError("A file with this name already exists.")
        newFile = File(fileName, fileExtension, fileContent)
        self.files[fileName] = newFile

    def createDirectory (self, directoryName: str):
        if directoryName in self.files or directoryName in self.directories:
            raise ValueError("A file or directory with this name already exists.")

        newDirectory = Directory(directoryName)
        self.directories[directoryName] = newDirectory

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

    def getFiles(self):
        return self.files

    def getDirectories(self):
        return self.directories