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
        if self.disk is None:
            raise ValueError("No disk created.")
        if name in self.currentDirectory.files:
            raise ValueError("Another file with the same name.")

        newFile = File(name, extension, content)
        sectors_list = self.disk.writeToDisk(content)

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
        self.currentDirectory.createDirectory(name)

    # ? Versión No usada
    def changeDirectory(self, selected_path: str):
        try:
            # Path string
            new_path = "/root"
            # Split the path into directories (Skip empty space and root)
            directories = selected_path.split("/")[2:]

            # Go throught all directories until reach the last directory
            selectedDirectory: Directory = self.root
            for d_name in directories:
                selectedDirectory = selectedDirectory.directories[ d_name ]
                new_path += f"/{d_name}"

            self.currentDirectory = selectedDirectory
            self.path = new_path
        except:
            # TODO: Pasar a messageBox
           print("No es directorio o no se logró reconocer bien")

    # def changeDirectory(self, directory_name: str, goBack: bool = False):
    #     try:
    #         if goBack and self.currentDirectory.parent_directory != None:
    #             self.path = self.path.rsplit("/", 1)[0]
    #             self.currentDirectory = self.currentDirectory.parent_directory
    #         elif not goBack:
    #             selected_directory: Directory = self.currentDirectory.directories[ directory_name ]
    #             self.path += f"/{directory_name}"
    #             self.currentDirectory = selected_directory
    #     except:
    #        # TODO: Pasar a messageBox
    #        print("No es directorio o no se logró reconocer bien")

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

    def __findInDirectory(self, search_value: str, selected_directory: Directory, dir_path: str):
        search_result = []
        dir_path += f"{selected_directory.name}/"
        for direc in selected_directory.directories.values():
            search_result.extend( self.__findInDirectory( search_value, direc, dir_path ) )

        search_result.extend( [f"[FILE] {dir_path}{f_file}" for f_file in selected_directory.findFiles(search_value)] )

        if search_value in selected_directory.name:
            search_result.append( f"[DIR] {dir_path[:-1]}" )

        return search_result

    # TODO: Encontrar un elemento ya sea carpeta o directorio
    def findElement(self, search_value: str):
        # Search name through all the root
        search_result: list[str] = self.__findInDirectory(search_value, self.root, "")

        # Order the result
        just_files = list( filter( lambda f: "[FILE]" in f, search_result ) )
        just_dirs  = list( filter( lambda d: "[DIR]" in d, search_result ) )
        result = just_dirs + just_files

        return result