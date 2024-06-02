from tkinter import Tk, Canvas, Entry, Text, Button

class SeeProperties_GUI(Tk):
    def __init__(self):
        super().__init__()

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
        entry_1 = Entry( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        entry_1.place( x=9.0, y=10.0, width=722.0, height=33.0 )

        # Text area: Display
        entry_2 = Text( bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0 )
        entry_2.place( x=171.0, y=67.0, width=558.0, height=459.0 )

        # Button
        button_1 = Button( text="Volver", borderwidth=0, highlightthickness=0, command=lambda: print("button_1 clicked"), relief="flat" )
        button_1.place( x=9.0, y=67.0, width=149.0000762939453, height=49.0 )

if __name__ == "__main__":
    app = SeeProperties_GUI()

    app.resizable(False, False)
    app.mainloop()
