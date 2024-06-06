import datetime


class File:
    def __init__(self, name, extension, content):
        self.name = name
        self.extension = extension
        self.content = content
        self.creationDate = datetime.datetime.now()
        self.modificationDate = datetime.datetime.now()
        self.size = len(content)
        self.fat_index: int = -1

    # Functions

    # To modify the file content
    def modifyContent(self, newContent):
        self.content = newContent
        self.modificationDate = datetime.now()
        self.size = len(newContent)

    # To view the file content
    def viewContent(self):
        # TODO: Que deberiamos de hacer aca?
        return self.content

    # To view the file properties
    def viewProperties(self):
        return {
            "name": self.name,
            "extension": self.extension,
            "creationDate": self.creationDate,
            "modificationDate": self.modificationDate,
            "size": self.size
            }

    # To assign file sectors
    def assignSectors(self, starting_index):
        self.fat_index = starting_index

    # To release file sectors
    # TODO: falta limpiar bien la estructura que vayamos a utilizar para el disco
    def releaseSectors(self):
        return -1
    
    # To get the file sectors