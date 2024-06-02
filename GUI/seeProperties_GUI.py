from tkinter import Tk, Canvas, Entry, Text, Button, Toplevel

class SeeProperties_GUI(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

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
        canvas.place(x = 0, y = 0)

        # Text input: Search bar
        entry_1 = Entry( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        entry_1.place( x=9.0, y=10.0, width=722.0, height=33.0 )

        # Text area: Display
        entry_2 = Text( self, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        entry_2.place( x=171.0, y=67.0, width=558.0, height=459.0 )

        # Button
        button_1 = Button( self, text="Volver", borderwidth=0, highlightthickness=0, command=lambda: print("button_1 clicked"), relief="flat" )
        button_1.place( x=9.0, y=67.0, width=149.0000762939453, height=49.0 )
