from tkinter import Canvas, Entry, Text, Button, Toplevel, END
from src.file import File
from src.directory import Directory

class ShowTree_GUI(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Display directory tree")
        self.geometry("750x415")
        self.configure(bg = "#FFFFFF")
        self.resizable(False, False)

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 415,
            width = 750,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        canvas.place(x = 0, y = 0)

        tree:Directory = parent.fileSystem.root
        show_tree: str = tree.print_tree(tree)

        # Text input: Directory path
        entry_1 = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        entry_1.place( x=9.0, y=10.0, width=722.0, height=33.0 )

        # Button: Go back
        button_1 = Button( self, text="Volver", borderwidth=0, highlightthickness=0, command=self.destroy, relief="flat" )
        button_1.place( x=9.0, y=67.0, width=149.0, height=49.0 )

        # Text Area: Display
        entry_2 = Text( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        entry_2.insert(END, show_tree)
        entry_2.place( x=171.0, y=67.0, width=558.0, height=323.0 )
