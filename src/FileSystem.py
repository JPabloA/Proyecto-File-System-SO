from .file import File
from .directory import Directory
from .disk import Disk
from .fat import FAT

class FileSystem:

    # Directory structure: { filename, FAT_index }

    # FAT structure: [ ( sector_id, next_FAT_index ) ]
    fat: FAT
    disk: Disk | int

    def __init__(self):
        self.root = Directory("/root");
        self.currentDirectory = self.root
        self.disk = -2

        self.fat = FAT()

    def testing_printFAT(self):
        self.fat.printFAT()

    def create_disk(self, sector_count, sector_size):
        self.disk = Disk(sector_count, sector_size)
        self.disk.createDisk()
        self.fat.createTable( sector_count )

    def createFile(self, name, extension, content):
        if self.disk is None:
            raise ValueError("No disk created.")
        if name in self.currentDirectory.files:
            raise ValueError("Another file with the same name.")


        #!: Validacion de espacio disponible (Antes de crear el archivo)
        # required_sectors = (len(content) + self.disk.__sector_size - 1)
        # if len(self.disk.__free_sectors) < required_sectors:
        #     raise ValueError ("Not enough space on disk.")

        newFile = File(name, extension, content)
        sectors_list = self.disk.writeToDisk(content)

        if len(sectors_list) == 0:
            raise ValueError("File couldnt be assing on disk - Not enough space on disk")

        first_FAT_sector = self.fat.assingSectorList( sectors_list )

        # File save the first sector
        newFile.assignSectors( first_FAT_sector )
        self.currentDirectory.files[name] = newFile
        # to assign file sectors (Then we need to separate the function)

    def getCurrentWorkingDirectory(self):
        return self.currentDirectory.getDirectoryName()

    def createDirectory(self, name):
        self.currentDirectory.createDirectory(name);

    # ? Los de movimiento van a ser todo un mundo (Pendiente)
    # def changeDirectory(self, name):
    #     self.currentDirectory =

    def listDirectory(self):
        return self.currentDirectory.listDirectory()

    def removeFile(self, name):
        if name in self.currentDirectory.files:
            fileToRemove = self.currentDirectory.files.pop(name)
            for sectorIndex in fileToRemove.sectors:
                self.disk.__free_sectors.append(sectorIndex)
                #! here we write in disk
        else:
            raise ValueError ("File not found.")

    # TODO: Arreglar el borrado de los directorios (Recordar que deben de ser recursivos y volarse todo directorio o archivo que este dentro de el)
    def remove_directory(self, name):
        self.current_directory.remove_directory(name)

    # TODO: Terminar este move
    def moveElement():
        return

    # TODO: Encontrar un elemento ya sea carpeta o directorio
    def findElement(self, name):
        return self.root.findElement(name)