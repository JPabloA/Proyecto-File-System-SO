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

    def createFile(self, name, extension, content, selected_directory: Directory = None):

        if selected_directory is None:
            selected_directory = self.currentDirectory

        newFile = File(name, extension, content)
        sectors_list = self.disk.writeToDisk(content)

        # Validacion sacarla a una nueva funcion por cuestiones de GUI
        if len(sectors_list) == 0:
            raise ValueError("File couldnt be assing on disk - Not enough space on disk")

        first_FAT_sector = self.fat.assingSectorList( sectors_list )

        # File save the first sector
        newFile.assignSectors( first_FAT_sector )
        selected_directory.files[f"{name}.{extension}"] = newFile

    def getCurrentWorkingDirectory(self):
        # return self.currentDirectory.getDirectoryName()
        return self.path

    def createDirectory(self, name: str, selected_directory: Directory = None):
        if selected_directory is None:
            selected_directory = self.currentDirectory

        return selected_directory.createDirectory(name)

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

    def listDirectory(self):
        return self.currentDirectory.listDirectory()

    # Get the directory from a path
    def navigateToDirectory(self, path: str):
        selected_directory: Directory = self.currentDirectory

        if "/" in path:
            directories = path.split("/")[2:-1]
            selected_directory = self.root
            for d_name in directories:
                try:
                    selected_directory = selected_directory.directories[d_name]
                except KeyError:
                    print("Bad path received")
                    return None
        return selected_directory

    # Clear directory content (Recursively)
    def __clearDirectoryContent(self, current_dir: Directory):

        # Clear all subdirectories
        for subdirectory in list( current_dir.directories.values() ):
            self.__clearDirectoryContent( subdirectory )

        # Remove all files in the current directory
        files_to_delete = [f"{file.name}.{file.extension}" for file in current_dir.files.values()]
        for f_name in files_to_delete:
            try:
                selected_file: File = current_dir.files.pop( f_name )
                sector_list = self.fat.freeFATEntries( selected_file.fat_index )
                self.disk.removeFromDisk( sector_list )
            except:
                print(f"File: {f_name} not found --- Continuing...")

        # Remove all the directories in the current directory
        dirs_to_delete = list( current_dir.directories.keys() )
        for d_name in dirs_to_delete:
            try:
                del current_dir.directories[ d_name ]
            except:
                print(f"Dir: {d_name} not found --- Continuing...")

    # Remove a file by its name/path
    def removeFile(self, file_name: str):
        selected_directory: Directory = self.navigateToDirectory( file_name )
        if selected_directory is None:
            return

        file_name = file_name.split("/")[-1]

        if file_name not in selected_directory.files:
            raise ValueError ("File not found.")

        selected_file: File = selected_directory.files.pop( file_name )
        sector_list = self.fat.freeFATEntries( selected_file.fat_index )
        self.disk.removeFromDisk( sector_list )

    # Remove a directory by its name/path
    def remove_directory(self, dir_name: str):
        selected_directory: Directory = self.navigateToDirectory( dir_name )
        if selected_directory is None:
            return

        dir_name = dir_name.split("/")[-1]

        if dir_name not in selected_directory.directories:
            raise ValueError ("Directory not found.")

        directory_to_remove: Directory = selected_directory.directories[dir_name]
        self.__clearDirectoryContent(directory_to_remove)
        selected_directory.directories.pop(dir_name)


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
    def findElement(self, name):
        return self.root.findElement(name)
    
    # To get the file content
    
    def getFileContent (self, fileObj):
        # To obtain sectors list
        fileSectors = self.fat.getFileSectors(fileObj.fat_index)

        # To read the content
        fileContent = self.disk.readFromDisk(fileSectors)

        return fileContent
    
    def findElement(self, search_value: str):
        # Search name through all the root
        search_result: list[str] = self.__findInDirectory(search_value, self.root, "")

        # Order the result
        just_files = list( filter( lambda f: "[FILE]" in f, search_result ) )
        just_dirs  = list( filter( lambda d: "[DIR]" in d, search_result ) )
        result = just_dirs + just_files

        return result
