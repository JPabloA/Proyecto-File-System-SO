import datetime
from tkinter import Tk, Canvas, Entry, Button, Toplevel, messagebox
from src.file import File
from src.directory import Directory
from enum import Enum

class objType(Enum):
    DIRECTORY = 0
    FILE = 1
    
class Move_GUI(Toplevel):
    
    def __init__(self, parent, object):
        super().__init__(parent)
        
        self.parent = parent
        self.object = object 
        
        if isinstance(self.object, File):
            self.object: File
        elif isinstance(self.object, Directory):
            self.object: Directory
        
        self.geometry("750x593")
        self.configure(bg = "#FFFFFF")

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 593,
            width = 750,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        # Labels
        canvas.create_text( 9.0, 14.0, anchor="nw", text="Mover archivo/directorio:", fill="#000000", font=("Inter", 16 * -1) )
        canvas.create_text( 9.0, 98.0, anchor="nw", text="Hasta:", fill="#000000", font=("Inter", 16 * -1) )

        # Text input: Directory path
        self.textInput_SearchBar = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
        self.textInput_SearchBar.place( x=9.0, y=40.0, width=722.0, height=33.0 )
        print("print", self.object.name)
        if isinstance(self.object, File):
            self.textInput_SearchBar.insert(0, self.parent.fileSystem.getCurrentWorkingDirectory() + "/" + self.object.name + "." + self.object.extension)
        else:
            self.textInput_SearchBar.insert(0, self.parent.fileSystem.getCurrentWorkingDirectory() + "/" + self.object.name)
        self.textInput_SearchBar.config(state="disabled")

        # Text input: Directory path 2
        self.textInput_SearchBar2 = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.textInput_SearchBar2.place( x=9.0, y=126.0, width=722.0, height=33.0 )
        if isinstance(self.object, File):
            self.textInput_SearchBar2.insert(0, self.parent.fileSystem.getCurrentWorkingDirectory() + "/" + self.object.name + "." + self.object.extension)
        else:
            self.textInput_SearchBar2.insert(0, self.parent.fileSystem.getCurrentWorkingDirectory() + "/" + self.object.name)

        # Buttons
        self.button_1 = Button( self, text="Mover", borderwidth=0, highlightthickness=0, command=self.moveElement, relief="flat" )
        self.button_1.place( x=9.0, y=196.0, width=203.0, height=49.0 )

        self.button_2 = Button( self, text="Cancelar", borderwidth=0, highlightthickness=0, command=self.destroy, relief="flat" )
        self.button_2.place( x=9.0, y=270.0, width=203.0, height=49.0 )
    
    def moveElement(self):
        
        dest_base_path = self.textInput_SearchBar2.get()
        name = dest_base_path.rsplit("/",1)[-1]
        print("Name:", name)
        dest_path =  dest_base_path.rsplit("/",1)[0]
        
        if dest_path[-1] != "/":
            dest_path += "/"
            
        print("Este es el dest path: ", dest_path)
        currentDirectory = self.parent.fileSystem.currentDirectory
        
        
        if isinstance(self.object, Directory):
            objectType = objType.DIRECTORY #!Directory
        else: #!File
            objectType = objType.FILE 
        
        # To get the destiny directory (Remember that you need to add / as the final char to navigate correctly)
        destiny_dir = self.parent.fileSystem.navigateToDirectory(dest_path)
        
        # To verify that the path exists
        if destiny_dir == None:
            messagebox.showwarning("Ruta de destino no existe", "Favor ingresar una ruta de destino correcta")
            return
        
        # To verify that a directory can not be moved to the same directory
        if objectType == objType.DIRECTORY:
            if self.parent.fileSystem.getCurrentWorkingDirectory() + f"/{self.object.name}/" == dest_path:
                messagebox.showwarning("Accion no permitida","Un directorio no se puede contener a el mismo.")
                return
        
        # To verify that the object is unique in the destiny directory
        if objectType == objType.DIRECTORY:
            if not self.parent.isUniqueInDestinyDir(self.object.name, "Directory", dest_path):
                messagebox.showwarning("Directorios con el mismo nombre", "Ya existe un directorio con el mismo nombre")
                return
        else:
            if not self.parent.isUniqueInDestinyDir(self.object.name  + "." + self.object.extension, "File", dest_path):
                messagebox.showwarning("Archivos con el mismo nombre", "Ya existe un archivo con el mismo nombre")
                return
            
        
        #Prints para ver cambios
        print("base", currentDirectory.directories)
        print("destino", destiny_dir.directories)
        
        # To delete and add the file or directory from the current dir dictionary to the dest dir dictionary
        if objectType == objType.DIRECTORY:
            currentDirectory.removeDirectory(self.object.name)
            destiny_dir.directories[self.object.name] = self.object
        else:
            currentDirectory.removeFile(self.object.name + "." + self.object.extension)
            self.object.modificationDate = datetime.datetime.now()
            # Actualizar nombre y extension del archivo
            self.object.name = name.split(".")[0]
            self.object.extension = name.split(".")[1]
            destiny_dir.files[name] = self.object
        
        #Prints para ver cambios
        print("Luego del move")
        print("base", currentDirectory.directories)
        print("destino", destiny_dir.directories)
        
        self.destroy()
            
        