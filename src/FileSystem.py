from .file import File
from .directory import Directory
from .disk import Disk
from .fat import FAT

class FileSystem:

    # Directory structure: { filename, FAT_index }

    # FAT structure: [ ( sector_id, next_FAT_index ) ]
    fat: FAT
    disk: Disk | None
    def __init__(self):
        self.path = "/root"
        self.root = Directory( self.path );
        self.currentDirectory = self.root
        self.disk = None

        self.fat = FAT()

    def testing_printFAT(self):
        self.fat.printFAT()

    def create_disk(self, sector_count, sector_size):
        self.disk = Disk(sector_count, sector_size)
        self.disk.createDisk()
        self.fat.createTable( sector_count )

    def createFile(self, name, extension, content):

        #!: Validacion de espacio disponible (Antes de crear el archivo)
        # required_sectors = (len(content) + self.disk.__sector_size - 1)
        # if len(self.disk.__free_sectors) < required_sectors:
        #     raise ValueError ("Not enough space on disk.")

        newFile = File(name, extension, content)
        sectors_list = self.disk.writeToDisk(content)

        # Validacion sacarla a una nueva funcion por cuestiones de GUI
        if len(sectors_list) == 0:
            raise ValueError("File couldnt be assing on disk - Not enough space on disk")

        first_FAT_sector = self.fat.assingSectorList( sectors_list )

        # File save the first sector
        newFile.assignSectors( first_FAT_sector )
        self.currentDirectory.files[name] = newFile

    def getCurrentWorkingDirectory(self):
        # return self.currentDirectory.getDirectoryName()
        return self.path

    def createDirectory(self, name):
        self.currentDirectory.createDirectory(name, self.currentDirectory)

    # ? Versión No usada
    # def changeDirectory_versionRecorrerLista(self, selected_path: str):
    #     try:
    #         # Path string
    #         new_path = "/root"
    #         # Split the path into directories (Skip empty space and root)
    #         directories = selected_path.split("/")[2:]

    #         # Go throught all directories until reach the last directory
    #         selectedDirectory: Directory = self.root
    #         for d_name in directories:
    #             selectedDirectory = selectedDirectory.directories[ d_name ]
    #             new_path += f"/{d_name}"

    #         print( selectedDirectory.name )
    #         print( new_path )

    #         self.currentDirectory = selectedDirectory
    #         self.path = new_path
    #     except:
    #         # TODO: Pasar a messageBox
    #        print("No es directorio o no se logró reconocer bien")

    def changeDirectory(self, directory_name: str, goBack: bool = False):
        try:
            if goBack and self.currentDirectory.parent_directory != None:
                self.path = self.path.rsplit("/", 1)[0]
                self.currentDirectory = self.currentDirectory.parent_directory
            elif not goBack:
                selected_directory: Directory = self.currentDirectory.directories[ directory_name ]
                self.path += f"/{directory_name}"
                self.currentDirectory = selected_directory
        except:
           # TODO: Pasar a messageBox
           print("No es directorio o no se logró reconocer bien")

    def listDirectory(self):
        return self.currentDirectory.listDirectory()

    def removeFile(self, name):
        if name in self.currentDirectory.files:
            fileToRemove = self.currentDirectory.files.pop(name)
            for sectorIndex in fileToRemove.sectors:
                self.disk.__free_sectors.append(sectorIndex)
                #! here we write in disk
        else:
            # actualmente chambeando en este
            # me parece que remove remove no deberia de tener valida (Tal vez si para cuando no se ha refrescado)
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
    
    # To get the file content
    
    def getFileContent (self, fileObj):
        # To obtain sectors list
        fileSectors = self.fat.getFileSectors(fileObj.fat_index)

        # To read the content
        fileContent = self.disk.readFromDisk(fileSectors)

        return fileContent