import GUI.showTree_GUI as showTree_GUI
import GUI.createDirectory_GUI as createDirectory_GUI
import GUI.move_GUI as move_GUI
import GUI.seeProperties_GUI as seeProperties_GUI
import GUI.createDisk_GUI as createDisk_GUI
import GUI.copy_GUI as copy_GUI
import GUI.createFile_GUI as createFile_GUI
import GUI.editFile_GUI as editFile_GUI
from tkinter import SINGLE, END, Tk, Canvas, Entry, Button, Listbox, Menu, messagebox

from src.FileSystem import FileSystem
from src.file import File
from src.directory import Directory

class FileSystem_GUI(Tk):

    fileSystem: FileSystem

    # Global class variables
    textInput_DirectoryPath: Entry
    textInput_SearchBar: Entry
    textArea_Display: Listbox

    def __init__(self):
        super().__init__()

        self.title("File system custom - OS")
        self.geometry("750x550")
        self.configure(bg = "#FFFFFF")

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 550,
            width = 750,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        # Get the current directory
        self.fileSystem = FileSystem()

        # Label "Buscador"
        canvas.place(x = 0, y = 0)
        canvas.create_text( 9, 445.0, anchor="nw", text="Buscador", fill="#000000", font=("Inter", 13 * -1) )

        # Text input: Directory path
        self.textInput_DirectoryPath = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=("Inter", 14))
        self.textInput_DirectoryPath.place( x=54.0, y=11.0, width=622.0, height=35.0 )

        self.__loadCurrentWorkingDirectory()

        # Text input: Search bar
        self.textInput_SearchBar = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.textInput_SearchBar.place( x=9.0, y=465.0, width=150.0, height=30.0 )

        # Text area: Display
        self.textArea_Display = Listbox( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, selectmode=SINGLE, font="Arial 14" )
        self.textArea_Display.place( x=173.0, y=72.0, width=558.0, height=459.0 )
        self.textArea_Display.bind("<Button-3>", lambda event: self.__contentDisplayRightClick(event))
        self.textArea_Display.bind("<Double-Button-1>", self.__onFSDoubleClick)

        self.__loadContentInFSDisplay()

        # Button: Refresh display directory
        button_UpdateDirectory = Button( text="↺", command=lambda: self.__loadContentInFSDisplay() , relief="flat", font="Arial 16" )
        button_UpdateDirectory.place( x=696.0, y=11.0, width=35.0, height=35.0 )

        # Button: Go 1 directory back
        button_GoBack = Button( text="←", command=self.__goBackDirectory , relief="flat", font="Arial 16" )
        button_GoBack.place( x=9.0, y=11.0, width=35.0, height=35.0 )

        button_1 = Button( text="Crear Disco", command=self.display_CreateDisk_GUI, relief="flat" )
        button_1.place( x=9.0, y=72.0, width=150.0, height=35.0 )

        button_2 = Button( text="Crear Directorio", borderwidth=0, command=self.display_CreateDirectory_GUI, relief="flat" )
        button_2.place( x=9.0, y=119.0, width=150.0, height=35.0 )

        button_3 = Button( text="Crear Archivo", borderwidth=0, command=self.display_CreateFile_GUI, relief="flat" )
        button_3.place( x=9.0, y=166.0, width=150.0, height=35.0 )

        button_4 = Button( text="Desp. Árbol", borderwidth=0, command=self.display_WindowShowTree, relief="flat" )
        button_4.place( x=9.0, y=213.0, width=150.0, height=35.0 )

        button_5 = Button( text="Buscar", borderwidth=0, command=self.__onSearchRequest, relief="flat" )
        button_5.place( x=9.0, y=503.0, width=150.0, height=30.0 )

    def __goBackDirectory(self):
        current_path = self.fileSystem.getCurrentWorkingDirectory()
        current_path = current_path.rsplit("/", 1)[0]

        if len(current_path) != 0:
            self.fileSystem.changeDirectory ( current_path )
            self.__loadCurrentWorkingDirectory()
            self.__loadContentInFSDisplay()

    def __onFSDoubleClick(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            value = widget.get(index)

            if "[DIR]" in value:
                directory_name: str = value.split("[DIR] ")[1]
                desired_path = directory_name if "/" in directory_name else self.fileSystem.getCurrentWorkingDirectory() + f"/{directory_name}"

                self.fileSystem.changeDirectory( desired_path )
                self.__loadCurrentWorkingDirectory()
                self.__loadContentInFSDisplay()
                print("Abriendo carpeta...")
            else:
                fileName = value.split("[FILE] ")[1]
                fileObj = self.getFileObj(fileName)
                content = self.getFileContent(fileObj)
                self.display_EditFile_GUI(fileObj, content)


    def __loadCurrentWorkingDirectory(self):
        cwd = self.fileSystem.getCurrentWorkingDirectory()

        self.textInput_DirectoryPath.config(state="normal")
        self.textInput_DirectoryPath.delete(0, END)
        self.textInput_DirectoryPath.insert(0, cwd)
        self.textInput_DirectoryPath.config(state="disabled")

    def __contentDisplayRightClick(self, event):
        # Get the selected file/directory
        try:
            index = self.textArea_Display.nearest(event.y)
            self.textArea_Display.select_clear(0, END)
            self.textArea_Display.selection_set( index )
            selected_item: str = self.textArea_Display.get( index )
        except IndexError:
            return

        if len(selected_item) <= 0:
            return

        selected_obj: File | Directory

        if "[FILE]" in selected_item:
            selected_item = selected_item.split("[FILE] ")[-1]
            selected_obj = self.getFileObj( selected_item )
        elif "[DIR]" in selected_item:
            selected_item = selected_item.split("[DIR] ")[-1]
            selected_obj = self.getDirObj( selected_item )

        menu = Menu( tearoff=0 )

        if "[FILE]" in selected_item:
            name = selected_item.split("[FILE] ")[-1]
            object = self.getFileObj(name)
            content = self.getFileContent(object)
        elif "[DIR]" in selected_item:
            name = selected_item.split("[DIR] ")[-1]
            object = self.getDirObj(name)

        menu.add_command(label="Abrir", font="Arial 12", command= lambda: self.display_EditFile_GUI(object, content))
        menu.add_command(label="Eliminar", font="Arial 12", command = lambda: self.__deleteFunction( selected_item ))
        menu.add_command(label="Copiar", font="Arial 12", command=lambda: self.display_Copy_GUI( selected_obj ))
        menu.add_command(label="Mover", font="Arial 12", command= lambda: self.display_Move_GUI (object))
        menu.add_command(label="Ver propiedades", font="Arial 12", command=self.display_seeProperties)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def __loadContentInFSDisplay(self, search_result: list = []):
        self.textArea_Display.delete(0, "end")

        content = self.fileSystem.listDirectory() if len(search_result) == 0 else search_result

        for i in range(0, len(content)):
            self.textArea_Display.insert(i, content[i])

    def __onSearchRequest(self):
        search_value = self.textInput_SearchBar.get()
        if len(search_value) == 0:
            return

        search_result = self.fileSystem.findElement(search_value)
        self.__loadContentInFSDisplay( search_result )

    def __deleteFunction(self, selected_item: str):
        #verificacion y messagebox de si el archivo existe, tomar en cuenta que depende la operacion a realizar depende del tipo (Entonces primero debemos de sacar el tipo para luego proceder a eliminar)
        if messagebox.askyesno("Eliminar","¿Estás seguro que deseas eliminar este archivo/directorio?"):
            print("Eliminando el directorio/archivo")

            if "[FILE]" in selected_item:
                self.fileSystem.removeFile( selected_item.split("[FILE] ")[-1] )
            elif "[DIR]" in selected_item:
                self.fileSystem.remove_directory( selected_item.split("[DIR] ")[-1] )
            else:
                print("__deleteFunction: Object not recognized")
                return

            self.__loadContentInFSDisplay()

        else:
            print ("Cancelando eliminacion")

    def display_CreateDirectory_GUI(self):
        window = createDirectory_GUI.CreateDirectory_GUI(self)
        window.grab_set()
        self.__loadContentInFSDisplay()

    def display_WindowShowTree(self):
        window = showTree_GUI.ShowTree_GUI(self)
        window.grab_set()

    def display_CreateDisk_GUI(self):
        window = createDisk_GUI.CreateDisk_GUI(self)
        window.grab_set()

    def display_Move_GUI(self, object):
        window = move_GUI.Move_GUI(self, object)
        window.deiconify()
        window.update_idletasks()
        window.grab_set()

    def display_seeProperties(self):
        window = seeProperties_GUI.SeeProperties_GUI(self)
        window.grab_set()

    def display_Copy_GUI(self, selected_obj: File | Directory):
        window = copy_GUI.CopyFiles(self, selected_obj)
        window.grab_set()

    def display_CreateFile_GUI(self):
        window = createFile_GUI.CreateFile(self)
        window.grab_set()

    def display_EditFile_GUI(self, fileObj, content):
        window = editFile_GUI.EditFile(self, fileObj, content)
        window.deiconify()
        window.update_idletasks()
        window.grab_set()

    def deleteFunction(self):
        #verificacion y messagebox de si el archivo existe, tomar en cuenta que depende la operacion a realizar depende del tipo (Entonces primero debemos de sacar el tipo para luego proceder a eliminar)
        if messagebox.askyesno("Eliminar","¿Estás seguro que deseas eliminar este archivo/directorio?"):
            #Codigo que en caso de que el usuario presione que si
            print("Eliminando el directorio/archivo")
        else:
            print ("Cancelando eliminacion")

    def getFileContent(self, fileObj):
        return self.fileSystem.getFileContent(fileObj)

    def getFileObj(self,fileName):
        if fileName in self.fileSystem.currentDirectory.files:
            fileObj = self.fileSystem.currentDirectory.files[fileName]
        else:
            messagebox.showwarning("Este archivo no existe", f"El archivo '{fileName}' no existe en el directorio actual.")
            return None

        return fileObj

    def getDirObj(self, dirName):
        if dirName in self.fileSystem.currentDirectory.directories:
            dirObj = self.fileSystem.currentDirectory.directories[dirName]
        else:
            messagebox.showwarning("Este directorio no existe", f"El directorio '{dirName}' no existe en el directorio actual.")
            return None
        return dirObj

    def isUniqueInDestinyDir(self, name, type, destinyPath):
        destinyDirectory: Directory
        destinyDirectory = self.fileSystem.navigateToDirectory(destinyPath)

        # Verification to see if the path exists
        if destinyDirectory == None:
            messagebox.showwarning("Ruta no encontrada", "Favor ingresar una ruta correcta")

        if type == "File":
            return name in destinyDirectory.files
        else:
            return name in destinyDirectory.directories


if __name__ == "__main__":
    app = FileSystem_GUI()

    app.resizable(False, False)
    app.mainloop()

