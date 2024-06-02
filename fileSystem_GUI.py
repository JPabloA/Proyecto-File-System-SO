import GUI.showTree_GUI as showTree_GUI
import GUI.createDirectory_GUI as createDirectory_GUI
import GUI.move_GUI as move_GUI
import GUI.seeProperties_GUI as seeProperties_GUI
import GUI.createDisk_GUI as createDisk_GUI
import GUI.copy_GUI as copy_GUI
import GUI.createFile_GUI as createFile_GUI
import GUI.editFile_GUI as editFile_GUI
from tkinter import SINGLE, END, Tk, Canvas, Entry, Button, Listbox, Menu

from src.FileSystem import FileSystem

class FileSystem_GUI(Tk):

    fileSystem: FileSystem

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
        textInput_DirectoryPath = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=("Inter", 14))
        textInput_DirectoryPath.place( x=9.0, y=11.0, width=667.0, height=37.0 )

        self.__loadCurrentWorkingDirectory(textInput_DirectoryPath)

        # Text input: Search bar
        textInput_SearchBar = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_SearchBar.place( x=9.0, y=465.0, width=150.0, height=30.0 )

        # Text area: Display
        textArea_Display = Listbox( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, selectmode=SINGLE, font="Arial 14" )
        textArea_Display.place( x=173.0, y=72.0, width=558.0, height=459.0 )
        textArea_Display.bind("<Button-3>", lambda event: self.__contentDisplayRightClick(event, textArea_Display))

        self.__loadContentInFSDisplay(textArea_Display)

        # Button: Refresh display directory
        button_UpdateDirectory = Button( text="↺", command=lambda: self.__loadContentInFSDisplay(textArea_Display) , relief="flat", font="Arial 16" )
        button_UpdateDirectory.place( x=696.0, y=11.0, width=35.0, height=35.0 )

        button_1 = Button( text="Crear Disco", command=self.display_CreateDisk_GUI, relief="flat" )
        button_1.place( x=9.0, y=72.0, width=150.0, height=35.0 )

        button_2 = Button( text="Crear Directorio", borderwidth=0, command=self.display_CreateDirectory_GUI, relief="flat" )
        button_2.place( x=9.0, y=119.0, width=150.0, height=35.0 )

        button_3 = Button( text="Crear Archivo", borderwidth=0, command=self.display_CreateFile_GUI, relief="flat" )
        button_3.place( x=9.0, y=166.0, width=150.0, height=35.0 )

        button_4 = Button( text="Desp. Árbol", borderwidth=0, command=self.display_WindowShowTree, relief="flat" )
        button_4.place( x=9.0, y=213.0, width=150.0, height=35.0 )

        button_5 = Button( text="Buscar", borderwidth=0, command=lambda: print("button_5 clicked"), relief="flat" )
        button_5.place( x=9.0, y=503.0, width=150.0, height=30.0 )

    def __loadCurrentWorkingDirectory(self, path_field: Entry):
        cwd = self.fileSystem.getCurrentWorkingDirectory()

        path_field.insert(0, cwd)
        path_field.config(state="disabled")

    def __contentDisplayRightClick(self, event, display: Listbox):

        # Get the selected file/directory
        try:
            index = display.nearest(event.y)
            display.select_clear(0, END)
            display.selection_set( index )
            selected_item = display.get( index )
        except IndexError:
            return

        if len(selected_item) <= 0:
            return

        print(selected_item)
        print("PRUEBA")

        menu = Menu( tearoff=0 )
        menu.add_command(label="Abrir", font="Arial 12", command=self.display_EditFile_GUI)
        menu.add_command(label="Eliminar", font="Arial 12")
        menu.add_command(label="Copiar", font="Arial 12", command=self.display_Copy_GUI)
        menu.add_command(label="Mover", font="Arial 12", command=self.display_Move_GUI)
        menu.add_command(label="Ver propiedades", font="Arial 12", command=self.display_seeProperties)

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def __loadContentInFSDisplay(self, display: Listbox):

        print("Loading directories and files...")
        display.delete(0, "end")

        # TODO: Gather files and folders
        content = ["Carpeta1", "Carpeta2", "Carpeta3", "File1", "File2"]

        for i in range(0, len(content)):
            display.insert(i, content[i])

    def display_CreateDirectory_GUI(self):
        window = createDirectory_GUI.CreateDirectory_GUI(self)
        window.grab_set()

    def display_WindowShowTree(self):
        window = showTree_GUI.ShowTree_GUI(self)
        window.grab_set()

    def display_CreateDisk_GUI(self):
        window = createDisk_GUI.CreateDisk_GUI(self)
        window.grab_set()

    def display_Move_GUI(self):
        window = move_GUI.Move_GUI(self)
        window.grab_set()

    def display_seeProperties(self):
        window = seeProperties_GUI.SeeProperties_GUI(self)
        window.grab_set()

    # TODO: Verify if they work correctly (These 3 functions)
    def display_Copy_GUI(self):
        window = copy_GUI.CopyFiles(self)
        window.grab_set()
    
    def display_CreateFile_GUI(self):
        window = createFile_GUI.CreateFile(self)
        window.grab_set()
    
    def display_EditFile_GUI(self):
        window = editFile_GUI.EditFile(self)
        window.grab_set()       

if __name__ == "__main__":
    app = FileSystem_GUI()

    app.resizable(False, False)
    app.mainloop()
