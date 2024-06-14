from tkinter import Tk, Canvas, Entry, Text, Button, Toplevel, messagebox
from src.directory import Directory

class CreateDirectory_GUI(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title("Create Directory")
        self.geometry("750x138")
        self.configure(bg = "#FFFFFF")

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 138,
            width = 750,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        canvas.create_text( 9.0, 10.0, anchor="nw", text="Nombre del directorio:", fill="#000000", font=("Inter", 14) )

        # Text input: Directory path
        entry_1 = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font="Arial 12" )
        entry_1.place( x=9.0, y=35.0, width=722.0, height=25.0 )

        # Button: Crear
        button_1 = Button( self, text="Crear", borderwidth=0, highlightthickness=0, command=lambda: self.__createDirectory( entry_1 ), relief="flat" )
        button_1.place( x=9.0, y=75.0, width=149.0, height=49.0 )

    def __createDirectory(self, entry: Entry):
        directory_name = entry.get().strip()

        if len(directory_name) == 0:
            return

        created_dir: Directory | None = self.parent.fileSystem.createDirectory( directory_name )

        if created_dir is None:
            answer = messagebox.askyesno("Sobreescribir directorio", "Se encontró un directorio con el mismo nombre. ¿Desea sobreescribir su contenido?")
            if answer:
                selected_dir: Directory = self.parent.getDirObj( directory_name )
                self.parent.fileSystem.clearDirectory (selected_dir)
            else:
                return
        self.parent.reloadFileSystem()
        self.destroy()



