from tkinter import Tk, Canvas, Entry, Button, Toplevel
from src.file import File
from src.directory import Directory
class Move_GUI(Toplevel):
    
    def __init__(self, parent, object):
        super().__init__(parent)
        
        self.parent = parent
        self.object = object 
        
        if isinstance(object, File):
            print ("File")
        elif isinstance(object, Directory):
            print("Directory")
        
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
        textInput_SearchBar = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
        textInput_SearchBar.place( x=9.0, y=40.0, width=722.0, height=33.0 )
        print("print", self.object.name)
        textInput_SearchBar.insert(0, self.parent.fileSystem.getCurrentWorkingDirectory() + "/" + self.object.name)
        textInput_SearchBar.config(state="disabled")

        # Text input: Directory path 2
        textInput_SearchBar2 = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        textInput_SearchBar2.place( x=9.0, y=126.0, width=722.0, height=33.0 )
        textInput_SearchBar2.insert(0, self.parent.fileSystem.getCurrentWorkingDirectory())

        # Buttons
        button_1 = Button( self, text="Mover", borderwidth=0, highlightthickness=0, command=self.moveElement, relief="flat" )
        button_1.place( x=9.0, y=196.0, width=203.0, height=49.0 )

        button_2 = Button( self, text="Cancelar", borderwidth=0, highlightthickness=0, command=self.destroy, relief="flat" )
        button_2.place( x=9.0, y=270.0, width=203.0, height=49.0 )
    
    def moveElement(self):
        source_path = self.textInput_SearchBar.get()
        dest_path = self.textInput_SearchBar2.get()
        
        self.parent.fileSystem.moveElement(source_path, dest_path)
        