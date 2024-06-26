from tkinter import Canvas, Entry, Text, Button, Toplevel, messagebox, END
from src.file import File
from src.directory import Directory

class SeeProperties_GUI(Toplevel):
    def __init__(self, parent, object):
        super().__init__(parent)

        self.parent = parent
        self.object = object

        path_origin: str = ""
        if isinstance(object, File):
            path_origin = f"{self.parent.fileSystem.getCurrentWorkingDirectory()}/{object.name}.{object.extension}"
            self.isFile = True
        elif isinstance(object, Directory):
            path_origin = f"{self.parent.fileSystem.getCurrentWorkingDirectory()}/{object.name}"
            self.isFile = False
        else:
            messagebox.showwarning("Properties", "Object could not be recognized")
            return

        self.title("Propiedades Files")
        self.geometry("750x550")
        self.configure(bg = "#FFFFFF")
        self.resizable(False, False)

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 550,
            width = 750,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)
        
        properties = object.viewProperties()
        if self.isFile:
            properties_print: str = f' Nombre del archivo {properties["name"]},\n Extensión: {properties["extension"]},\n Creado el: {properties["creationDate"]},\n Última modificación: {properties["modificationDate"]},\n Tamaño: {properties["size"]} bytes'
        else:
            properties_print: str = f' Nombre del directorio {properties["name"]},\n Creado el: {properties["creationDate"]},\n Total de items: {properties["number_items"]},\n Tamaño total: {properties["total_size"]} bytes'

        # Text input: Search bar
        self.entry_1 = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_1.insert(0, path_origin)
        self.entry_1.place( x=9.0, y=10.0, width=722.0, height=33.0 )
        self.entry_1.config(state="disabled")

        # Text area: Display
        self.entry_2 = Text( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_2.insert(END, properties_print)
        self.entry_2.place( x=171.0, y=67.0, width=558.0, height=459.0 )
        self.entry_2.config(state="disabled")

        # Button
        self.button_1 = Button( self, text="Volver", borderwidth=0, highlightthickness=0, command=lambda: self.buttonFunction(), relief="flat" )
        self.button_1.place( x=9.0, y=67.0, width=149.0000762939453, height=49.0 )
        
    
    def buttonFunction(self):
        self.destroy()
