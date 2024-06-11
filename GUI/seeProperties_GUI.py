from tkinter import Canvas, Entry, Text, Button, Toplevel, END
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
            print("Object could not be recognized")
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
            properties_print: str = f" name {properties["name"]},\n extension: {properties["extension"]},\n creationDate: {properties["creationDate"]},\n modificationDate: {properties["modificationDate"]},\n size: {properties["size"]}"
        else:
            properties_print: str = f" name {properties["name"]},\n creationDate: {properties["creationDate"]},\n number_items: {properties["number_items"]},\n total_size: {properties["total_size"]}"

        # Text input: Search bar
        self.entry_1 = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_1.insert(0, path_origin)
        self.entry_1.place( x=9.0, y=10.0, width=722.0, height=33.0 )

        # Text area: Display
        self.entry_2 = Text( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        self.entry_2.insert(END, properties_print)
        self.entry_2.place( x=171.0, y=67.0, width=558.0, height=459.0 )

        # Button
        self.button_1 = Button( self, text="Volver", borderwidth=0, highlightthickness=0, command=lambda: print("button_1 clicked"), relief="flat" )
        self.button_1.place( x=9.0, y=67.0, width=149.0000762939453, height=49.0 )
